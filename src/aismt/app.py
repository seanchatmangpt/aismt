import asyncio

import streamlit as st
import pyperclip
from utils.create_prompts import create_python


async def main():
    # Define a Streamlit app title
    st.title("Advanced Python Assistant")

    # Create a Streamlit input for user choice
    user_choice = st.selectbox(
        "Choose an action:",
        ["Generate Python Code", "Update Python Code"],
    )

    # Create a Streamlit output area to display code
    code_output = st.empty()

    if user_choice == "Update Python Code":
        # Create a Streamlit checkbox to enable/disable code pasting
        paste_code = st.checkbox("Paste code to update")

        if paste_code:
            st.write("Please paste the code you'd like to update below:")
            code_to_update = st.text_area("Paste code here:", value=pyperclip.paste())
        else:
            code_to_update = st.text_area("What would you like for me to generate?")

        if st.button("Update Code"):
            code = code_to_update

            if paste_code:
                code += "\n\nUser: I would like to have " + code_to_update

                # Use st.spinner to indicate processing
            with st.spinner("Generating updated code..."):
                updated_code = await create_python(prompt=code)
            # Display updated code
            code_output.text("Updated Code:\n" + updated_code)

            # Copy the code to the clipboard
            pyperclip.copy(updated_code)

            st.success("Code has been updated and copied to the clipboard.")


asyncio.run(main())