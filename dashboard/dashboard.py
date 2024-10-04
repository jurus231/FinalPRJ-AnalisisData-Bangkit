import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

# Load data
cust_df = pd.read_csv("../data/olist_customers_dataset.csv")
geoloc_df = pd.read_csv("../data/olist_geolocation_dataset.csv")
order_item_df = pd.read_csv("../data/olist_order_items_dataset.csv")
order_payment_df = pd.read_csv("../data/olist_order_payments_dataset.csv")
order_reviews_df = pd.read_csv("../data/olist_order_reviews_dataset.csv")
orders_df = pd.read_csv("../data/olist_orders_dataset.csv")
products_df = pd.read_csv("../data/olist_products_dataset.csv")
sellers_df = pd.read_csv("../data/olist_sellers_dataset.csv")
translate_df = pd.read_csv("../data/product_category_name_translation.csv")

products_eng_df = pd.merge(products_df, translate_df, on="product_category_name", how="left")
products_eng_df['product_category_name'] = products_eng_df['product_category_name_english']
products_eng_df = products_eng_df.drop(columns=["product_category_name_english"])
order_reviews_df.isna().sum()

order_reviews_df_clean = order_reviews_df.dropna(subset=['review_comment_title', 'review_comment_message'])
orders_df_clean = orders_df.dropna(subset=['order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date'])
products_eng_df_clean = products_eng_df.dropna(subset=['product_category_name', 
                                                       'product_name_lenght', 
                                                       'product_description_lenght', 
                                                       'product_photos_qty', 
                                                       'product_weight_g', 
                                                       'product_length_cm', 
                                                       'product_height_cm', 
                                                       'product_width_cm'])

join_data= orders_df_clean.merge(cust_df,on="customer_id").merge(order_item_df, on="order_id").merge(products_eng_df_clean,on="product_id").merge(translate_df,on="product_category_name").merge(order_payment_df,on="order_id").merge(sellers_df,on="seller_id").merge(order_reviews_df_clean,on="order_id")

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
    top_customers = join_data.groupby("customer_unique_id")["payment_value"].sum().reset_index().sort_values("payment_value", ascending=False)
    st.write(top_customers)
    
    # Plotting
    ax = sns.barplot(x="payment_value", y="customer_unique_id", data=top_customers[:10])
    ax.set_title("Top 10 Customer paling banyak belanja")
    st.pyplot(plt)

# Pertanyaan 2: Daerah paling banyak belanja
elif analysis_option == "Daerah Paling Banyak Belanja":
    st.header("Statistik Daerah Paling Banyak Belanja")
    
    customer_count = join_data['customer_state'].value_counts()
    customer_percentage = (join_data['customer_state'].value_counts(normalize=True) * 100).round(2)
    most_customers_state = customer_count.idxmax()
    most_customers_count = customer_count.max()
    least_customers_state = customer_count.idxmin()
    least_customers_count = customer_count.min()

    # Menampilkan statistik tambahan dengan st.write()
    st.write("Total pelanggan per negara bagian:")
    st.write(customer_count)

    st.header("Visualisasi Statistik Daerah Paling Banyak Belanja")
    plt.figure(figsize=(15,8))
    sns.countplot(x='customer_state', data=join_data)
    plt.title('Daerah Paling Banyak Belanja')
    plt.xlabel('Kota')
    plt.ylabel('Banyaknya Customer')
    st.pyplot(plt)

# RFM Analysis
elif analysis_option == "RFM Analysis":
    st.header("RFM Analysis")
    df_recency = join_data.groupby(by="customer_unique_id", as_index=False)["order_purchase_timestamp"].max()
    df_recency.rename(columns={"order_purchase_timestamp":"Last_purchase_date"}, inplace=True)
    df_recency["Last_purchase_date"] = pd.to_datetime(df_recency["Last_purchase_date"])
    recent_date = pd.to_datetime(join_data["order_purchase_timestamp"]).max()
    df_recency["Recency"] = df_recency["Last_purchase_date"].apply(lambda x: (recent_date - x).days)
    frequency_df = join_data.groupby(["customer_unique_id"]).agg({"order_id":"nunique"}).reset_index()
    frequency_df.rename(columns={"order_id":"Frequency"}, inplace=True)
    
    monetary_df = join_data.groupby("customer_unique_id", as_index=False)["payment_value"].sum()
    monetary_df.columns = ["customer_unique_id", "Monetary"]
    
    rfm_df = df_recency.merge(frequency_df, on="customer_unique_id")
    rfm_df = rfm_df.merge(monetary_df, on="customer_unique_id").drop(columns="Last_purchase_date")
    
    st.write(rfm_df)

# Analisis Waktu Ekspedisi
elif analysis_option == "Analisis Waktu Ekspedisi":
    st.header("Analisis Waktu Ekspedisi")
    join_data['order_delivered_carrier_date'] = pd.to_datetime(join_data['order_delivered_carrier_date'])
    join_data['order_delivered_customer_date'] = pd.to_datetime(join_data['order_delivered_customer_date'])
    join_data['waktu_ekspedisi'] = (join_data['order_delivered_customer_date'] - join_data['order_delivered_carrier_date']).dt.days
    
    plt.figure(figsize=(10,6))
    sns.histplot(join_data['waktu_ekspedisi'], bins=50, kde=True)
    plt.title("Histogram Waktu Ekspedisi")
    plt.xlabel("Waktu Ekspedisi (hari)")
    plt.ylabel("Frekuensi")
    st.pyplot(plt)
    
    plt.figure(figsize=(10,6))
    sns.scatterplot(x=join_data['order_delivered_carrier_date'], y=join_data['waktu_ekspedisi'])
    plt.title("Scatterplot Waktu Ekspedisi vs Tanggal Pengiriman")
    plt.xlabel("Tanggal Pengiriman")
    plt.ylabel("Waktu Ekspedisi (hari)")
    st.pyplot(plt)