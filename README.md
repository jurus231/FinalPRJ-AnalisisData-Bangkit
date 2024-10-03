# E-Commerce Public Dataset Analysis

This project is a **Streamlit** dashboard for analyzing an e-commerce public dataset. The dashboard provides insights into the top customers, most popular regions for purchases, and an RFM (Recency, Frequency, Monetary) analysis of customer behavior.

## Table of Contents
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Features](#features)
- [File Structure](#file-structure)
- [Deployment](#deployment)
- [License](#license)

---

## Installation

To run this project locally, follow the steps below.

### Clone the Repository
First, clone the repository to your local machine:

```bash
git clone https://github.com/jurus231/FinalPRJ-AnalisisData-Bangkit

cd https://github.com/jurus231/FinalPRJ-AnalisisData-Bangkit

python -m venv venv

Windows : 
    venv\Scripts\activate

Linux : 
    source venv/bin/activate

Install Dependencies : 
    pip install -r requirements.txt

Ensure the CSV File is in Place
Ensure that the CSV file (join_data.csv) is located at the specified path, or update the path in the load_data() function if necessary.

How to Run
To run the Streamlit dashboard:

Run the following command from the project directory:

- bash

- Copy code

- streamlit run app.py

- or you can just simply type https://khoiruddin28.streamlit.app/ in your browser, because i already deploy it inside streamlit community.

Features
This Streamlit dashboard provides the following features:

1. Customer Paling Banyak Belanja
Displays the customers who have spent the most.
Shows a line plot of customer contribution to total sales.
2. Daerah Paling Banyak Belanja
Displays the regions with the most purchases.
Visualized with a count plot showing the number of customers per region.
3. RFM (Recency, Frequency, Monetary) Analysis
Recency: The number of days since the last purchase.
Frequency: The number of unique orders a customer has placed.
Monetary: The total amount of money a customer has spent.
File Structure
Here is the general structure of the project:

bash
Copy code
FinalPRJ-AnalisisData-Bangkit
├───dashboard
| ├───join_data.csv
| └───dashboard.py
├───data
    -olist_customers_dataset.csv 
    -olist_geolocation_dataset.csv 
    -olist_order_items_dataset.csv 
    -olist_order_payments_dataset.csv 
    -olist_order_reviews_dataset.csv 
    -olist_orders_dataset.csv 
    -olist_products_dataset.csv 
    -olist_sellers_dataset.csv 
    -product_category_name_translation.csv
├───notebook.ipynb
├───README.md
└───requirements.txt
└───url.txt