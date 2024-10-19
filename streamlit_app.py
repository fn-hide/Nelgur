import os
import sqlite3
import streamlit as st


# setup permission
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.header(':material/login: Log In')
    if st.button(":material/login:", use_container_width=True):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    st.header(':material/logout: Log Out')
    if st.button(":material/logout:", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()


# setup pages
page_login = st.Page(login, title="Log in", icon=":material/login:")
page_logout = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard = st.Page(
    "pages/home/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True
)
pickups = st.Page(
    "pages/distribution/pickups.py", title="Pickups", icon=":material/phishing:"
)
shipments = st.Page(
    "pages/distribution/shipments.py", title="Shipments", icon=":material/local_shipping:"
)

# setup database
if not os.path.exists('assets/sqlite3.db'):
    
    with sqlite3.connect('assets/sqlite3.db') as conn:
        curr = conn.cursor()
        
        curr.execute(
            '''
            CREATE TABLE Purchases (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                DateCreated DATETIME NOT NULL,
                Weight INTEGER NOT NULL,
                Price REAL NOT NULL,
                Amount REAL NOT NULL,
                Species NOT NULL,
                Count INTEGER,
                PaymentID INTEGER
            );
            '''
        )
        
        curr.execute(
            '''
            CREATE TABLE Sales (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                DateCreated DATETIME NOT NULL,
                Weight INTEGER NOT NULL,
                Price REAL NOT NULL,
                Amount REAL NOT NULL,
                Species NOT NULL,
                Count INTEGER,
                PaymentID INTEGER
            );
            '''
        )
        
        curr.execute(
            '''
            CREATE TABLE Payments (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                DateCreated DATETIME NOT NULL,
                Amount REAL NOT NULL,
                Type TEXT NOT NULL
            );
            '''
        )

# entrypoint
if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Home": [dashboard, page_logout],
            "Distribution": [pickups, shipments],
        }
    )
else:
    pg = st.navigation([page_login])

pg.run()
