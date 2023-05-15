#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import streamlit as st
# Define the function that will process the merged CSV file
import numpy as np
import plotly.graph_objects as go
from IPython.display import display

## orders/month
def get_insight(merged_df):
    
    print("1. Monthwise Order Counts\n")
    # convert 'Created At' column to datetime format
    merged_df['Created At'] = pd.to_datetime(merged_df['Created At'])
    # group by month of 'Created At' column and count 'Order' column
    order_count_month = merged_df.groupby(merged_df['Created At'].dt.month)['Order'].count()

    # create a line plot using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=order_count_month.index, y=order_count_month.values, mode='lines',line=dict(color='blue', width=2)))

    fig.update_layout(
        title={
            'text': "Order Count by Month",
            'font': {'size': 24},
            'x': 0.5,
            'xanchor': 'center'},
        xaxis_title="Month",
        yaxis_title="Order Count"
    )

    # mark max value
    max_idx = order_count_month.idxmax()
    fig.add_annotation(x=max_idx, y=order_count_month[max_idx], text=f'Max: {order_count_month[max_idx]}', 
                       showarrow=True, arrowhead=1, ax=-50)

    # mark min value
    min_idx = order_count_month.idxmin()
    fig.add_annotation(x=min_idx, y=order_count_month[min_idx], text=f'Min: {order_count_month[min_idx]}', 
                       showarrow=True, arrowhead=1, ax=50)

    fig.show()

    print("Order Count by Month:\n")
    #print(order_count_month,'\n\n')
    display(order_count_month)
    print("Maximum: Month =",order_count_month.idxmax()," Value =",order_count_month.max())
    print("Minimum: Month =",order_count_month.idxmin()," Value =",order_count_month.min())


    print("\n\n\n2. Top Ten Products")
    # 2. Top Ten Products
    # create a Plotly bar chart
    # create a Plotly bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=merged_df["Lineitem name"].value_counts().index[:10], 
                         y=merged_df["Lineitem name"].value_counts().values[:10],
                         text=merged_df["Lineitem name"].value_counts().values[:10],
                         textposition='auto'))
    fig.update_layout(
        title='Top 10 Products',
        xaxis_title='Product',
        yaxis_title='Count'
    )
    fig.show()

    # display top 10 products as a table
    top_products = merged_df["Lineitem name"].value_counts().nlargest(10).reset_index()
    top_products.columns = ['Product', 'Count']
    print("Top 10 Products:\n", top_products.to_string(index=False))

    
    print("\n\n\n3. Orders Max and Min based on Date and Time")

    # convert the 'Created At' column to datetime type
    merged_df['Created At'] = pd.to_datetime(merged_df['Created At'])

    # extract the date and time parts of the timestamp in the 'Created At' column
    merged_df['Date'] = merged_df['Created At'].dt.date
    merged_df['Time'] = merged_df['Created At'].dt.time
    print("\nDate Wise\n")
    # Date Wise
    orders_Per_Day = merged_df.groupby(['Date'])['Order'].count()

    # Find the maximum and minimum values
    max_value = orders_Per_Day.max()
    min_value = orders_Per_Day.min()

    # Find the indexes where the value is equal to the maximum or minimum value
    max_indexes = np.where(orders_Per_Day.values == max_value)[0]
    min_indexes = np.where(orders_Per_Day.values == min_value)[0]

    # Create a trace
    trace = go.Scatter(x=orders_Per_Day.index, y=orders_Per_Day.values, mode='lines', name='Number of Orders')

    # Create a layout
    layout = go.Layout(title='Number of Orders per Day', xaxis_title='Date', yaxis_title='Number of Orders')

    # Create a figure
    fig = go.Figure(data=[trace], layout=layout)

    # Add red dots for maximum values
    for idx in max_indexes:
        date = orders_Per_Day.index[idx]
        fig.add_trace(go.Scatter(x=[date], y=[max_value], mode='markers', marker=dict(color='green', size=10)))

    # Add blue dots for minimum values
    for idx in min_indexes:
        date = orders_Per_Day.index[idx]
        fig.add_trace(go.Scatter(x=[date], y=[min_value], mode='markers', marker=dict(color='Red', size=10)))

    # Show the figure
    fig.show()
    
    print(f"The dates with the most orders are {orders_Per_Day[max_indexes].index.to_list()} with {max_value} orders")
    print(f"The dates with the fewest orders are {orders_Per_Day[min_indexes].index.to_list()} with {min_value} orders")
    print("\nTime Wise\n")
    # Time Wise
    orders_Per_Time = merged_df.groupby(['Time'])['Order'].count()
    # Find the date with the highest orders
    max_Time = orders_Per_Time.idxmax()

    # Find the date with the lowest orders
    min_Time = orders_Per_Time.idxmin()
    # Create a trace
    trace = go.Scatter(x=orders_Per_Time.index, y=orders_Per_Time.values, mode='lines', name='Number of Orders')

    # Create a layout
    layout = go.Layout(title='Number of Orders as per Time', xaxis_title='Time', yaxis_title='Number of Orders')

    # Create a figure
    fig = go.Figure(data=[trace], layout=layout)

    # Add annotations for the maximum and minimum values
    max_value = max(orders_Per_Time.values)
    min_value = min(orders_Per_Time.values)

    # Find the indexes with the highest orders
    max_indexes = [i for i, x in enumerate(orders_Per_Time.values) if x == max_value]

    # Find the indexes with the lowest orders
    min_indexes = [i for i, x in enumerate(orders_Per_Time.values) if x == min_value]

    top_10 = orders_Per_Time.sort_values(ascending=False)[:15]
    # Add red dots for maximum values
    for idx in max_indexes:
        time = orders_Per_Time.index[idx]
        fig.add_trace(go.Scatter(x=[time], y=[max_value], mode='markers', marker=dict(color='Green', size=10)))
    # Add red dots for top 10 values
    for time, value in top_10.items():
        fig.add_trace(go.Scatter(x=[time], y=[value], mode='markers', marker=dict(color='Green', size=10)))

    # Add blue dot for minimum value
    min_time = orders_Per_Time.idxmin()
    fig.add_trace(go.Scatter(x=[min_time], y=[min_value], mode='markers', marker=dict(color='blue', size=10)))

    # Show the figure
    fig.show()

    print(f"The Time with the most orders is {max_Time} with {orders_Per_Time[max_Time]} orders")
    print("Time Stamps that has the maximum Orders",orders_Per_Time[max_indexes].index.to_list())
    print(f"The Time with the fewest orders is {min_Time} with {orders_Per_Time[min_Time]} orders")
    print("Time Stamps that has the minimum Orders",len(min_indexes))

    
    print("\n\n\n4. Per Order: Number of Items\n")

    # Group the data by order and count the number of items per order
    Items_Per_Order = merged_df.groupby('Order')['Lineitem name'].count()
    # Find the order with the most items
    max_Items_Per_Order = Items_Per_Order.idxmax()
    # Find the order with the fewest items
    min_Items_Per_Order = Items_Per_Order.idxmin()
    # Find the average number of items per order
    mean_Items_Per_Order = Items_Per_Order.mean()
    # Sort the orders by number of items and get the top 10
    top_10 = Items_Per_Order.sort_values(ascending=False)[:10]
    # Create a trace for the number of items per order
    trace_items = go.Scatter(x=Items_Per_Order.index, y=Items_Per_Order.values, mode='lines', name='Number of Items')
    # Create a trace for the top 10 orders
    trace_top_10 = go.Scatter(x=top_10.index, y=top_10.values, mode='markers+text', text=top_10.values, textposition='top center', marker=dict(color='red', size=10), name='Top 10 Orders')
    # Create a layout
    layout = go.Layout(title='Number of Items per Order', xaxis_title='Order', yaxis_title='Number of Items')
    # Create a figure
    fig = go.Figure(data=[trace_items, trace_top_10], layout=layout)
    # Show the figure
    fig.show()

    # Print the order with the most items, the order with the fewest items, and the average number of items per order
    print(f"The order with the most items is {max_Items_Per_Order} with {Items_Per_Order.max()} items")
    print(f"The order with the fewest items is {min_Items_Per_Order} with {Items_Per_Order.min()} items")
    print(f"The average number of items per order is {mean_Items_Per_Order:.2f}\n\n")



    print("\n\n\n5. Average Value per Order")
    ## Average Value per Order
    AVG_Value_Orders = merged_df.groupby('Order').agg({'Amount': 'mean', 'Lineitem quantity': 'sum'}).reset_index()
    order_with_max_amount = AVG_Value_Orders.loc[AVG_Value_Orders['Amount'] == AVG_Value_Orders['Amount'].max(), 'Order'].values[0]
    order_with_min_amount = AVG_Value_Orders.loc[AVG_Value_Orders['Amount'] == AVG_Value_Orders['Amount'].min(), 'Order'].values[0]

    # Before Removing the outliers
    print("\nMaximum Amount order id:", order_with_max_amount, " Amount: ", AVG_Value_Orders['Amount'].max())
    print("Minimum Amount order id:", order_with_min_amount, " Amount:", AVG_Value_Orders['Amount'].min())
    print("Average Amount", AVG_Value_Orders['Amount'].mean())
    
    print("\n\n\n6. return customer %")
    cancelled_orders = merged_df[merged_df['Cancelled at'].notnull()]
    not_cancelled_orders = merged_df[merged_df['Cancelled at'].isnull()]

    total_orders = len(cancelled_orders) + len(not_cancelled_orders)
    cancellation_rate = len(cancelled_orders) / total_orders
    print(f"The return customer rate is {cancellation_rate:.2%}")


# Define the Streamlit app
def main():
    # Set the title of the app
    st.title("CSV File Merger")

    # Allow users to upload two CSV files
    st.header("Upload CSV Files")
    uploaded_file1 = st.file_uploader("Choose a CSV file for the first dataset", type="csv")
    uploaded_file2 = st.file_uploader("Choose a CSV file for the second dataset", type="csv")

    # Merge the CSV files and pass them to the processing function when the user clicks the button
    if st.button("Get Insights"):
        if uploaded_file1 is not None and uploaded_file2 is not None:
            # Read the CSV files into DataFrames
            df1 = pd.read_csv(uploaded_file1)
            df2 = pd.read_csv(uploaded_file2)

            merged_df = pd.merge(df2, df1, on="Name")
            merged_df = merged_df.rename(columns={
                merged_df.columns[15]: 'OrderExport_Created_at',
                merged_df.columns[-7]: 'Transactions_Created_at'
            })

            # Call the processing function
            #mean_values = process_csv(merged_df)

            # Display the results
            st.header("Results")
            st.write(get_insight(merged_df))
        else:
            st.warning("Please upload two CSV files.")

# Run the app
if _name_ == "_main_":
    main()

