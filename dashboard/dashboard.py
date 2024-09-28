import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import urllib.request
import matplotlib.image as mpimg


# read datasets
df_customers = pd.read_csv("https://raw.githubusercontent.com/nathsteve13/ecommerce-dataset-analysis/main/data/customers_dataset.csv")
df_geolocation = pd.read_csv("https://raw.githubusercontent.com/nathsteve13/ecommerce-dataset-analysis/main/data/geolocation_dataset.csv")
df_order_items = pd.read_csv("https://raw.githubusercontent.com/nathsteve13/ecommerce-dataset-analysis/main/data/order_items_dataset.csv")
df_order_payments = pd.read_csv("https://raw.githubusercontent.com/nathsteve13/ecommerce-dataset-analysis/main/data/order_payments_dataset.csv")
df_order_reviews = pd.read_csv("https://raw.githubusercontent.com/nathsteve13/ecommerce-dataset-analysis/main/data/order_reviews_dataset.csv")
df_orders = pd.read_csv("https://raw.githubusercontent.com/nathsteve13/ecommerce-dataset-analysis/main/data/orders_dataset.csv", parse_dates=['order_approved_at'])
df_product_category = pd.read_csv("https://raw.githubusercontent.com/nathsteve13/ecommerce-dataset-analysis/main/data/product_category_name_translation.csv")
df_products = pd.read_csv("https://raw.githubusercontent.com/nathsteve13/ecommerce-dataset-analysis/main/data/products_dataset.csv")
df_sellers = pd.read_csv("https://raw.githubusercontent.com/nathsteve13/ecommerce-dataset-analysis/main/data/sellers_dataset.csv")

# sidebar
with st.sidebar:
    st.header("Filter Options")
    start_date, end_date = st.date_input("Select Date Range", value=[datetime(2016, 9, 15), datetime(2016, 10, 15)])

    st.caption("Dashboard created by Nathanael Steven S (2024)")

# metric statistic
st.header("E-COMMERCE DASHBOARD")
col1, col2, col3, col4 = st.columns(4)

