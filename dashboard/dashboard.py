import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
file_path = 'main_data.csv'
main_data = pd.read_csv(file_path)

# Preprocessing data for dashboard
main_data['order_purchase_timestamp'] = pd.to_datetime(main_data['order_purchase_timestamp'])
main_data['order_delivered_carrier_date'] = pd.to_datetime(main_data['order_delivered_carrier_date'])

# Sidebar Profile Section
st.sidebar.title("Adriel F.S.")
st.sidebar.image("e-commerce_logo.png", width=300)  # Path to the uploaded image file

# Sidebar for date range selection
st.sidebar.header("Filter Date Range")
start_date = st.sidebar.date_input('Start date', main_data['order_purchase_timestamp'].min().date())
end_date = st.sidebar.date_input('End date', main_data['order_purchase_timestamp'].max().date())

# Filter the data by selected date range
filtered_data = main_data[(main_data['order_purchase_timestamp'] >= pd.Timestamp(start_date)) &
                          (main_data['order_purchase_timestamp'] <= pd.Timestamp(end_date))]


st.title("📊 E-Commerce Dashboard")

# 1. Daily Orders Delivered Chart (Interactive)
daily_orders = filtered_data.groupby(filtered_data['order_delivered_carrier_date'].dt.date).size()
total_orders = daily_orders.sum()

# Total revenue calculation
total_revenue = filtered_data['price'].sum()

st.header("📦 Daily Orders Delivered")
st.write(f"**Total Orders:** {total_orders}")
st.write(f"**Total Revenue:** ${total_revenue:,.2f}")
fig_daily_orders = px.line(x=daily_orders.index, y=daily_orders.values, labels={'x': 'Date', 'y': 'Number of Orders'},
                           title="Daily Orders Delivered")
st.plotly_chart(fig_daily_orders)

# 2. Customer Spend Money Chart (Interactive) 
st.header("💰 Customer Spend Money (by Date)")
customer_spend_by_date = filtered_data.groupby(filtered_data['order_purchase_timestamp'].dt.date)['price'].sum()
total_spend = customer_spend_by_date.sum()
average_spend = customer_spend_by_date.mean()

st.write(f"**Total Spend:** ${total_spend:,.2f}")
st.write(f"**Average Spend per Day:** ${average_spend:,.2f}")
fig_customer_spend = px.line(x=customer_spend_by_date.index, y=customer_spend_by_date.values, 
                             labels={'x': 'Date', 'y': 'Total Spend'},
                             title="Customer Spend Money by Date")
st.plotly_chart(fig_customer_spend)

# 3. Number of Items in Orders (by Date) 
st.header("📦 Number of Items in Orders (by Date)")
items_by_date = filtered_data.groupby(filtered_data['order_purchase_timestamp'].dt.date)['order_item_id'].count()
total_items = items_by_date.sum()
average_items = items_by_date.mean()

st.write(f"**Total Items Ordered:** {total_items}")
st.write(f"**Average Items per Day:** {average_items:.2f}")
fig_items_by_date = px.line(x=items_by_date.index, y=items_by_date.values, labels={'x': 'Date', 'y': 'Number of Items'},
                            title="Number of Items per Day")
st.plotly_chart(fig_items_by_date)

# 4. Review Score Chart 
st.header("⭐ Review Score")
if 'review_score' in filtered_data.columns:
    review_scores = filtered_data['review_score'].dropna()
    average_review_score = review_scores.mean()
    most_common_review_score = review_scores.mode()[0]

    st.write(f"**Average Review Score:** {average_review_score:.2f}")
    st.write(f"**Most Common Review Score:** {most_common_review_score}")
    
    fig_review_score = px.histogram(review_scores, nbins=5, labels={'value': 'Review Score', 'count': 'Frequency'},
                                    title="Review Score Distribution",
                                    color_discrete_sequence=['#636EFA'])  # Custom color for better readability
    fig_review_score.update_layout(bargap=0.2, xaxis_title='Review Score', yaxis_title='Count')
    st.plotly_chart(fig_review_score)
else:
    st.write("Review score data not available.")

# 5. Customer Demographics by State 
st.header("📊 Customer Demographics by State")
customer_by_state = filtered_data.groupby('customer_state').size()

fig_customer_state = px.bar(x=customer_by_state.index, y=customer_by_state.values, 
                            labels={'x': 'State', 'y': 'Number of Customers'},
                            title="Customer Distribution by State",
                            color_discrete_sequence=['#FF7F0E'])  # Using orange for better contrast
fig_customer_state.update_layout(xaxis_title='State', yaxis_title='Number of Customers')
st.plotly_chart(fig_customer_state)

# 6. Best-Selling Products
st.header("🏆 Best-Selling Products")
if 'product_category_name_english' in filtered_data.columns:
    product_sales = filtered_data.groupby('product_category_name_english').size().sort_values(ascending=False).head(10)

    fig_product_sales = px.bar(x=product_sales.index, y=product_sales.values, 
                               labels={'x': 'Product Category', 'y': 'Number of Sales'},
                               title="Top 10 Best-Selling Products",
                               color_discrete_sequence=px.colors.qualitative.Vivid)
    fig_product_sales.update_layout(xaxis_title='Product Category', yaxis_title='Number of Sales', xaxis_tickangle=-45)
    st.plotly_chart(fig_product_sales)
else:
    st.write("Product category data not available.")


st.markdown("**Developer:** Adriel Fabian Suryoto")  
st.markdown("© 2024 All Rights Reserved") 