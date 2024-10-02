# %% [markdown]
# # Proyek Analisis Data: E-Commerce Public Dataset
# - **Nama:** Fikri Khoiruddin
# - **Email:** fikrikhoiruddin28@gmail.com
# - **ID Dicoding:** fikrikhoiruddin28

# %% [markdown]
# ## Menentukan Pertanyaan Bisnis

# %% [markdown]
# - Pertanyaan 1 : Siapa Customer yang paling banyak membeli?
# - Pertanyaan 2 : Daerah mana yang paling banyak belanja?

# %% [markdown]
# ## Import Semua Packages/Library yang Digunakan

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# ## Data Wrangling

# %% [markdown]
# ### Gathering Data

# %% [markdown]
# #**Gathering Data**
# Pada tahap ini saya akan read dataset yang akan saya pakai dalam Project Data Analysis ini.

# %%
cust_df = pd.read_csv("./Data/olist_customers_dataset.csv")
print(cust_df)

# %%
geoloc_df = pd.read_csv("./Data/olist_geolocation_dataset.csv")
print(geoloc_df)

# %%
order_item_df = pd.read_csv("./Data/olist_order_items_dataset.csv")
print(order_item_df)

# %%
order_payment_df = pd.read_csv("./Data/olist_order_payments_dataset.csv")
print(order_payment_df)

# %%
order_reviews_df = pd.read_csv("./Data/olist_order_reviews_dataset.csv")
print(order_reviews_df)

# %%
orders_df = pd.read_csv("./Data/olist_orders_dataset.csv")
print(orders_df)

# %%
products_df = pd.read_csv("./Data/olist_products_dataset.csv")
print(products_df)

# %%
sellers_df = pd.read_csv("./Data/olist_sellers_dataset.csv")
print(sellers_df)

# %%
translate_df = pd.read_csv("./Data/product_category_name_translation.csv")
print(translate_df)

# %%
products_eng_df = pd.merge(products_df, translate_df, on="product_category_name", how="left")

products_eng_df['product_category_name'] = products_eng_df['product_category_name_english']

products_eng_df = products_eng_df.drop(columns=["product_category_name_english"])

print(products_eng_df)

# %% [markdown]
# Men-Translate Nama Produk dalam products_df menjadi Berbahasa Inggris dengaan melakukan merger bersama translate_df

# %% [markdown]
# **Insight:**
# - Data yang dikumpulkan berdasarkan dari Situs E-Commerce yang bernama "Olist" bertempat dan beroperasi kebanyakan di Brazil, ada berbagai macam  jenis informasi dari dataset ini seperti, aktivitas belanja online, data pelanggan, produk, pesanan, pembayaran dan lain sebagainya.

# %% [markdown]
# ### Assessing Data

# %%
cust_df.info()
print()
geoloc_df.info()
print()
order_item_df.info()
print()
order_payment_df.info()
print()
order_reviews_df.info()
print()
orders_df.info()
print()
products_df.info()
print()
sellers_df.info()
print()
translate_df.info()


# %%
# Menampilkan informasi dasar dari masing-masing dataset
print("Order Payments Dataset Info:")
print(order_payment_df.info(), "\n")

print("Order Items Dataset Info:")
print(order_item_df.info(), "\n")

print("Orders Dataset Info:")
print(orders_df.info(), "\n")

print("Customers Dataset Info:")
print(cust_df.info(), "\n")

# Menampilkan statistik deskriptif untuk setiap dataset
print("Order Payments Dataset Descriptive Statistics:")
print(order_payment_df.describe(), "\n")

print("Order Items Dataset Descriptive Statistics:")
print(order_item_df.describe(), "\n")

print("Orders Dataset Descriptive Statistics:")
print(orders_df.describe(), "\n")

print("Customers Dataset Descriptive Statistics:")
print(cust_df.describe(), "\n")


# %%
# Collections for each dataset
datasets = [cust_df, geoloc_df, orders_df, order_item_df, order_payment_df,
            order_reviews_df, products_eng_df, sellers_df]
names = ['cust_df', 'geoloc_df', 'orders_df', 'order_item_df', 'order_payment_df',
         'order_reviews_df', 'products_eng_df', 'sellers_df']

# Creating a DataFrame with useful information about all datasets
data_info = pd.DataFrame({})
data_info['dataset'] = names
#[df.shape[0] for df in datasets] gives number of row count
data_info['n_rows'] = [df.shape[0] for df in datasets]
#[df.shape[1] for df in datasets] gives number of col count
data_info['n_cols'] = [df.shape[1] for df in datasets]
data_info['null_amount'] = [df.isnull().sum().sum()for df in datasets]
data_info['qty_null_columns'] = [len([col for col, null in df.isnull().sum().items() if null > 0]) for df in datasets] #which columns have nulls
data_info['null_columns'] = [', '.join([col for col, null in df.isnull().sum().items() if null > 0]) for df in datasets]
data_info.style.background_gradient()

