"""aismt CLI."""
import inspect
import sys
from typing import NamedTuple

from utils.complete import create

"""
Feature: Interactive CLI Robot
Scenario: Robot can be placed on a 2d plane
Given a 2d plane
When I place the robot at 0,0 facing north
Then the robot is at 0,0 facing north
"""



import typer

app = typer.Typer()


@app.command()
def test() -> None:
    """Say a message."""
    map = Map()
    map.create_map([Coordinate(1, 1), Coordinate(2, 2)])
    typer.echo(map)


class Coordinate(NamedTuple):
    x: int
    y: int


class Obstacle:
    def __init__(self):
        pass


class Map:
    def __init__(self):
        self.width = 3
        self.height = 3
        self.map_dict: dict[Coordinate, Obstacle | None] = {}

    def create_map(self, obstacle_coords: list[Coordinate]) -> None:
        for obstacle_coord in obstacle_coords:
            self.map_dict[obstacle_coord] = Obstacle()

    def __str__(self):
        return f"Map has obstacles at {self.map_dict.keys()}"


class Robot:
    def __init__(self, x, y, orientation, map):
        self.x = 0
        self.y = 0
        self.orientation = "E"
        self.map = map

    def turn_left(self):
        if self.orientation == "E":
            self.orientation = "N"
        elif self.orientation == "N":
            self.orientation = "W"
        elif self.orientation == "W":
            self.orientation = "S"
        elif self.orientation == "S":
            self.orientation = "E"

    def turn_right(self):
        if self.orientation == "E":
            self.orientation = "S"
        elif self.orientation == "S":
            self.orientation = "W"
        elif self.orientation == "W":
            self.orientation = "N"
        elif self.orientation == "N":
            self.orientation = "E"

    def move_forward(self):
        if self.orientation == "E":
            if self.check_for_obstacle(self.x + 1, self.y):
                return
            self.x += 1
        elif self.orientation == "S":
            if self.check_for_obstacle(self.x, self.y - 1):
                return
            self.y -= 1
        elif self.orientation == "W":
            if self.check_for_obstacle(self.x - 1, self.y):
                return
            self.x -= 1
        elif self.orientation == "N":
            if self.check_for_obstacle(self.x, self.y + 1):
                return
            self.y += 1

    def check_for_obstacle(self, x, y):
        print(f"Checking for obstacle {self.map}")
        if Coordinate(x, y) in self.map.map_dict:
            print("Obstacle detected")
            return True

    def __str__(self):
        return f"Robot is at {self.x}, {self.y} facing {self.orientation}"

@app.command("int")
def interact() -> None:
    """Interact with the Turning Robot."""
    # Print out a 3x3 grid with the robot in the middle
    done = False

    map = Map()
    map.create_map([Coordinate(1, 0), Coordinate(2, 2)])

    robot = Robot(0, 0, "E", map)

    while not done:
        text = typer.prompt("What would you like to do? L or R to turn, F to move forward, Q to quit.").lower()

        if text == "l":
            typer.echo("Turning left")
            robot.turn_left()

        if text == "r":
            typer.echo("Turning right")
            robot.turn_right()

        if text == "f":
            typer.echo("Moving forward")
            robot.move_forward()

        if text == "q":
            typer.echo("Quitting")
            done = True

        typer.echo(robot)


def save_state(robot: tuple) -> None:
    """Save the state of the robot to a file."""
    with open("robot.txt", "w") as f:
        f.write(str(robot))


def load_state(robot: tuple) -> None:
    """Load the state of the robot from a file."""
    with open("robot.txt", "r") as f:
        robot = f.read()


@app.command("chat")
def chat():
    prompt = typer.prompt("Hello, I am the interview bot.")
    this_modules_source = inspect.getsource(sys.modules[__name__])

    typer.echo(create(prompt=f"{prompt}"))