# metric statistic - average delivery time (days)
with col1:
    df_orders_with_region = pd.merge(df_orders, df_customers[['customer_id', 'customer_state']], on='customer_id')
    df_orders_with_region['order_delivered_customer_date'] = pd.to_datetime(df_orders_with_region['order_delivered_customer_date'], errors='coerce')
    df_orders_with_region['order_purchase_timestamp'] = pd.to_datetime(df_orders_with_region['order_purchase_timestamp'], errors='coerce')
    df_orders_with_region = df_orders_with_region.dropna(subset=['order_delivered_customer_date', 'order_purchase_timestamp'])
    df_orders_with_region['delivery_time_days'] = (df_orders_with_region['order_delivered_customer_date'] - df_orders_with_region['order_purchase_timestamp']).dt.days
    filtered_orders = df_orders_with_region[(df_orders_with_region['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
                                            (df_orders_with_region['order_purchase_timestamp'] <= pd.to_datetime(end_date))]
    if not filtered_orders.empty:
        average_delivery_time = round(filtered_orders['delivery_time_days'].mean())
        st.metric(label="Average delivery time", value=f"{average_delivery_time:,.2f} days")
    else:
        st.warning("No data available for the selected date range.")

# metric statistic - total revenue
with col2: 
    df_order_items_with_orders = pd.merge(df_order_items, df_orders[['order_id', 'order_purchase_timestamp']], on='order_id')
    df_order_items_with_orders['order_purchase_timestamp'] = pd.to_datetime(df_order_items_with_orders['order_purchase_timestamp'], errors='coerce')
    filtered_order_items = df_order_items_with_orders[(df_order_items_with_orders['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
                                                    (df_order_items_with_orders['order_purchase_timestamp'] <= pd.to_datetime(end_date))]
    total_revenue = filtered_order_items['price'].sum()
    st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")

# metric statistic - item sold
with col3:
    total_items_sold = filtered_order_items['order_item_id'].count()
    st.metric(label="Total Items Sold", value=total_items_sold)

# metric statistic - average review score
with col4: 
    df_order_reviews['review_creation_date'] = pd.to_datetime(df_order_reviews['review_creation_date'], errors='coerce')
    filtered_reviews = df_order_reviews[(df_order_reviews['review_creation_date'] >= pd.to_datetime(start_date)) &
                                        (df_order_reviews['review_creation_date'] <= pd.to_datetime(end_date))]
    if not filtered_reviews.empty:
        average_review_score = filtered_reviews['review_score'].mean()
        st.metric(label="Average Review Score", value=f"{average_review_score:.2f}")
    else:
        st.warning("No reviews available for the selected date range.")


# graph visualization 1 - daily revenue
df_non_cancelled = df_orders[df_orders['order_status'] != 'cancelled']
df_merged = pd.merge(df_non_cancelled[['order_id', 'order_approved_at']], df_order_items[['order_id', 'price']], on='order_id')
df_merged['order_approved_at'] = pd.to_datetime(df_merged['order_approved_at'], errors='coerce')
df_merged['day_month_year'] = df_merged['order_approved_at'].dt.to_period('D')
df_filtered = df_merged[(df_merged['order_approved_at'] >= pd.to_datetime(start_date)) &
                        (df_merged['order_approved_at'] <= pd.to_datetime(end_date))]
df_revenue_per_daily = df_filtered.groupby('day_month_year').agg({
    'price': 'sum'
}).reset_index().rename(columns={
    'price': 'total_revenue'
})
df_revenue_per_daily['day_month_year'] = df_revenue_per_daily['day_month_year'].dt.to_timestamp()
st.subheader("Daily Revenue")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df_revenue_per_daily['day_month_year'], df_revenue_per_daily['total_revenue'], marker='o', linestyle='-', color='b')
ax.set_title('Daily Revenue Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('Total Revenue ($)')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)



# graph visualization 2 - payment method used
df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'], errors='coerce')

df_filtered_orders = df_orders[(df_orders['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
                               (df_orders['order_purchase_timestamp'] <= pd.to_datetime(end_date))]

df_filtered_payments = pd.merge(df_order_payments, df_filtered_orders[['order_id', 'order_purchase_timestamp']], on='order_id')

df_payment_agg = df_filtered_payments.groupby(df_filtered_payments['payment_type']).agg({
    'payment_value': 'sum',
    'order_id': 'count'
}).rename(columns={
    'payment_value': 'total_transaction',
    'order_id': 'total_used'
}).reset_index()

st.subheader(f"Payment Methods Used from {start_date} to {end_date}")

if not df_payment_agg.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_payment_agg['payment_type'], df_payment_agg['total_transaction'], color='skyblue', label='Total Transaction')
    ax.set_title('Total Transaction Value by Payment Type')
    ax.set_xlabel('Payment Type')
    ax.set_ylabel('Total Transaction Value ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning(f"No data available for payment methods from {start_date} to {end_date}.")


# graph visualization 3 - highest and lowest product categories revenue
df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'], errors='coerce')
df_filtered_orders = df_orders[(df_orders['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
                               (df_orders['order_purchase_timestamp'] <= pd.to_datetime(end_date))]

df_filtered_order_items = pd.merge(df_order_items, df_filtered_orders[['order_id', 'order_purchase_timestamp']], on='order_id')
df_product_agg = df_filtered_order_items.groupby('product_id').agg({
    'order_item_id': 'count',          
    'price': 'sum',                    
}).rename(columns={
    'order_item_id': 'total_items_sold',
    'price': 'total_revenue',
})

df_final_product_agg = pd.merge(df_product_agg, df_products[['product_id', 'product_category_name']], on='product_id')
df_final_product_agg = pd.merge(df_final_product_agg, df_product_category[['product_category_name']], on='product_category_name', how='left')

df_category_agg = df_final_product_agg.groupby('product_category_name').agg({
    'total_items_sold': 'sum',
    'total_revenue': 'sum'
}).reset_index()

df_category_agg_sorted = df_category_agg.sort_values(by='total_revenue', ascending=False)
top_5_categories = df_category_agg_sorted.head(5)
bottom_5_categories = df_category_agg_sorted.tail(5)

st.subheader("Top 5 VS Buttom 5 Product Categories by Revenue")

tab1, tab2 = st.tabs(["Top 5", "Bottom 5"])
with tab1:
    st.subheader(f"Top 5 Product Categories by Revenue (from {start_date} to {end_date})")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_5_categories['product_category_name'], top_5_categories['total_revenue'], color='green')
    ax.set_title('Top 5 Product Categories by Revenue')
    ax.set_xlabel('Total Revenue ($)')
    ax.set_ylabel('Product Category')
    plt.tight_layout()
    st.pyplot(fig)

with tab2:
    st.subheader(f"Bottom 5 Product Categories by Revenue (from {start_date} to {end_date})")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(bottom_5_categories['product_category_name'], bottom_5_categories['total_revenue'], color='red')
    ax.set_title('Bottom 5 Product Categories by Revenue')
    ax.set_xlabel('Total Revenue ($)')
    ax.set_ylabel('Product Category')
    plt.tight_layout()
    st.pyplot(fig)



# graph visualization 4 - total item sold for each state
df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'], errors='coerce')
df_filtered_orders = df_orders[(df_orders['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
                               (df_orders['order_purchase_timestamp'] <= pd.to_datetime(end_date))]

df_merged_items_products = pd.merge(df_order_items, df_products[['product_id', 'product_category_name']], on='product_id')
df_merged_items_orders = pd.merge(df_merged_items_products, df_filtered_orders[['order_id', 'customer_id', 'order_purchase_timestamp']], on='order_id')
df_final = pd.merge(df_merged_items_orders, df_customers[['customer_id', 'customer_state']], on='customer_id')

df_top_selling = df_final.groupby(['customer_state', 'product_category_name']).agg({
    'order_item_id': 'count'  
}).reset_index().rename(columns={
    'order_item_id': 'total_items_sold'
})

df_top_category_per_state = df_top_selling.loc[df_top_selling.groupby('customer_state')['total_items_sold'].idxmax()]

tab3, tab4 = st.tabs(["Items Sold by State", "Top Selling Product by State"])

with tab3:
    st.subheader("Total Items Sold by State")

    if not df_top_category_per_state.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.bar(df_top_category_per_state['customer_state'], df_top_category_per_state['total_items_sold'], color='purple')
        
        ax.set_title(f'Total Items Sold by State (Top Category) from {start_date} to {end_date}')
        ax.set_xlabel('State')
        ax.set_ylabel('Total Items Sold')
        
        plt.xticks(rotation=45)  
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning(f"No data available for the selected date range from {start_date} to {end_date}.")

with tab4: 
    st.subheader(f"Top Selling Product Categories by State (from {start_date} to {end_date})")
    st.write(df_top_category_per_state)



# graph visualization 5 - average rating
df_order_reviews['review_creation_date'] = pd.to_datetime(df_order_reviews['review_creation_date'], errors='coerce')

df_filtered_reviews = df_order_reviews[(df_order_reviews['review_creation_date'] >= pd.to_datetime(start_date)) &
                                       (df_order_reviews['review_creation_date'] <= pd.to_datetime(end_date))]

df_merged = pd.merge(df_order_items, df_filtered_reviews[['order_id', 'review_score']], on='order_id')

average_review_score_per_product = df_merged.groupby('product_id')['review_score'].mean().reset_index()
average_review_score_per_product.columns = ['product_id', 'average_review_score']

df_final = pd.merge(average_review_score_per_product, df_products[['product_id', 'product_category_name']], on='product_id')

df_final['product_category_name'] = df_final['product_category_name'].fillna('Unknown')

df_final[['product_category_name', 'average_review_score']]

st.subheader(f"Average Review Score per Product Category (from {start_date} to {end_date})")

if not df_final.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df_final['product_category_name'], df_final['average_review_score'], color='orange')
    ax.set_title('Average Review Score per Product Category')
    ax.set_xlabel('Average Review Score')
    ax.set_ylabel('Product Category')
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning(f"No reviews available for the selected date range from {start_date} to {end_date}.")


# graph visualization 6 - geospasial
f_filtered_orders = df_orders[(df_orders['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
                               (df_orders['order_purchase_timestamp'] <= pd.to_datetime(end_date))]

df_orders_customers = pd.merge(df_filtered_orders[['order_id', 'customer_id']], df_customers, on='customer_id')

df_orders_geo = pd.merge(df_orders_customers, df_geolocation[['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng']], 
                         left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix')

if df_orders_geo.empty:
    st.warning("No data available for the selected date range.")
else:
    st.subheader(f"Customer data geolocation (from {start_date} to {end_date})")

    st.write("Data Geolocation:", df_orders_geo.head())

    url = 'https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'
    brazil_map = mpimg.imread(urllib.request.urlopen(url), 'jpg')

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(df_orders_geo['geolocation_lng'], df_orders_geo['geolocation_lat'], alpha=0.6, s=20, c='maroon')
    ax.axis('off')
    ax.imshow(brazil_map, extent=[-73.98283055, -33.8, -33.75116944, 5.4])
    st.pyplot(fig)


st.caption("Dashboard created by Nathanael Steven S (2024)")