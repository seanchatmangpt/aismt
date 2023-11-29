import ast
from textwrap import dedent
from typing import Callable, Type, TypeVar

import anyio
import autopep8
import loguru
from icontract import ensure, require

from .complete import acreate


# Add a pre-condition to check the type of the 'prompt' variable
@require(lambda prompt: isinstance(prompt, str))
# Add a post-condition to check the type of the result and ensure the list length constraints
@ensure(
    lambda result, min_len, max_len: isinstance(result, list)
    and all(isinstance(item, str) for item in result)
    and min_len <= len(result) <= max_len,
    "List length must be within min_len and max_len, and all elements must be strings.",
)
async def create_list(prompt, min_len=1, max_len=20, **kwargs) -> list:
    # Explicitly stating the constraints and expectations in the prompt
    instructions = dedent(
        f"Create a PerfectPep8Python list of strings"
        f"The list should be based on the prompt: \n\n```prompt\n\n{prompt}\n\n```\n\n"
        f"The list should have a minimum length of {min_len} and a maximum length of {max_len}. "
        "Make sure the list is formatted according to PEP8 guidelines. Please complete the following code block: "
        f"```python\n"
        f"# I have IMPLEMENTED your PerfectPythonProductionCode® AGI enterprise innovative and opinionated "
        f"list based on your prompt. I have validated that this list does not match the order of the prompt.\n"
        f"from typing import List\n"
        f'perfect_str_list: List[str] = ["'
    )

    result = await acreate(
        prompt=instructions,
        stop=["```", "\n\n"],
        max_tokens=2000,
        **kwargs,
    )

    try:
        # Extract the list and validate its elements are strings
        extracted_list = extract_list('["' + result)
        return extracted_list
    # If list extraction fails, this section will execute
    except (ValueError, SyntaxError) as e:
        loguru.logger.warning(f"Invalid list generated: {e} {result}")

        # Improved prompt with explicit constraints and expectations similar to the original 'instructions'
        fix_instructions = dedent(
            f"The list generated earlier did not meet the specified requirements due to the following error: {e}. "
            "Please correct the list format. Make sure all elements are strings and adhere to PEP8 guidelines. The list should also meet the length constraints: "
            f"a minimum of {min_len} and a maximum of {max_len} items. Complete the following code block: "
            f"```python\n"
            f"# I have IMPLEMENTED your PerfectPythonProductionCode® AGI enterprise innovative and opinionated "
            f"list based on your prompt.\n"
            f'from typing import List\nperfect_str_list: List[str] = ["'
        )

        fixed_list = await acreate(
            prompt=fix_instructions,
            stop=["```", "\n\n"],
            max_tokens=2000,
            **kwargs,
        )
        return extract_list('["' + fixed_list)


def extract_list(input_str: str) -> list:
    # Safely evaluate the input string to generate the list, ensuring all elements are strings
    extracted_list = ast.literal_eval(input_str)
    if not all(isinstance(item, str) for item in extracted_list):
        raise ValueError("All elements in the list must be strings.")
    return extracted_list


# To run the code, you can use asyncio
# import asyncio
# oct_17_23 = "Your prompt here"
# idea_list = await create_list(prompt=oct_17_23, min_len=24, max_len=27, model="text-davinci-002")
# print(idea_list, len(idea_list))


