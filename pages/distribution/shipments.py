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

'''## :material/table_chart: Tampilan 5 🚛 Terakhir'''
stmt = f'''
        select
            s.ID,
            s.DateCreated,
            s.Weight,
            s.Price,
            s.Amount SalesAmount,
            s.Count,
            s.Species,
            p.Amount PaymentsAmount
        from
            Sales s
        left join
            Payments p
        on
            p.ID = s.PaymentID
        order by s.DateCreated desc 
        limit 5
        '''
df = pd.read_sql_query(stmt, sqlite3.connect('assets/sqlite3.db'))
df = df.rename(columns={
    'DateCreated': 'Tanggal', 
    'Weight': 'Kirim',
    'Price': 'Harga',
    'SalesAmount': 'Subtotal',
    'Count': 'Ekor',
    'Species': 'Jenis',
    'PaymentsAmount': 'Titipan'
})
df = df.set_index(keys=['ID'])
st.dataframe(df, use_container_width=True)

'''## :material/add_task: Tambahkan Kiriman'''
with st.container(border=True):
    weight = st.number_input(
        "Masukkan berat", value=None, placeholder="Kilogram", format='%0.0f'
    )
    price = st.number_input(
        "Masukkan harga", value=None, placeholder="IDR", format='%0.0f'
    )
    if weight and price:
        st.write(f"Estimasi :green[laba kotor] pada kiriman saat ini adalah :green-background[Rp{weight*price:,.0f}.-] rupiah.")

    count = st.number_input(
        "Masukkan jumlah (opsional)", value=None, placeholder="ekor", format='%0.0f'
    )
    if count:
        st.write(f"Estimasi berat ikan :blue[per-ekor] adalah :blue-background[{weight/count:.2f}] kg.")

    species = st.selectbox(
        "Pilih jenis", options=['Gurami', 'Nila', 'Patin']
    )
    payment = st.number_input(
        "Masukkan jumlah titipan (opsional)", value=None, placeholder="IDR", format='%0.0f'
    )

    # Every form must have a submit button.
    submitted = st.button("Submit", use_container_width=True)
    if submitted:
        with sqlite3.connect('assets/sqlite3.db') as conn:
            now = datetime.now()
            curr = conn.cursor()
            
            if payment:
                curr.execute(
                    '''
                    insert into
                        Payments (DateCreated, Amount, Type)
                    values
                        (?, ?, ?)
                    ''', (now, payment, 'Kiriman')
                )
                
                curr.execute(
                    '''
                    insert into
                        Sales (DateCreated, Weight, Price, Amount, Species, Count, PaymentID)
                    values
                        (?, ?, ?, ?, ?, ?, ?)
                    ''', (now, weight, price, weight*price, species, count, curr.lastrowid)
                )
            else:
                curr.execute(
                    '''
                    insert into
                        Sales (DateCreated, Weight, Price, Amount, Count, Species)
                    values
                        (?, ?, ?, ?, ?, ?)
                    ''', (now, weight, price, weight*price, count, species)
                )
        
        st.rerun()
