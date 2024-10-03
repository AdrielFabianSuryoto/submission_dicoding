import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np

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


# Question 1: Top 5 and Bottom 5 Sold Product Categories
st.header("🏆 Top 5 and Bottom 5 Sold Product Categories")

# Check if product category exists in the dataset
if 'product_category_name_english' in filtered_data.columns:
    product_sales = filtered_data.groupby('product_category_name_english').size().sort_values(ascending=False)

    # Top 5 Best-Selling Products
    top_5_best_selling = product_sales.head(5)

    # Bottom 5 Lowest-Selling Products
    bottom_5_lowest_selling = product_sales.tail(5)

    # Create a horizontal bar chart
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plotting top 5
    sns.barplot(y=top_5_best_selling.index, x=top_5_best_selling.values, ax=axes[0], palette='Blues_r')
    axes[0].set_title('Top 5 Sold Products')
    axes[0].set_xlabel('Total Sales')
    axes[0].set_ylabel('Product Category')

    # Plotting bottom 5
    sns.barplot(y=bottom_5_lowest_selling.index, x=bottom_5_lowest_selling.values, ax=axes[1], palette='Oranges_r')
    axes[1].set_title('Bottom 5 Sold Products')
    axes[1].set_xlabel('Total Sales')
    axes[1].set_ylabel('')

    plt.tight_layout()
    st.pyplot(fig)

# Question 2: Average Customer Spending by State with Confidence Interval
# Ensure payment_value and customer_unique_id columns exist in filtered_data
if 'customer_state' in filtered_data.columns and 'price' in filtered_data.columns and 'customer_unique_id' in filtered_data.columns:
    st.header("💰 Average Customer Spending by State")

    # Estimate mean and confidence interval for customers in each state
    customer_regions = filtered_data.groupby('customer_state').agg({
        'price': ['mean', 'std'],  # 'price' column is used for payment value
        'customer_unique_id': 'count'
    }).reset_index()


    
    cis = stats.t.interval(
        0.95, 
        loc=customer_regions['price']['mean'], 
        scale=customer_regions['price']['std'] / np.sqrt(customer_regions['customer_unique_id']['count']), 
        df=customer_regions['customer_unique_id']['count'] - 1
    )

    # Add confidence interval columns
    customer_regions['ci_low'] = cis[0]
    customer_regions['ci_hi'] = cis[1]

    # Function to adjust Matplotlib plot
    def default_plot(ax, spines):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.get_yaxis().set_tick_params(direction='out')
        ax.get_xaxis().set_tick_params(direction='out')
        for loc, spine in ax.spines.items():
            if loc in spines:
                spine.set_position(('outward', 10))
        return ax

    # Sort states for better visualization
    plot = customer_regions.sort_values(by=('price', 'mean'))

    # Plot mean transaction amounts with confidence intervals using Matplotlib
    fig, ax = plt.subplots(figsize=(12, 6))
    ax = default_plot(ax, ['left', 'bottom'])
    plt.xticks(rotation=45)
    plt.xlabel('State')
    plt.ylabel('Mean Spending (95% CI)')
    plt.scatter(plot['customer_state'], plot['price']['mean'], s=100, c=plot['price']['mean'])
    plt.vlines(plot['customer_state'], plot['ci_low'], plot['ci_hi'], lw=0.5)
    plt.title('Average Customer Spending by State with 95% Confidence Interval')
    plt.tight_layout()

    st.pyplot(fig)

else:
    st.write("Data for customer state, price, or unique customer ID is not available.")



st.markdown("**Developer:** Adriel Fabian Suryoto")  
st.markdown("© 2024 All Rights Reserved") 
