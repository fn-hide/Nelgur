import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime, date, timedelta


@st.cache_data
def convert_df(df: pd.DataFrame):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


st.set_page_config(page_title="Laporan", page_icon="📔")

'''# 📔Laporan'''
st.sidebar.header("Laporan")
st.write(
    """This page provides all stuffs related with "📔Laporan". Enjoy!"""
)

col1, col2 = st.columns(2, vertical_alignment='bottom')

now = datetime.now()
report_range = col1.date_input(
    "Pilih tanggal",
    value=(now - timedelta(7), now),
    min_value=date(2010, 1, 1),
    max_value=now,
    format="DD/MM/YYYY",
)

if len(report_range) == 2:
    report_type = col2.selectbox("Pilih jenis laporan", ["Kiriman", "Unduhan", "Pembayaran"])
    if report_type == 'Kiriman':
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
                where
                    s.DateCreated >= ?
                    and s.DateCreated <= ?
                '''
        df = pd.read_sql_query(stmt, sqlite3.connect('assets/sqlite3.db'), params=((report_range[0], report_range[1] + timedelta(1))))
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
        
        excel_shipments = convert_df(df)

        st.download_button(
            label=":material/download: Download data as CSV",
            data=excel_shipments,
            file_name=f"{report_type}_{report_range[0]}_{report_range[1]}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    elif report_type == 'Unduhan':
        stmt = f'''
                select
                    s.ID,
                    s.DateCreated,
                    s.Weight,
                    s.Price,
                    s.Amount PurchasesAmount,
                    s.Count,
                    s.Species,
                    p.Amount PaymentsAmount
                from
                    Purchases s
                left join
                    Payments p
                on
                    p.ID = s.PaymentID
                where
                    s.DateCreated >= ?
                    and s.DateCreated <= ?
                '''
        df = pd.read_sql_query(stmt, sqlite3.connect('assets/sqlite3.db'), params=((report_range[0], report_range[1] + timedelta(1))))
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
        
        excel_shipments = convert_df(df)

        st.download_button(
            label=":material/download: Download data as CSV",
            data=excel_shipments,
            file_name=f"{report_type}_{report_range[0]}_{report_range[1]}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    elif report_type == 'Pembayaran':
        stmt = f'''
                select
                    ID,
                    DateCreated,
                    Amount,
                    Type
                from
                    Payments
                where
                    DateCreated >= ?
                    and DateCreated <= ?
                '''
        df = pd.read_sql_query(stmt, sqlite3.connect('assets/sqlite3.db'), params=((report_range[0], report_range[1] + timedelta(1))))
        df = df.rename(columns={
            'DateCreated': 'Tanggal', 
            'Amount': 'Jumlah',
            'Type': 'Keperluan'
        })
        df = df.set_index(keys=['ID'])
        st.dataframe(df, use_container_width=True)
        
        excel_shipments = convert_df(df)

        st.download_button(
            label=":material/download: Download data as CSV",
            data=excel_shipments,
            file_name=f"{report_type}_{report_range[0]}_{report_range[1]}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        pass
