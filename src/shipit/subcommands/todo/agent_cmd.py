from utils.agent_tools import select_and_execute_function
from abc import ABC, abstractmethod
from pydantic import BaseModel
from datetime import datetime
from typing import Callable, Any
from utils.create_prompts import *


class Agent(BaseModel):
    agent_id: str
    memory: dict = {}  # Agent's memory for context
    functions: list[Callable] = []  # Agent's functions
    models: list[BaseModel] = []

    @property
    def persona(self) -> str:
        # Dynamically compute the agent's profile based on its functions
        func_names = [func.__name__ for func in self.functions]
        model_names = [model.__name__ for model in self.models]

        return (
            f"Agent ID: {self.agent_id}\nFunctions: {func_names}\nModels: {model_names}"
        )

    async def execute(self, instructions: str) -> Any | None:
        # Execute the instructions on the agent
        result = await select_and_execute_function(
            f"{instructions} {self.persona}", self.functions
        )
        await write(contents=result)
        return result


class AgentRepository(ABC):
    @abstractmethod
    def find_by_id(self, agent_id: str) -> Agent:
        pass

    @abstractmethod
    def find_all(self) -> list[Agent]:
        pass

    @abstractmethod
    def save(self, agent: Agent) -> None:
        pass


class AgentService:
    def __init__(self, repository: AgentRepository):
        self.repository = repository

    async def generate_response(self, agent_id: str, prompt: str) -> str:
        agent = self.repository.find_by_id(agent_id)
        if not agent:
            return "Agent not found."

        # the key for the memory is now
        now = datetime.now()
        agent.memory[now] = await acreate(prompt=prompt)
        return agent.memory[now]


class InMemoryAgentRepository(AgentRepository):
    def __init__(self):
        self.agents = {}  # key: agent_id, value: Agent

    def find_by_id(self, agent_id: str) -> Agent:
        return self.agents.get(agent_id)

    def find_all(self) -> list[Agent]:
        return list(self.agents.values())

    def save(self, agent: Agent) -> None:
        self.agents[agent.agent_id] = agent


class Orchestrator:
    def __init__(self, agents: list[Agent]):
        self.agents = agents

    async def choose_agent(self, task_description: str) -> Agent:
        async with anyio.create_task_group() as tg:
            suitable_agents = []
            for agent in self.agents:
                tg.start_soon(
                    self.evaluate_agent, agent, task_description, suitable_agents
                )

        if suitable_agents:
            return suitable_agents[
                0
            ]  # or any logic to select one from the suitable agents
        else:
            raise ValueError("No suitable agent found.")

    async def evaluate_agent(
        self, agent: Agent, task_description: str, suitable_agents: list
    ):
        if await self.is_suitable(agent, task_description):
            suitable_agents.append(agent)

    @staticmethod
    async def is_suitable(agent: Agent, task_description: str) -> bool:
        combined_prompt = (
            agent.persona
            + f"\n\nTask description: {task_description}\nIs this agent suitable or False?"
        )
        print("combined prompt:", combined_prompt)
        selected_function_name = await acreate(prompt=combined_prompt)
        print(f"Selected agent: {agent.agent_id}")

        return selected_function_name != "False"


import anyio


async def main():
    yaml_specialist = Agent(agent_id="YamlAssistant", functions=[create_yaml])
    jinja_specialist = Agent(agent_id="JinjaAssistant", functions=[create_jinja])
    python_coder = Agent(agent_id="PythonAssistant", functions=[create_python])
    pydantic_coder = Agent(
        agent_id="PydanticAssistant", functions=[create_pydantic_class]
    )
    # ... other agents ...

    team_agents = [jinja_specialist, python_coder, pydantic_coder]
    orchestrator = Orchestrator(team_agents)

    while True:
        task_description = "pizza api"  # input("Enter your website creation task description (or 'exit' to quit): ")

        if task_description.lower() == "exit":
            break

        selected_agent = await orchestrator.choose_agent(task_description)
        print(f"Selected Agent: {selected_agent.agent_id}")
        result = await selected_agent.execute(task_description)

        # Output the result (you can customize this part based on your needs)
        print("Agent's Response:")
        print(result)

        # Copy the result to the clipboard (optional)
        pyperclip.copy(result)


if __name__ == "__main__":
    anyio.run(main)
