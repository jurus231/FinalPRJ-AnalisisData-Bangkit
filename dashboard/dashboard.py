import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    return pd.read_csv("join_data.csv")

data = load_data()

# Sidebar untuk memilih bagian dashboard
st.sidebar.title("Pilih Analisis")
analysis_option = st.sidebar.selectbox("Pilih bagian yang ingin ditampilkan:",
    ["Customer Paling Banyak Belanja", 
     "Daerah Paling Banyak Belanja", 
     "RFM Analysis", 
     "Analisis Waktu Ekspedisi"]
)

# Title dashboard
st.title("E-Commerce Public Dataset Analysis")

# Pertanyaan 1: Customer paling banyak belanja
if analysis_option == "Customer Paling Banyak Belanja":
    st.header("Customer Paling Banyak Belanja")
    top_customers = data.groupby("customer_unique_id")["payment_value"].sum().reset_index().sort_values("payment_value", ascending=False)
    st.write(top_customers)

    # Plotting
    plt.figure(figsize=(12,9))
    top_customers["% of Total Sales"] = (top_customers["payment_value"] / top_customers["payment_value"].sum()) * 100
    top_customers["Cum % of Total Sales"] = top_customers["% of Total Sales"].cumsum()
    ax = sns.lineplot(x=range(1, len(top_customers)+1), y="Cum % of Total Sales", data=top_customers)
    ax.set_xlabel("N = Customer")
    ax.set_title("% Kontribusi ke Bagian Sales dari banyaknya customer")
    st.pyplot(plt)

# Pertanyaan 2: Daerah paling banyak belanja
elif analysis_option == "Daerah Paling Banyak Belanja":
    st.header("Daerah Paling Banyak Belanja")
    plt.figure(figsize=(15,8))
    sns.countplot(x='customer_state', data=data)
    plt.title('Daerah Paling Banyak Belanja')
    plt.xlabel('Kota')
    plt.ylabel('Banyaknya Customer')
    st.pyplot(plt)

# RFM Analysis
elif analysis_option == "RFM Analysis":
    st.header("RFM Analysis")
    df_recency = data.groupby(by="customer_unique_id", as_index=False)["order_purchase_timestamp"].max()
    df_recency.rename(columns={"order_purchase_timestamp":"Last_purchase_date"}, inplace=True)
    df_recency["Last_purchase_date"] = pd.to_datetime(df_recency["Last_purchase_date"])
    recent_date = pd.to_datetime(data["order_purchase_timestamp"]).max()
    df_recency["Recency"] = df_recency["Last_purchase_date"].apply(lambda x: (recent_date - x).days)
    st.write(df_recency)

    frequency_df = data.groupby(["customer_unique_id"]).agg({"order_id":"nunique"}).reset_index()
    frequency_df.rename(columns={"order_id":"Frequency"}, inplace=True)
    st.write(frequency_df)

    monetary_df = data.groupby("customer_unique_id", as_index=False)["payment_value"].sum()
    monetary_df.columns = ["customer_unique_id", "Monetary"]
    st.write(monetary_df)

    rf_df = df_recency.merge(frequency_df, on="customer_unique_id")
    rfm_df = rf_df.merge(monetary_df, on="customer_unique_id").drop(columns="Last_purchase_date")
    st.write(rfm_df)

# Analisis Waktu Ekspedisi
elif analysis_option == "Analisis Waktu Ekspedisi":
    data['order_delivered_carrier_date'] = pd.to_datetime(data['order_delivered_carrier_date'])
    data['order_delivered_customer_date'] = pd.to_datetime(data['order_delivered_customer_date'])

    # Menghitung waktu ekspedisi
    data['waktu_ekspedisi'] = (data['order_delivered_customer_date'] - data['order_delivered_carrier_date']).dt.days

    # Histogram Waktu Ekspedisi
    st.subheader("Histogram Waktu Ekspedisi")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['waktu_ekspedisi'], bins=50, kde=True, ax=ax)
    ax.set_title("Histogram Waktu Ekspedisi")
    ax.set_xlabel("Waktu Ekspedisi (hari)")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)

    # Boxplot Waktu Ekspedisi
    st.subheader("Boxplot Waktu Ekspedisi")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data['waktu_ekspedisi'], ax=ax)
    ax.set_title("Boxplot Waktu Ekspedisi")
    ax.set_xlabel("Waktu Ekspedisi (hari)")
    st.pyplot(fig)

    # Scatterplot Waktu Ekspedisi vs Tanggal Pengiriman
    st.subheader("Scatterplot Waktu Ekspedisi vs Tanggal Pengiriman")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=data['order_delivered_carrier_date'], y=data['waktu_ekspedisi'], ax=ax)
    ax.set_title("Scatterplot Waktu Ekspedisi vs Tanggal Pengiriman")
    ax.set_xlabel("Tanggal Pengiriman")
    ax.set_ylabel("Waktu Ekspedisi (hari)")
    st.pyplot(fig)
