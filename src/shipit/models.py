import json
import uuid
from dataclasses import dataclass
from pathlib import Path

import openai
from dateutil import parser
from icontract import require, ensure
from pydantic import BaseModel
from slugify import slugify
from sqlmodel import Field, SQLModel, Relationship, select
from datetime import datetime
from typing import Optional, List, NamedTuple

from tzlocal import get_localzone

from shipit.data import get_session
from utils.crud_tools import add_model, update_model, delete_model, get_model


class OptionConfig(BaseModel):
    model: Optional[str]
    input_file: Optional[str]
    output_file: Optional[str]
    prompt: Optional[str]
    verbose: Optional[bool]
    auto_save: Optional[bool]
    paste_from_clipboard: Optional[bool]
    file_extension: Optional[str]
    append_to_output: Optional[bool]
    response: Optional[str]
    max_tokens: Optional[int]


class Calendar(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prodid: str = Field(description="Product Identifier")
    version: str = Field(description="Version of the calendar")
    calscale: Optional[str] = Field(description="Calendar scale used")
    method: Optional[str] = Field(description="Method used in the calendar")
    events: List["Event"] = Relationship(back_populates="calendar")
    todos: List["Todo"] = Relationship(back_populates="calendar")
    journals: List["Journal"] = Relationship(back_populates="calendar")


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: str = Field(description="Globally unique identifier")
    dtstamp: datetime = Field(description="Date/time stamp")
    dtstart: datetime = Field(description="Start date/time of the event")
    dtend: Optional[datetime] = Field(description="End date/time of the event")
    duration: Optional[str] = Field(description="Duration of the event")
    summary: Optional[str] = Field(description="Summary of the event")
    description: Optional[str] = Field(description="Full description of the event")
    location: Optional[str] = Field(description="Location of the event")
    calendar_id: Optional[int] = Field(default=None, foreign_key="calendar.id")
    calendar: Optional[Calendar] = Relationship(back_populates="events")
    alarms: List["Alarm"] = Relationship(back_populates="event")

    def to_ics(self, file_path: Optional[str] = None) -> str:
        """
        Converts the event to iCalendar format with the user's local timezone.
        """
        # Get the user's local timezone
        local_tz = get_localzone()

        # Convert event start and end times to the user's local timezone
        dtstart_local = self.dtstart.astimezone(local_tz)
        dtend_local = self.dtend.astimezone(local_tz) if self.dtend else None

        # Start the calendar
        ics_str = "BEGIN:VCALENDAR\n"
        ics_str += "VERSION:2.0\n"
        ics_str += "PRODID:-//YourCompany//YourProduct//EN\n"  # Example Product ID

        # Event details
        ics_str += "BEGIN:VEVENT\n"
        ics_str += f"UID:{self.uid}\n"
        ics_str += f'DTSTAMP:{self.dtstamp.strftime("%Y%m%dT%H%M%SZ")}\n'
        ics_str += f'DTSTART:{dtstart_local.strftime("%Y%m%dT%H%M%S")}\n'
        if dtend_local:
            ics_str += f'DTEND:{dtend_local.strftime("%Y%m%dT%H%M%S")}\n'
        if self.summary:
            ics_str += f"SUMMARY:{self.summary}\n"
        if self.description:
            ics_str += f"DESCRIPTION:{self.description}\n"
        if self.location:
            ics_str += f"LOCATION:{self.location}\n"
        ics_str += "END:VEVENT\n"

        # End the calendar
        ics_str += "END:VCALENDAR\n"

        # If path is a directory, save the ICS content to a file in that directory
        # the file name will be the event slugged summary and dtstart with a .ics extension
        if file_path and Path(file_path).is_dir():
            file_name = (
                f"{slugify(self.summary)}_{self.dtstart.strftime('%Y%m%dT%H%M%SZ')}.ics"
            )
            file_path = Path(file_path) / file_name
            with open(file_path, "w") as f:
                f.write(ics_str)
        elif file_path:
            with open(file_path, "w") as f:
                f.write(ics_str)

        return ics_str

    def __repr__(self):
        return (
            f"Event(id={self.id}, summary='{self.summary}', dtstart={self.dtstart}, "
            f"dtend={self.dtend}, duration={self.duration}, description='{self.description}', "
            f"location='{self.location}')"
        )

    def __str__(self):
        dtstart_str = self.dtstart.strftime("%I:%M%p on %A, %B %d, %Y")
        dtend_str = (
            self.dtend.strftime("%I:%M%p on %A, %B %d, %Y") if self.dtend else ""
        )
        return (
            f"Summary:\t{self.summary}\n"
            f"Start:\t\t{dtstart_str}\n"
            f"End:\t\t{dtend_str}\n"
            f"Description:\t{self.description}\n"
            f"Location:\t{self.location}"
        )

    @staticmethod
    @require(lambda dtstart: parser.parse(dtstart))
    @require(lambda dtend: dtend is None or parser.parse(dtend))
    @require(lambda duration: duration is None or isinstance(duration, str))
    @require(lambda summary: summary is None or isinstance(summary, str))
    @require(lambda description: description is None or isinstance(description, str))
    @require(lambda location: location is None or isinstance(location, str))
    @ensure(lambda result: result.id is not None)
    def create(
        dtstart: str,
        dtend: str = None,
        duration: str = None,
        summary: str = None,
        description: str = None,
        location: str = None,
    ) -> "Event":
        uid = uuid.uuid4()
        uid_str = str(uid)

        dtstamp = datetime.utcnow()

        event = Event(
            uid=uid_str,
            dtstamp=dtstamp,
            dtstart=parser.parse(dtstart),
            dtend=parser.parse(dtend) if dtend else None,
            duration=duration,
            summary=summary,
            description=description,
            location=location,
        )

        add_model(event)
        return event

    @staticmethod
    @require(lambda event_id: isinstance(event_id, int))
    @require(lambda dtstart: parser.parse(dtstart))
    @require(lambda dtend: dtend is None or parser.parse(dtend))
    @require(lambda duration: duration is None or isinstance(duration, str))
    @require(lambda summary: summary is None or isinstance(summary, str))
    @require(lambda description: description is None or isinstance(description, str))
    @require(lambda location: location is None or isinstance(location, str))
    # @ensure(lambda result: result.id is not None)
    def update(
        event_id: int,
        dtstart: str,
        dtend: str = None,
        duration: str = None,
        summary: str = None,
        description: str = None,
        location: str = None,
    ):
        with update_model(Event, event_id) as event:
            event.dtstamp = datetime.utcnow()
            event.dtstart = parser.parse(dtstart)
            event.dtend = parser.parse(dtend) if dtend else None
            event.duration = duration
            event.summary = summary
            event.description = description
            event.location = location

    @staticmethod
    @require(lambda event_id: isinstance(event_id, int))
    @ensure(lambda result, event_id: result is None)
    def delete(event_id: int) -> None:
        delete_model(Event, event_id)

    @staticmethod
    @require(lambda event_id: isinstance(event_id, int))
    @ensure(lambda result, event_id: result.id == event_id)
    def read(event_id: int) -> "Event":
        return get_model(Event, event_id)

    @staticmethod
    def most_recent() -> "Event":
        return get_session().exec(select(Event).order_by(Event.dtstamp.asc())).first()

    @staticmethod
    def get_by_page(
        page: int = 0,
        per_page: int = 10,
        sort: str = "dtstart",
        asc: bool = True,
        include_past: bool = False,
    ) -> List["Event"]:
        """Get events by page sorted by"""
        order_by = getattr(Event, sort).asc() if asc else getattr(Event, sort).desc()

        query = select(Event).order_by(order_by)

        if not include_past:
            # Add a filter to exclude past events
            query = query.filter(Event.dtstart >= datetime.now())

        return get_session().exec(query.offset(page * per_page).limit(per_page)).all()


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: str = Field(description="Globally unique identifier")
    dtstamp: datetime = Field(description="Date/time stamp")
    dtstart: Optional[datetime] = Field(description="Start date/time of the todo")
    due: Optional[datetime] = Field(description="Due date/time of the todo")
    summary: Optional[str] = Field(description="Summary of the todo")
    description: Optional[str] = Field(description="Description of the todo")
    completed: Optional[datetime] = Field(description="Completion date/time")
    calendar_id: Optional[int] = Field(default=None, foreign_key="calendar.id")
    calendar: Optional[Calendar] = Relationship(back_populates="todos")


class Journal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: str = Field(description="Globally unique identifier")
    dtstamp: datetime = Field(description="Date/time stamp")
    dtstart: Optional[datetime] = Field(
        description="Start date/time of the journal entry"
    )
    summary: Optional[str] = Field(description="Summary of the journal entry")
    description: Optional[str] = Field(description="Description of the journal entry")
    calendar_id: Optional[int] = Field(default=None, foreign_key="calendar.id")
    calendar: Optional[Calendar] = Relationship(back_populates="journals")


class Alarm(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    action: str = Field(description="Action of the alarm")
    trigger: datetime = Field(description="Trigger time of the alarm")
    duration: Optional[str] = Field(description="Duration of the alarm")
    repeat: Optional[int] = Field(description="Repeat count of the alarm")
    description: Optional[str] = Field(description="Description of the alarm")
    event_id: Optional[int] = Field(default=None, foreign_key="event.id")
    event: Optional[Event] = Relationship(back_populates="alarms")
