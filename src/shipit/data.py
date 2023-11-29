import os

from sqlalchemy import create_engine
from sqlmodel import Session


current_dir = os.path.dirname(os.path.abspath(__file__))


db_path = os.path.join(current_dir, "dev.db")

DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL)


def get_session():
    return Session(engine)
