import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Pembayaran", page_icon="💸")

'''# 💸Pembayaran'''
st.sidebar.header("Pembayaran")
st.write(
    """This page provides all stuffs related with "💸Pembayaran". Enjoy!"""
)

'''## :material/table_chart: Tampilan 5 Data Terakhir'''
stmt = f'''
        select
            ID,
            DateCreated,
            Amount,
            Type
        from
            Payments
        order by DateCreated desc 
        limit 5
        '''
df = pd.read_sql_query(stmt, sqlite3.connect('assets/sqlite3.db'))
df = df.rename(columns={
    'DateCreated': 'Tanggal', 
    'Amount': 'Jumlah',
    'Type': 'Keperluan'
})
df = df.set_index(keys=['ID'])
st.dataframe(df, use_container_width=True)

'''## :material/add_task: Tambahkan Pembayaran'''
with st.container(border=True):
    amount = st.number_input(
        "Masukkan jumlah", value=None, placeholder="IDR", format='%0.0f'
    )
    
    with sqlite3.connect('assets/sqlite3.db') as conn:
        curr = conn.cursor()
        
        data = curr.execute(
            '''
            select
                distinct Type
            from
                Payments
            '''
        ).fetchall()
        data = [_[0] for _ in data]
    
    amount_type = st.selectbox(
        "Pilih keperluan pembayaran", options=data
    )
    
    # Every form must have a submit button.
    submitted = st.button("Submit", use_container_width=True)
    if submitted:
        with sqlite3.connect('assets/sqlite3.db') as conn:
            now = datetime.now()
            curr = conn.cursor()
            
            curr.execute(
                '''
                insert into
                    Payments (DateCreated, Amount, Type)
                values
                    (?, ?, ?)
                ''', (now, amount, amount_type)
            )
        
        st.rerun()
