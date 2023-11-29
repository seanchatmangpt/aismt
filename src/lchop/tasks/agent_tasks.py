# import asyncio

# from langchain.agents import AgentType, initialize_agent, load_tools
# from langchain.agents.agent_toolkits import create_python_agent
# from langchain.chat_models import ChatOpenAI
# from langchain.tools import PythonREPLTool
# from loguru import logger
# from munch import Munch

# async def load_agent(yaml_path, work_ctx):
#     try:
#         with open(yaml_path, "r") as stream:
#             agent_config = Munch.fromDict(yaml.safe_load(stream))
#
#         llm_name = agent_config.llm_name
#         tool_names = agent_config.tool_names
#         agent_type_name = agent_config.agent_type
#         verbose = agent_config.get("verbose", True)
#
#         llm = (
#             OpenAI(temperature=0) if llm_name == "OpenAI" else ChatOpenAI(temperature=0)
#         )
#         tools = load_tools(tool_names, llm=llm)
#         agent_type = AgentType[agent_type_name]
#
#         agent = initialize_agent(tools, llm, agent=agent_type, verbose=verbose)
#         AgentContext.register_agent(agent_config.name, agent)
#
#         logger.info(
#             f"Successfully loaded and registered agent {agent_config.name} from {yaml_path}."
#         )
#
#     except Exception as e:
#         logger.error(f"Failed to load agent from {yaml_path}: {str(e)}")
#         raise
#
#
# async def exe_agent(query, agent_name, agent_ctx):
#     try:
#         agent = agent_ctx.agents[agent_name]
#         result = agent.run(query)
#         logger.info(
#             f"Executed agent {agent_name} with query: '{query}'. Result: '{result}'"
#         )
#         return result
#
#     except Exception as e:
#         logger.error(f"Failed to execute agent {agent_name}: {str(e)}")
#         raise


# async def main():
#     agent_executor = create_python_agent(
#         llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
#         tool=PythonREPLTool(),
#         verbose=True,
#         agent_type=AgentType.OPENAI_FUNCTIONS,
#         agent_executor_kwargs={"handle_parsing_errors": True},
#     )
#
#     result = await agent_executor.arun("")
#     print(result)
#     # result  = await agent_executor.arun("What is the 10th fibonacci number?")
#

# if __name__ == "__main__":
# work_ctx = WorkContext(TaskContext(), TemplateContext(), BrowserContext())
# result = generate_task_code_from_workflow(
#     "your_workflow.yaml", "gen_email_tasks.py", work_ctx
# )
# print(result)

# asyncio.run(main())
