import typer

from utils.complete import create

app = typer.Typer(
    help="""Planning, researching, collaborating,
and finalizing their assignments or projects."""
)


@app.command("plan")
def plan_assignment(
    title: str = typer.Argument(..., help="Title of the assignment or task."),
    deadline: str = typer.Option(
        None, help="Deadline in YYYY-MM-DD format (optional)."
    ),
    steps: str = typer.Option(None, help="Comma-separated list of steps (optional)."),
):
    """
    Plan and organize professional tasks and assignments with structured steps and timelines.
    """
    gpt_prompt = f"""You are a Plan Assignment assistant:
    Title: {title}
    Deadline: {deadline}
    Steps: {steps}
    
    {plan_assignment.__doc__}"""

    typer.echo(create(prompt=gpt_prompt))


@app.command("research")
def research_help(
    topic: str = typer.Argument(..., help="Topic for research."),
    depth: int = typer.Option(1, help="Depth of research, scale 1-5 (optional)."),
):
    """
    Provides research assistance for professional projects.
    """
    gpt_prompt = f"""You are a Research Help assistant:
    Topic: {topic}
    Depth of Depth of research, scale 1-5 (optional): {depth}
    
    {research_help.__doc__}"""

    typer.echo(create(prompt=gpt_prompt))


@app.command("collab")
def collaborate(
    members: str = typer.Argument(..., help="List of team members."),
    tasks: str = typer.Argument(..., help="List of tasks to be distributed."),
):
    """
    Facilitates collaboration on team assignments.
    """
    gpt_prompt = f"""You are a Collaborate assistant:
    Members: {members}
    Tasks: {tasks}
    
    {collaborate.__doc__}"""

    typer.echo(create(prompt=gpt_prompt))


@app.command("format")
def format_check(
    file: str = typer.Argument(..., help="Path to the document."),
    style: str = typer.Option(
        None, "--style", help="Formatting style (optional, e.g., APA, MLA)."
    ),
):
    """
    Checks and corrects document formatting.
    """
    with open(file, "r") as f:
        content = f.read()

    gpt_prompt = f"""You are a Format Check assistant:
    Formatting style (optional, e.g., APA, MLA).
    {style}
    
    {content}
    
    {format_check.__doc__}"""

    typer.echo(create(prompt=gpt_prompt))


@app.command("prepare")
def submission_preparation(
    file: str = typer.Argument(..., help="Path to the document."),
    review: bool = typer.Option(
        False, "--review", help="Flag to conduct a final review."
    ),
    checklist: bool = typer.Option(
        False, "--checklist", help="Flag to run a submission checklist."
    ),
):
    """
    Prepares documents for submission.
    """
    with open(file, "r") as f:
        content = f.read()

    gpt_prompt = f"""You are a Submission Preparation assistant:
    Review: {review}
    
    {content}
    
    {submission_preparation.__doc__}"""

    typer.echo(create(prompt=gpt_prompt))


if __name__ == "__main__":
    app()
