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
    'quantity': 'Kirim',
    'price': 'Harga',
    'total': 'Jumlah',
})
df = df.set_index(keys=['ID'])
st.dataframe(df, use_container_width=True)

'''## 🚛Tambahkan Kiriman'''
with st.form("sales"):
    col1, col2 = st.columns(2)
    quantity = col1.number_input(
        "Masukkan kuantitas", value=None, placeholder="Kilogram", format='%0.0f'
    )
    price = col2.number_input(
        "Masukkan harga", value=None, placeholder="IDR", format='%0.0f'
    )

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(f"Kuantitas {quantity:,.0f}, Harga {price:,.0f}. Total {quantity*price:,.0f}.-")
        
        with sqlite3.connect('assets/sqlite3.db') as conn:
            curr = conn.cursor()
            
            curr.execute(
                '''
                insert into
                    Sales (datetime, quantity, price, total)
                values
                    (?, ?, ?, ?)
                ''', (datetime.now(), quantity, price, quantity*price)
            )
        
        st.rerun()
