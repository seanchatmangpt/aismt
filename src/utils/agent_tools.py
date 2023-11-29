import inspect
from typing import List, Callable, Any

from utils.complete import acreate
from utils.create_prompts import create_kwargs


async def choose_function(user_input: str, function_list: list):
    prompts = []
    for function in function_list:
        source = inspect.getsource(function)
        docstring = function.__doc__ if function.__doc__ else "No docstring provided."
        prompts.append(
            f"Function: {function.__name__}\nDocstring: {docstring.strip()}\nSource:\n{source}"
        )

    combined_prompt = (
        "\n\n".join(prompts)
        + f"\n\nUser input: {user_input}\nWhich function should be called?"
    )

    selected_function_name = await acreate(prompt=combined_prompt)

    for function in function_list:
        if function.__name__ in selected_function_name:
            print(f"Selected function: {function.__name__}")
            return function

    raise ValueError("No suitable function found.")


async def select_and_execute_function(
    instructions: str, function_list: List[Callable]
) -> Any | None:
    selected_function = await choose_function(instructions, function_list)
    function_signature = inspect.signature(selected_function)
    required_args = [
        param.name
        for param in function_signature.parameters.values()
        if param.default is param.empty
    ]

    source = inspect.getsource(selected_function)

    prompt_for_kwargs = f"""You are a Function Execution Assistant.
    Here are your instructions:
    ```instructions
    {instructions}.
    ```
    Create the kwargs dictionary for the function based on the user input
    
    Function:
    {source}"""

    kwargs = await create_kwargs(prompt_for_kwargs, selected_function)
    try:
        # If the selected function is a coroutine, await it
        print(
            f"Executing function: {selected_function.__name__}, is coroutine: {inspect.iscoroutinefunction(selected_function)}, kwargs: {kwargs}"
        )

        if inspect.iscoroutinefunction(selected_function):
            result = await selected_function(**kwargs)
            print(f"Result: {result}")
            return result
        else:
            result = await selected_function(**kwargs)
            print(f"Result: {result}")
            return result
    except TypeError as e:
        print(f"Error when calling the function: {e}")


async def execute_function(user_input: str, function: Callable):
    source = inspect.getsource(function)

    prompt_for_kwargs = f"The user has input {user_input}.\n\nCreate the kwargs dictionary for the function based on the user input\n\nFunction:\n{source}"

    kwargs = await create_kwargs(prompt_for_kwargs, function)
    try:
        return function(**kwargs)
    except TypeError as e:
        print(f"Error when calling the function: {e}")
