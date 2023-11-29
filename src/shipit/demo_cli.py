import typer
from typing import Callable, List

import inspect
import asyncio
import ast

from utils.agent_tools import select_and_execute_function
from utils.complete import create  # Assuming this is your OpenAI API wrapper


import icontract

from utils.create_primatives import create_dict

app = typer.Typer()


# Function definitions with icontract decorators


@icontract.require(
    lambda dataset_path: dataset_path.endswith(".csv"),
    "Dataset path must point to a CSV file.",
)
@icontract.require(
    lambda analysis_type: analysis_type in ["regression", "classification"],
    "Analysis type must be 'regression' or 'classification'.",
)
@icontract.require(
    lambda output_format: output_format in ["csv", "json"],
    "Output format must be 'csv' or 'json'.",
)
def perform_data_analysis(dataset_path: str, analysis_type: str, output_format: str):
    """
    Performs data analysis on the specified dataset.
    Args:
    dataset_path (str): Path to the dataset file. Must be a CSV file.
    analysis_type (str): Type of analysis to perform ('regression', 'classification').
    output_format (str): Format for the analysis output ('csv', 'json').
    """
    print(f"Analyzing {dataset_path} using {analysis_type} analysis.")
    print(f"Output will be provided in {output_format} format.")


@icontract.require(
    lambda action: action in ["create", "update", "delete"],
    "Action must be 'create', 'update', or 'delete'.",
)
@icontract.require(lambda user_id: user_id.isalnum(), "User ID must be alphanumeric.")
@icontract.require(
    lambda details: isinstance(details, dict), "Details must be a dictionary."
)
def manage_user_account(action: str, user_id: str, details: dict):
    """
    Manages user accounts based on the given action.
    Args:
    action (str): Action to perform on the user account ('create', 'update', 'delete').
    user_id (str): Unique identifier of the user account. Must be alphanumeric.
    details (dict): Additional details for the account action. Must be a dictionary.
    """
    print(f"Action '{action}' will be performed on user account with ID: {user_id}.")
    print(f"Additional details provided: {details}")


@app.command()
def chatbot():
    user_input = typer.prompt("How can I assist you today?")
    function_list = [perform_data_analysis, manage_user_account]
    asyncio.run(select_and_execute_function(user_input, function_list))


if __name__ == "__main__":
    app()