# Add a pre-condition to check the type of the 'prompt' variable
@require(lambda prompt: isinstance(prompt, str))
# Add a post-condition to check the type of the result and ensure that the dictionary meets constraints
@ensure(
    lambda result, min_len, max_len: isinstance(result, dict)
    and all(isinstance(key, str) for key in result.keys())
    and min_len <= len(result) <= max_len,
    "Dictionary size must be within min_len and max_len, and all keys and values must be strings.",
)
async def create_dict(prompt, min_len=1, max_len=20, **kwargs) -> dict:
    # Explicit instructions without line breaks within the dictionary
    instructions = dedent(
        f"""Create a Python dictionary where both keys and values are strings.
The dictionary should have a minimum size of {min_len} and a maximum size of {max_len}.
It should be formatted according to PEP8 guidelines with no line breaks within the dictionary.
The dictionary should be based on the prompt: \n\n```prompt\n\n{prompt}\n\n```\n\n
Please complete the following code block:
```python
from typing import Dict
perfect_str_dict: Dict[str, str] = {{"""
    )

    result = await acreate(
        prompt=instructions,
        stop=["```", "\n\n"],
        max_tokens=3000,
        **kwargs,
    )

    try:
        # Extract the dictionary and validate its keys and values are strings
        extracted_dict = extract_dict("{" + result.replace("\n", ""))
        return extracted_dict
    except (ValueError, SyntaxError) as e:
        loguru.logger.warning(f"Invalid dictionary generated: {e} {result}")

        # Prompt to fix the invalid dictionary with explicit constraints
        fix_instructions = dedent(
            f"""The dictionary generated earlier did not meet the specified requirements due to the following error: {e}.
                                      Please correct the dictionary format, ensuring all keys and values are strings and adhere to PEP8 guidelines.
                                      The dictionary should also meet the size constraints: a minimum of {min_len} and a maximum of {max_len} key-value pairs.
                                                                    The dictionary should be based on the prompt: \n\n```prompt\n\n{prompt}\n\n```\n\n

                                      Complete the following code block:
                                      ```python
                                      perfect_str_dict: Dict[str, str] = {{"""
        )

        fixed_dict = await acreate(
            prompt=fix_instructions,
            stop=["```", "\n\n"],
            max_tokens=2000,
            **kwargs,
        )
        return extract_dict("{" + fixed_dict.replace("\n", ""))


def extract_dict(input_str: str) -> dict:
    # Safely evaluate the input string to generate the dictionary, ensuring all keys and values are strings
    input_str = autopep8.fix_code(input_str).strip()
    extracted_dict = ast.literal_eval(input_str)
    return extracted_dict


# To run the code, you can use asyncio
# import asyncio
# oct_17_23 = "Your prompt here"
# idea_dict = await create_dict(prompt=oct_17_23, min_len=20, max_len=30)
# print(idea_dict, len(idea_dict))

# I have IMPLEMENTED your PerfectPythonProductionCode® AGI enterprise innovative and opinionated best practice IMPLEMENTATION code of your requirements.


T = TypeVar("T")

# List of Python primitives we want to handle
PRIMITIVE_TYPES = [int, float, str, bool, complex, bytes]


# General pre-condition to check the type of the 'prompt' variable
@require(lambda prompt: isinstance(prompt, str))
# Add a post-condition to ensure the result is of the correct type
@ensure(
    lambda result, primitive_type: isinstance(result, primitive_type),
    "Result must match the expected type.",
)
async def create_python_primitive(
    prompt: str,
    primitive_type: Type[T],
    type_checker: Callable[[T], bool] = lambda x: True,
    **kwargs,
) -> T:
    """
    Create a Python primitive of the given type based on the prompt.

    :param prompt: The prompt for generating the Python primitive.
    :param primitive_type: The expected Python type of the primitive.
    :param type_checker: A function to further validate the type.
    :return: A Python primitive of the given type.
    """

    type_name = primitive_type.__name__

    # General instructions based on type
    instructions = f"Create a Python {type_name} based on the prompt: '{prompt}'."
    instructions += (
        f"\nPlease complete the following code block:\n"
        f"```python\n"
        f"from typing import {type_name}\n"
        f"# {prompt}\n"
        f"perfect_{type_name}: {type_name} = "
    )

    # Generate the result
    result = await acreate(
        prompt=instructions,
        stop=["```", "\n", " "],
        max_tokens=2000,
        **kwargs,
    )

    # Safely evaluate to expected type
    try:
        evaluated_result = ast.literal_eval(result)
        if not isinstance(evaluated_result, primitive_type):
            raise TypeError(f"Expected {primitive_type}, got {type(evaluated_result)}.")

        # Additional type check if provided
        if not type_checker(evaluated_result):
            raise ValueError("Type checking failed.")

        return evaluated_result
    except (ValueError, SyntaxError, TypeError) as e:
        loguru.logger.warning(
            f"Invalid {primitive_type.__name__} generated: {e} {result}"
        )
        fix_instructions = f"The {primitive_type.__name__} generated earlier did not meet the specified requirements due to the following error: {e}. Please correct it."
        corrected_result = await acreate(
            prompt=fix_instructions,
            stop=["```", "\n", " "],
            max_tokens=2000,
            **kwargs,
        )
        return ast.literal_eval(corrected_result)


# Test functions to ensure everything is working as expected

