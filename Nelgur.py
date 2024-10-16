import os
import sqlite3
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

# setup database
if not os.path.exists('assets/sqlite3.db'):
    
    with sqlite3.connect('assets/sqlite3.db') as conn:
        curr = conn.cursor()
        
        curr.execute(
            '''
            CREATE TABLE Sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime DATETIME NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL
            );
            '''
        )