# %% [markdown]
# ### Cleaning Data

# %%
cust_df.isna().sum()

# %%
geoloc_df.isna().sum()

# %%
order_item_df.isna().sum()

# %%
order_payment_df.isna().sum()

# %%
order_reviews_df.isna().sum()

# %%
orders_df.isna().sum()

# %%
products_df.isna().sum()

# %%
sellers_df.isna().sum()

# %%
translate_df.isna().sum()

# %% [markdown]
# **Insight:**
# - Untuk menghapus beberapa missing value yang ada diatas, saya memakai berbagai macam method tergantung dengan tipe data dan banyak-nya data yang mengalami missing value.
# - Untuk mengecek kembali apakah kolom data yang sudah dibenarkan sudah tidak terdapat missing value, saya menggunakan method isna().sum()

# %% [markdown]
# ## Exploratory Data Analysis (EDA)

# %% [markdown]
# ### Explore ...

# %% [markdown]
# Join Data agar lebih mudah meng-analisisnya di satu variabel

# %%
join_data= orders_df.merge(cust_df,on="customer_id").merge(order_item_df, on="order_id").merge(products_df,on="product_id").merge(translate_df,on="product_category_name").merge(order_payment_df,on="order_id").merge(sellers_df,on="seller_id").merge(order_reviews_df,on="order_id")

# %%
join_data.head()

# %%
top_customers= join_data.groupby("customer_unique_id")["payment_value"].sum().reset_index().sort_values("payment_value", ascending=False)
print(top_customers)


# %% [markdown]
# **Insight:**
# - Dari Exploratory Data Analysis diatas saya bisa mengkaitkan beberapa kolom yang berpotensi ada relasi-nya, seperti product dengan seller, produk dengan geolokasi, dan sebagai-nya
# - dan juga saya melakukan perhitungan secara kasar menggunakan code saja untuk bisa melihat hasil dari siapa yang belanja paling banyak sebelum nanti di visualisasikan.

# %% [markdown]
# ## Visualization & Explanatory Analysis

# %% [markdown]
# ### Pertanyaan 1: Customer paling banyak belanja

# %%
#Plotting
plt.figure(figsize=(12,9))
top_customers["% of Total Sales"] = (top_customers["payment_value"] / top_customers["payment_value"].sum()) * 100
top_customers["Cum % of Total Sales"] = top_customers["% of Total Sales"].cumsum()
ax = sns.lineplot(x=range(1,len(top_customers)+1), y="Cum % of Total Sales", data=top_customers)
ax.set_xlabel("N = Customer")
ax.set_title("% Kontribusi ke Bagian Sales dari banyaknya customer")

#filling with color the strongest cumulative part
a=np.arange(1,len(top_customers)+1)
b=top_customers["Cum % of Total Sales"]
plt.fill_between(a, b, 0,
                 where = (a >= 0) & (a <= 40000),
                 color = 'r')
ax.text(42000, 70, """40000 customers (sekitar 42% dari total customer) 
berkontribusi sekitar 80% dari total sales.""", fontsize=14)


# %%
ax = sns.barplot(x="payment_value", y="customer_unique_id", data=top_customers[:10])
ax.set_title("Top 10 Customer paling banyak belanja")

# %% [markdown]
# **Insight**
# - Berdasarkan dari tabel Plot diatas, kita dapat menyimpulkan bahwa customer dengan unique id seperti yang tertera itu menjadi tukang belanja yang paling banyak.
# - Berdasarkan Tabel Plot diagram merah kita bisa menyimpulkan bahwa kontribusi sales 80% berasal dari customer, yang mana itu sangat besar bagi perusahaan.

# %% [markdown]
# ### Pertanyaan 2: Kota Paling banyak belanja

# %%
plt.figure(figsize=(15,8))
sns.countplot(x='customer_state', data=join_data)
plt.title('Daerah Paling banyak belanja')
plt.xlabel('Kota')
plt.ylabel('Banyaknya Customer')

# %% [markdown]
# **Insight:**
# - Dari Tabel Plot diatas saya bisa menginformasikan bahwa, kota SP lah yang paling banyak berbelanja.
# - Dan juga ada beberapa kota yang potensial untuk bisa menjadi kota paling banyak berbelanja lain-nya, seperti kota PR,RJ,RS,MG, dan SC, selain kota itu kelihatannyaa relatif rendah.

