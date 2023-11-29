import streamlit as st
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from lchop.context.work_context import default_work_context
from lchop.tasks.template_tasks import generate_task_code_from_workflow
from utils.yaml_tools import YAMLMixin


class Task(BaseModel, YAMLMixin):
    name: str
    description: str
    kwargs: Dict[str, Any]


class Workflow(BaseModel, YAMLMixin):
    global_kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict)
    tasks: List[Task] = Field(default_factory=list)


def create_yaml_file(workflow: Workflow, filename: str):
    workflow.to_yaml(filename)
    st.success(f"YAML file '{filename}' has been created!")


def main():
    st.title("YAML Creator")

    st.sidebar.header("Workflow Configuration")
    global_kwargs = st.sidebar.text_area("Global Kwargs (YAML)", value="{}")
    tasks = st.sidebar.text_area("Tasks (YAML List)", value="[]")

    try:
        global_kwargs = eval(global_kwargs)
    except Exception as e:
        st.sidebar.error("Invalid Global Kwargs format. Please use valid JSON format.")
        return

    try:
        tasks = eval(tasks)
        if not isinstance(tasks, list):
            raise ValueError("Tasks must be a list.")
    except Exception as e:
        st.sidebar.error("Invalid Tasks format. Please use a valid JSON list format.")
        return

    workflow = Workflow(global_kwargs=global_kwargs, tasks=tasks)

    if st.sidebar.button("Create YAML File"):
        create_yaml_file(workflow, "workflow.yaml")

    st.sidebar.markdown("---")

    st.sidebar.header("Generate Task Code")
    if st.sidebar.button("Generate Task Code"):
        generate_task_code_from_workflow(
            work_ctx=default_work_context(),
            workflow_path="workflow.yaml",
            task_code_path="sub_page_tasks.py",
        )
        st.sidebar.success("Task code has been generated!")

    st.sidebar.markdown("---")

    st.sidebar.header("Load Workflow")
    uploaded_file = st.sidebar.file_uploader("Upload YAML File", type=["yaml", "yml"])
    if uploaded_file:
        st.sidebar.success("File uploaded successfully!")
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getvalue())

        st.sidebar.text("Loaded Workflow:")
        with open(uploaded_file.name, "r") as f:
            loaded_workflow_yaml = f.read()
            st.sidebar.code(loaded_workflow_yaml)

    st.markdown("## Workflow Configuration")
    st.write("Edit the workflow configuration on the left sidebar and click 'Create YAML File' to save it.")

    st.markdown("## Additional Actions")
    st.write(
        "Use the sidebar buttons to generate task code or load an existing workflow. "
        "You can also upload a YAML file to view its contents."
    )


if __name__ == "__main__":
    main()
