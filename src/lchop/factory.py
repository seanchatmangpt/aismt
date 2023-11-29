# Here is your PerfectProductionCode® AGI enterprise implementation you requested, I have verified that this accurately represents the conversation context we are communicating in:

from jinja2 import Template
import click
from click.testing import CliRunner

# Define the Jinja2 template string
template_str = '''
from click import group, command, option
from click.testing import CliRunner

@group()
def cli():
    """MetaCodeManufacturingPlant CLI"""
    pass

{% for cmd, opts in commands_dict.items() %}
@cli.command()
{% for opt_name, opt_details in opts.items() %}
@option('--{{ opt_name }}', default='{{ opt_details["default"] }}', help='{{ opt_details["help"] }}')
{% endfor %}
def {{ cmd }}({{ ", ".join(opts.keys()) }}):
    """This is the {{ cmd }} command"""
    print("Executing {{ cmd }} with options:", {{ ", ".join(opts.keys()) }})
{% endfor %}

def test_cli_commands():
    runner = CliRunner()
    {% for cmd in commands_dict.keys() %}
    print("Testing command: {{ cmd }}")
    result = runner.invoke(cli, ["{{ cmd|replace('_', '-') }}"])
    print(result.output)
    {% endfor %}

if __name__ == '__main__':
    test_cli_commands()
'''


def replace_dashes_with_underscores(data):
    if isinstance(data, dict):
        return {
            k.replace("-", "_"): replace_dashes_with_underscores(v)
            for k, v in data.items()
        }
    elif isinstance(data, str):
        return data.replace("-", "_")
    return data


# Sample dictionary parsed from your shell script
commands_dict = {
    "init": {"project": {"default": "None", "help": "Project name"}},
    "validate": {"workflow": {"default": "None", "help": "Workflow file"}},
    "build-backend": {
        "agent": {"default": "None", "help": "Agent name"},
        "task": {"default": "None", "help": "Task name"},
    },
    "generate-dashboard": {
        "agent": {"default": "None", "help": "Agent name"},
        "task": {"default": "None", "help": "Task summary"},
    },
    "test-backend": {},
}

commands_dict = replace_dashes_with_underscores(commands_dict)


# Create a Jinja2 template object
template = Template(template_str)

# Render the template
rendered_cli = template.render(commands_dict=commands_dict)

# Print or write to a .py file
print(rendered_cli)

open("cli.py", "w").write(rendered_cli)