# %% [markdown]
# ## Analisis Lanjutan (Opsional) RFM(Recency, Frequency, Monetary)

# %% [markdown]
# Menghitung Recency dari customer, tanggal terakhir customer membeli, saya me rename order_purchase_timestamp menjagi Last_purchase_date agar lebih mudah dibaca,terakhir convert last_purchase_date menjadi tanggal.

# %%
df_recency=join_data.groupby(by="customer_unique_id", as_index=False)["order_purchase_timestamp"].max()
df_recency.rename(columns={"order_purchase_timestamp":"Last_purchase_date"}, inplace=True)
df_recency["Last_purchase_date"]=pd.to_datetime(df_recency["Last_purchase_date"])
recent_date=pd.to_datetime(join_data["order_purchase_timestamp"]).max()
df_recency["Recency"]=df_recency["Last_purchase_date"].apply(lambda x=None: (recent_date - x).days)
df_recency.head()

# %% [markdown]
# Menghitung frekuensi customer menggunakan customer_unique_id menggunakan method .agg dan juga nunique

# %%
frequency_df=join_data.groupby(["customer_unique_id"]).agg({"order_id":"nunique"}).reset_index()
frequency_df.rename(columns={"order_id":"Frequency"}, inplace=True)
frequency_df.head()

# %%
monetary_df=join_data.groupby("customer_unique_id", as_index=False)["payment_value"].sum()
monetary_df.columns=["customer_unique_id","Monetary"]
monetary_df.head()

# %% [markdown]
# Gabungkan data data diatasa menjadi variabel rfm_df

# %%
rf_df=df_recency.merge(frequency_df, on="customer_unique_id")
rfm_df=rf_df.merge(monetary_df, on="customer_unique_id").drop(columns="Last_purchase_date")
rfm_df.head()

# %% [markdown]
# ## Conclusion

# %% [markdown]
# - Conclution pertanyaan 1 : Konklusi dari Analisis RFM
# 
# Dari analisis RFM yang telah dilakukan, beberapa konklusi yang bisa diambil adalah:
# 
# Identifikasi pelanggan berharga: Dengan menggunakan analisis RFM, kita dapat mengidentifikasi pelanggan yang memiliki nilai yang tinggi dan berpotensi menjadi pelanggan yang loyal.
# Segmentasi pelanggan: Analisis RFM memungkinkan kita untuk membagi pelanggan menjadi beberapa segmen berdasarkan perilaku dan nilai mereka, sehingga kita dapat membuat strategi pemasaran yang lebih efektif.
# 
# Pengembangan strategi pemasaran: Dengan memahami perilaku dan nilai pelanggan, kita dapat mengembangkan strategi pemasaran yang lebih efektif untuk meningkatkan penjualan dan meningkatkan loyalitas pelanggan.
# 
# Pengurangan biaya: Dengan mengidentifikasi pelanggan yang tidak berharga, kita dapat mengurangi biaya pemasaran dan meningkatkan efisiensi.
# Peningkatan loyalitas pelanggan: Dengan memahami perilaku dan nilai pelanggan, kita dapat meningkatkan loyalitas pelanggan dengan menawarkan produk dan layanan yang lebih sesuai dengan kebutuhan mereka.
# 
# Dalam keseluruhan, analisis RFM dapat membantu kita untuk memahami perilaku dan nilai pelanggan, sehingga kita dapat membuat keputusan yang lebih efektif dalam strategi pemasaran dan meningkatkan kesuksesan bisnis.
# 
# - Conclution pertanyaan 2 : Konklusi dari diagram diatas adalah :
# 
# Daerah SP mendominasi jumlah customer. Ini menunjukkan bahwa mayoritas customer berasal dari daerah SP.
# Terdapat beberapa daerah dengan jumlah customer yang cukup tinggi, seperti BA, PR, RJ, RS, dan MG.
# Sebagian besar daerah lainnya memiliki jumlah customer yang relatif rendah.
# 
# Konklusi Strategis:
# Fokuskan strategi marketing pada daerah dengan transaksi tinggi untuk meningkatkan penjualan.
# Upaya perlu dilakukan untuk meningkatkan transaksi di daerah dengan transaksi rendah.
# Investigasi lebih lanjut diperlukan untuk memahami faktor-faktor yang mempengaruhi transaksi di setiap daerah.
# 
# Konklusi Bisnis:
# Penting untuk mempertimbangkan kedua faktor jumlah transaksi dan nilai transaksi untuk mendapatkan gambaran yang lebih komprehensif.
# Analisis ini dapat membantu dalam pengambilan keputusan bisnis yang lebih tepat dan efektif.


