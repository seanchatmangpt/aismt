from loguru import logger
from munch import Munch


def register_task(func):
    TaskContext.tasks[func.__name__] = func
    # logger.info(f"Task {func.__name__} registered.")
    return func  # return the function so it can still be used normally


class TaskContext:
    _instance = None  # Private class variable to hold the single instance
    tasks = Munch()  # Class-level dictionary to hold task functions

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskContext, cls).__new__(cls)
            logger.info("TaskContext initialized.")
        return cls._instance
