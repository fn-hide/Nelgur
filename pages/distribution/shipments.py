import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Kiriman", page_icon="🚛")

'''# 🚛Kiriman'''
st.sidebar.header("Kiriman")
st.write(
    """This page provides all stuffs related with "🚛Kiriman". Enjoy!"""
)

'''## 🗒️Tampilan 5 Data Terakhir'''
stmt = f'''
        select
            s.id,
            s.datetime,
            s.weight,
            s.price,
            s.total,
            s.quantity,
            s.kind,
            p.amount
        from
            Sales s
        left join
            Payments p
        on
            p.id = s.payment_id
        order by s.datetime desc 
        limit 5
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
    'amount': 'Titipan'
})
df = df.set_index(keys=['ID'])
st.dataframe(df, use_container_width=True)

'''## 📤Tambahkan Kiriman'''
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
    payment = st.number_input(
        "Masukkan jumlah titipan (opsional)", value=None, placeholder="IDR", format='%0.0f'
    )

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(f"Berat {weight:,.0f} kg, Harga {price:,.0f} rupiah. Total {weight*price:,.0f}.- rupiah.")
        
        with sqlite3.connect('assets/sqlite3.db') as conn:
            curr = conn.cursor()
            
            if payment:
                curr.execute(
                    '''
                    insert into
                        Payments (datetime, amount)
                    values
                        (?, ?)
                    ''', (datetime.now(), payment, )
                )
                
                curr.execute(
                    '''
                    insert into
                        Sales (datetime, weight, price, total, quantity, kind, payment_id)
                    values
                        (?, ?, ?, ?, ?, ?, ?)
                    ''', (datetime.now(), weight, price, weight*price, quantity, kind, curr.lastrowid)
                )
            else:
                curr.execute(
                    '''
                    insert into
                        Sales (datetime, weight, price, total, quantity, kind)
                    values
                        (?, ?, ?, ?, ?, ?)
                    ''', (datetime.now(), weight, price, weight*price, quantity, kind)
                )
        
        st.rerun()