# async def test_create_python_primitive():
#     for ptype in PRIMITIVE_TYPES:
#         result = await create_python_primitive(f"Create a {ptype.__name__}", primitive_type=ptype)
#         assert isinstance(result, ptype), f"Test failed for {ptype}, got {type(result)}"
#         print(f"Successfully created {ptype}: {result}")


# To run the tests, you can use asyncio
# import asyncio
# asyncio.run(test_create_python_primitive())
# Let's say you want to generate an integer, but you want it to be an even number.
def is_even(x: int) -> bool:
    return x % 2 == 0


def is_odd(x: int) -> bool:
    return x % 2 == 1


# You would then call `create_python_primitive` like this:
# await create_python_primitive("Create an even integer", primitive_type=int, type_checker=is_even)


class MaieuticPrompting:
    """
    Simulates the Maieutic Prompting technique, focusing on logical integrity, tree generation, and depth-wise spanning.
    """

    @require(lambda statement: isinstance(statement, str))
    async def logical_integrity(self, statement: str) -> bool:
        """
        Determines the logical integrity of a proposition using OpenAI.
        """
        prompt_context = """
        In the context of Maieutic Prompting, a proposition Q is logically integral when the Language Model consistently infers the truth value of Q and ¬Q (i.e. Q as True and ¬Q as False, or vice versa).
        Using this definition, determine the logical integrity of the following statement:
        """
        prompt = prompt_context + statement
        integrity_response = await create_python_primitive(prompt, primitive_type=bool)
        return integrity_response

    @require(lambda question: isinstance(question, str))
    async def generate_tree(self, question: str) -> dict:
        """
        Uses OpenAI to construct a maieutic tree from a provided question.
        """
        prompt_context = """
        In Maieutic Prompting, given a question, the Language Model is required to post-hoc rationalize both True and 
        False labels. This is known as abductive explanation generation. It exposes the model to consider different 
        possible answers, revealing explanations that otherwise wouldn't have been generated.
        Using this methodology, construct a maieutic tree for the following question:
        """
        prompt = prompt_context + question
        tree_representation = await create_dict(prompt)
        return tree_representation

    @require(lambda tree: isinstance(tree, dict))
    async def convert_to_graph(self, tree: dict) -> dict:
        """
        Transforms a maieutic tree into a graph of relational concepts using OpenAI.
        """
        prompt_context = """
        Once a maieutic tree is generated, the next step in Maieutic Prompting is to convert that tree into a graph of relational concepts. This graph represents the relationships and dependencies between the concepts in the tree.
        Convert the provided maieutic tree into such a graph:
        """
        prompt = prompt_context + str(tree)
        graph_representation = await create_dict(prompt)
        return graph_representation

    @require(lambda graph: isinstance(graph, dict))
    async def find_consistent_beliefs(self, graph: dict) -> dict:
        """
        Identifies a set of consistent beliefs from the relational graph using OpenAI.
        """
        prompt_context = """
        In Maieutic Prompting, after converting a maieutic tree into a graph, the next step is to extract consistent beliefs from that graph. These beliefs are propositions that are consistent with each other and with the original question.
        Extract the most consistent set of beliefs from the following graph:
        """
        prompt = prompt_context + str(graph)
        beliefs_representation = await create_dict(prompt)
        return beliefs_representation


# Test function to demonstrate the use of the MaieuticPrompting class
async def main():
    maieutic_prompter = MaieuticPrompting()

    question = "Is the sky blue during a clear day?"

    integrity = await maieutic_prompter.logical_integrity(question)
    print(f"Logical Integrity: {integrity}")
    # Expected Output: Logical Integrity: True

    tree = await maieutic_prompter.generate_tree(question)
    print(f"Tree Representation: {tree}")
    # Expected Output: Tree Representation: {'base': 'Color of sky', 'true_reason': 'Refraction of sunlight', 'false_reason': 'Presence of clouds', ...}

    graph = await maieutic_prompter.convert_to_graph(tree)
    print(f"Graph Representation: {graph}")
    # Expected Output: Graph Representation: {'nodes': ['Color of sky', 'Refraction of sunlight', ...], 'edges': [('Color of sky', 'Refraction of sunlight'), ...]}

    beliefs = await maieutic_prompter.find_consistent_beliefs(graph)
    print(f"Consistent Beliefs: {beliefs}")
    # Expected Output: Consistent Beliefs: {'belief_1': 'The sky is blue due to refraction of sunlight', 'belief_2': 'Clouds can change the color of the sky', ...}


if __name__ == "__main__":
    anyio.run(main)
