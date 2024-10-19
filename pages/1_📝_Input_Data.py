import os
import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Input Data", page_icon="📝")

'''# 📝Input Data'''
st.sidebar.header("Input Data")
st.write(
    """This page provides a form that receive some data with Nelgur. Enjoy!"""
)

'''## 🏓Tampilan 10 Data Terakhir'''
stmt = f'''
        select
            *
        from
            sales
        order by datetime desc 
        limit 10
        '''
df = pd.read_sql_query(stmt, sqlite3.connect('assets/sqlite3.db'))
df = df.rename(columns={
    'id': 'ID',
    'datetime': 'Tanggal', 
    'weight': 'Kirim',
    'price': 'Harga',
    'total': 'Subtotal',
    'quantity': 'Ekor',
    'kind': 'Jenis',
})
df = df.set_index(keys=['ID'])
st.dataframe(df, use_container_width=True)

'''## 🚛Tambahkan Kiriman'''
with st.form("sales"):
    weight = st.number_input(
        "Masukkan berat", value=None, placeholder="Kilogram", format='%0.0f'
    )
    price = st.number_input(
        "Masukkan harga", value=None, placeholder="IDR", format='%0.0f'
    )
    quantity = st.number_input(
        "Masukkan jumlah", value=None, placeholder="ekor", format='%0.0f'
    )
    kind = st.selectbox(
        "Pilih jenis", options=['Gurami', 'Nila', 'Patin']
    )

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(f"Berat {weight:,.0f} kg, Harga {price:,.0f} rupiah. Total {weight*price:,.0f}.- rupiah.")
        
        with sqlite3.connect('assets/sqlite3.db') as conn:
            curr = conn.cursor()
            
            curr.execute(
                '''
                insert into
                    Sales (datetime, weight, price, total, quantity, kind)
                values
                    (?, ?, ?, ?, ?, ?)
                ''', (datetime.now(), weight, price, weight*price, quantity, kind)
            )
        
        st.rerun()
