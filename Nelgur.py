import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.write("# Welcome to Nelgur! 👋")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    Nelgur is an sales app built specifically for
    Nelgur projects.
    **👈 Select a page from the sidebar** to see some examples
    of what Nelgur can do!
    ### Want to learn more?
"""
)