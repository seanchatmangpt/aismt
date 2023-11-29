import uuid

from munch import Munch
from sismic.interpreter import Interpreter
from sismic.io import import_from_yaml

from lchop.context.task_context import register_task


class StateContext:
    _instance = None
    charts = None
    interpreters = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StateContext, cls).__new__(cls, *args, **kwargs)
            cls.charts = Munch()
            cls.interpreters = Munch()
        return cls._instance


# @register_task
# async def state_from_file(work_ctx, filepath, chart_id, **kwargs):
#     if not chart_id:
#         chart_id = filepath
#     work_ctx.state_ctx.charts[chart_id] = import_from_yaml(filepath=filepath)
#     return {
#         "success": True,
#         "results": {"chart_id": chart_id, "chart": work_ctx.state_ctx.charts[chart_id]},
#     }
#
#
# @register_task
# async def state_from_string(work_ctx, yaml_string, chart_id, **kwargs):
#     if not chart_id:
#         chart_id = uuid.uuid4()
#     work_ctx.state_ctx.charts[chart_id] = import_from_yaml(text=yaml_string)
#     return {
#         "success": True,
#         "results": {"chart_id": chart_id, "chart": work_ctx.state_ctx.charts[chart_id]},
#     }


def create_interpreter(work_ctx, chart_id):
    if chart_id not in work_ctx.state_ctx.charts:
        raise ValueError(f"Statechart with ID {chart_id} has not been loaded.")
    work_ctx.state_ctx.interpreters[chart_id] = Interpreter(
        work_ctx.state_ctx.charts[chart_id], initial_context={"work_ctx": work_ctx}
    )


# @register_task
# async def execute_once(work_ctx, chart_id=None, **kwargs):
#     if chart_id not in work_ctx.state_ctx.interpreters:
#         create_interpreter(work_ctx, chart_id)
#     macro_step = work_ctx.state_ctx.interpreters[chart_id].execute_once()
#     return {
#         "success": True,
#         "results": {"chart_id": chart_id, "macro_step": macro_step},
#     }
#
#
# @register_task
# async def execute(work_ctx, chart_id, max_steps, **kwargs):
#     if chart_id not in work_ctx.state_ctx.interpreters:
#         create_interpreter(work_ctx, chart_id)
#     macro_steps = work_ctx.state_ctx.interpreters[chart_id].execute(max_steps=max_steps)
#     return {
#         "success": True,
#         "results": {"chart_id": chart_id, "macro_steps": macro_steps},
#     }
#
#
# @register_task
# async def queue(
#     work_ctx, chart_id, event_name, event_names, event_parameters, **kwargs
# ):
#     if chart_id not in work_ctx.state_ctx.interpreters:
#         create_interpreter(work_ctx, chart_id)
#     interpreter = work_ctx.state_ctx.interpreters[chart_id].queue(
#         event_name, *event_names, **event_parameters
#     )
#     return {
#         "success": True,
#         "results": {"chart_id": chart_id, "interpreter": interpreter},
#     }
