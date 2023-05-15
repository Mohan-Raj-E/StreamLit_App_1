import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def get_insight(merged_df):
    import streamlit as st
    st.markdown("**1. Monthwise Order Counts**")

    # convert 'Created At' column to datetime format
    merged_df['Created At'] = pd.to_datetime(merged_df['Created At'])
    # group by month of 'Created At' column and count 'Order' column
    order_count_month = merged_df.groupby(merged_df['Created At'].dt.month)['Order'].count()

    # create a line plot using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=order_count_month.index, y=order_count_month.values, mode='lines',
                             line=dict(color='blue', width=2)))

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

    st.plotly_chart(fig)

    st.markdown(
        "The graph illustrates the order counts for each month, revealing a consistent growth trend from the 2nd to the 9th month. Notably, the peak of order numbers occurred in the 8th month, followed by a decline from the 9th month. This information indicates the varying order volumes throughout the analyzed period.\n")

    st.markdown("**Order Count by Month:**")
    st.write(order_count_month.to_string(), "\n")

    st.markdown("**2. Top Ten Products**")

    # Create a Plotly bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=merged_df["Lineitem name"].value_counts().index[:10],
                         y=merged_df["Lineitem name"].value_counts().values[:10],
                         text=merged_df["Lineitem name"].value_counts().values[:10],
                         textposition='auto'))
    fig.update_layout(
        title={
            'text': "Top 10 Products",
            'font': {'size': 24},
            'x': 0.5,
            'xanchor': 'center'},
        xaxis_title='Product',
        yaxis_title='Count'
    )

    # Display the bar chart using Streamlit
    st.plotly_chart(fig)

    # Display top 10 products as a table
    top_products = merged_df["Lineitem name"].value_counts().nlargest(10).reset_index()
    top_products.columns = ['Product', 'Count']

    st.write(
        "The chart showcases the top 10 products that have been sold and purchased by customers. These products have gained significant popularity and demand among the customer base. It is essential to closely monitor these top-selling items as they contribute significantly to the overall sales and customer satisfaction.\n")
    st.write("Top 10 Products:")
    #st.write(top_products.to_string(index=False))
    for rank, (index, row) in enumerate(top_products.iterrows(), start=1):
        product = row['Product']
        count = row['Count']
        st.write(f"Rank: {rank}, Product: {product}, Count: {count}\n")


    st.markdown("**3. Orders Max and Min based on Date and Time**")
    # convert the 'Created At' column to datetime type
    merged_df['Created At'] = pd.to_datetime(merged_df['Created At'])

    # extract the date and time parts of the timestamp in the 'Created At' column
    merged_df['Date'] = merged_df['Created At'].dt.date
    merged_df['Time'] = merged_df['Created At'].dt.time

    st.write("\nDate Wise\n")

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
    layout = go.Layout(title={
            'text': "Number of Orders per Day",
            'font': {'size': 24},
            'x': 0.5,
            'xanchor': 'center'}, xaxis_title='Date', yaxis_title='Number of Orders')

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
    st.plotly_chart(fig)

    st.write(
        "The chart provides insights into the distribution of orders across various dates. It enables us to identify the dates with the highest and lowest number of orders. This information is valuable in understanding customer behavior and planning business strategies accordingly. By analyzing the patterns and trends in order volumes, we can optimize operations and allocate resources effectively to meet customer demands on high-order dates and identify opportunities for improvement on low-order dates.")

    st.write(
        f"The dates with the most orders are {orders_Per_Day[max_indexes].index.to_list()} with {max_value} orders")

    st.write(
        f"The dates with the fewest orders are {orders_Per_Day[min_indexes].index.to_list()} with {min_value} orders")

    # Time Wise
    orders_Per_Time = merged_df.groupby(['Time'])['Order'].count()

    # Find the time with the highest orders
    max_Time = orders_Per_Time.idxmax()

    # Find the time with the lowest orders
    min_Time = orders_Per_Time.idxmin()

    # Create a trace
    trace = go.Scatter(x=orders_Per_Time.index, y=orders_Per_Time.values, mode='lines', name='Number of Orders')

    # Create a layout
    layout = go.Layout(title={
            'text': "Number of Orders as per Time",
            'font': {'size': 24},
            'x': 0.5,
            'xanchor': 'center'}, xaxis_title='Time', yaxis_title='Number of Orders')

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

    # Add green dots for maximum values and top 10 values
    for time, value in top_10.items():
        fig.add_trace(go.Scatter(x=[time], y=[value], mode='markers', marker=dict(color='Green', size=10)))

    # Add blue dot for minimum value
    fig.add_trace(go.Scatter(x=[min_Time], y=[min_value], mode='markers', marker=dict(color='blue', size=10)))

    # Show the figure
    st.plotly_chart(fig)

    st.write(
        "The chart shows when we receive the most and least orders during different times of the day. This helps us plan our operations effectively, allocate resources, and optimize order processing. By understanding customer ordering patterns, we can improve efficiency and boost sales by targeting promotions and marketing efforts during slower periods.")

    st.write(f"The Time with the most orders is {max_Time} with {orders_Per_Time[max_Time]} orders")
    st.write("Time Stamps that have the maximum Orders", orders_Per_Time[max_indexes].index.to_list())
    st.write(f"The Time with the fewest orders is {min_Time} with {orders_Per_Time[min_Time]} orders")
    st.write("Time Stamps that have the minimum Orders", len(min_indexes),'\n')

    st.markdown("**4. Per Order: Number of Itemse**")

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
    trace_top_10 = go.Scatter(x=top_10.index, y=top_10.values, mode='markers+text', text=top_10.values,
                              textposition='top center', marker=dict(color='red', size=10), name='Top 10 Orders')

    # Create a layout
    layout = go.Layout(title={'text': "Number of Items per Order",
                                'font': {'size': 24},
                                'x': 0.5,
                                'xanchor': 'center'}, xaxis_title='Order', yaxis_title='Number of Items')


    # Create a figure
    fig = go.Figure(data=[trace_items, trace_top_10], layout=layout)

    # Show the figure
    st.plotly_chart(fig)

    st.write(
        "The chart displays the number of items per order. It provides insights into the distribution of items across orders, allowing us to understand the average number of items per order and identify orders with the highest and lowest item counts.")

    # Print the order with the most items, the order with the fewest items, and the average number of items per order
    st.write(f"The order with the most items is {max_Items_Per_Order} with {Items_Per_Order.max()} items")
    st.write(f"The order with the fewest items is {min_Items_Per_Order} with {Items_Per_Order.min()} items")
    st.write(f"The average number of items per order is {mean_Items_Per_Order:.2f}\n")

    st.markdown("**5. Average Value per Order**")
    import streamlit as st

    ## Average Value per Order
    AVG_Value_Orders = merged_df.groupby('Order').agg({'Amount': 'mean', 'Lineitem quantity': 'sum'}).reset_index()
    order_with_max_amount = \
    AVG_Value_Orders.loc[AVG_Value_Orders['Amount'] == AVG_Value_Orders['Amount'].max(), 'Order'].values[0]
    order_with_min_amount = \
    AVG_Value_Orders.loc[AVG_Value_Orders['Amount'] == AVG_Value_Orders['Amount'].min(), 'Order'].values[0]

    st.write("Maximum Amount order id:", order_with_max_amount, " Amount: ", AVG_Value_Orders['Amount'].max())
    st.write("Minimum Amount order id:", order_with_min_amount, " Amount: ", AVG_Value_Orders['Amount'].min())
    st.write("Average Amount:", AVG_Value_Orders['Amount'].mean())

    st.write(
        "This information gives us the maximum order amount, minimum order amount, and the average order amount. It helps us understand the range of order values and the typical spending patterns of customers. By analyzing these metrics, we can identify high-value orders, low-value orders, and determine the average transaction value. This knowledge is valuable in pricing strategies.")

    st.markdown("**6. Return Customer %**")

    merged_df = merged_df.rename(columns={
        merged_df.columns[15]: 'OrderExport_Created_at',
        merged_df.columns[-7]: 'Transactions_Created_at'})
    cancelled_orders = merged_df[merged_df['Cancelled at'].notnull()]
    cancelled_orders = cancelled_orders.groupby('Order').first().reset_index()
    not_cancelled_orders = merged_df[merged_df['Cancelled at'].isnull()]
    not_cancelled_orders = not_cancelled_orders.groupby('Order').first().reset_index()

    total_orders = len(cancelled_orders) + len(not_cancelled_orders)
    cancellation_rate = len(cancelled_orders) / total_orders

    # Create a bar plot
    bar_data = {
        'Category': ['Total Orders', 'Not Cancelled Orders', 'Cancelled Orders'],
        'Count': [total_orders, len(not_cancelled_orders), len(cancelled_orders)]
    }

    fig = go.Figure(
        data=[go.Bar(x=bar_data['Category'], y=bar_data['Count'], text=bar_data['Count'], textposition='auto')])
    fig.update_layout(title={'text': "Order Cancellation Statistics",
                                'font': {'size': 24},
                                'x': 0.5,
                                'xanchor': 'center'})

    # Show the figure
    st.plotly_chart(fig)

    st.write(f"Total Orders: {total_orders}")
    st.write(f"Not Cancelled Orders: {len(not_cancelled_orders)}")
    st.write(f"Cancelled Orders: {len(cancelled_orders)}")
    st.write(f"The Cancellation customer rate is {cancellation_rate:.2%}")

    st.write(
        "This information provides us with the total number of orders, the number of cancelled orders, the number of not cancelled orders, and the cancellation customer rate. It helps us understand the overall order volume and the percentage of orders that were cancelled. By analyzing these metrics, we can evaluate the effectiveness of our order management and customer service processes.")

def main():
    st.title("Gulabs Yearly Report Analysis")

    # Step 1: Upload Transaction CSV
    transaction_file = st.file_uploader("Upload Transaction CSV")

    # Step 1: Upload Order Export CSV
    order_file = st.file_uploader("Upload Order Export CSV")

    if transaction_file is not None and order_file is not None:
        # Read CSV files
        transactions_export = pd.read_csv(transaction_file)
        orders_export = pd.read_csv(order_file)

        # Merge dataframes
        merged_df = pd.merge(orders_export, transactions_export, on="Name")

        # Step 2: Display "Get Insight" button
        if st.button("Get Insight"):
            # Step 3: Call get_insight() function and display the output
            get_insight(merged_df)
            # st.write(insights)


if __name__ == "__main__":
    main()
