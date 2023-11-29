from loguru import logger
from munch import Munch


class AgentContext:
    _instance = None  # Private class variable to hold the single instance
    agents = Munch()  # Class-level dictionary to hold agent functions

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentContext, cls).__new__(cls)
            logger.info("AgentContext initialized.")
        return cls._instance

    @staticmethod
    def register_agent(name, agent):
        AgentContext.agents[name] = agent
        logger.info(f"Agent {name} registered.")
        return agent
