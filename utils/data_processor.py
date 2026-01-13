#----------Task 2.1: Sales Summary Calculator----------

#--a)Calculate Total Revenue--

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.

    Parameters:
        transactions (list): List of transaction dictionaries

    Returns:
        float: Total revenue calculated as
               sum of (Quantity * UnitPrice) for all transactions
    """

    total_revenue = 0.0

    # Loop through each transaction
    for tx in transactions:
        # Calculate revenue for one transaction
        transaction_revenue = tx['Quantity'] * tx['UnitPrice']

        # Add to total revenue
        total_revenue += transaction_revenue

    return total_revenue

#--b)Region-wise Sales Anaysis--

def region_wise_sales(transactions):
    """
    Analyzes sales by region.

    Parameters:
        transactions (list): List of valid transaction dictionaries

    Returns:
        dict: Region-wise sales statistics sorted by total sales (descending)
    """

    region_stats = {}
    overall_total = 0.0

    # Step 1: Calculate total sales per region and overall total
    for tx in transactions:
        region = tx['Region']
        amount = tx['Quantity'] * tx['UnitPrice']

        overall_total += amount

        # Initialize region entry if not present
        if region not in region_stats:
            region_stats[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        # Update region totals
        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1

    # Step 2: Calculate percentage of total sales for each region
    for region in region_stats:
        percentage = (region_stats[region]['total_sales'] / overall_total) * 100
        region_stats[region]['percentage'] = round(percentage, 2)

    # Step 3: Sort regions by total_sales in descending order
    sorted_regions = dict(
        sorted(
            region_stats.items(),
            key=lambda item: item[1]['total_sales'],
            reverse=True
        )
    )

    return sorted_regions

#--c)Top Selling Products--

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples
    (ProductName, TotalQuantity, TotalRevenue)
    """

    product_summary = {}

    # Step 1: Aggregate quantity and revenue per product
    for tx in transactions:
        product = tx['ProductName']
        quantity = tx['Quantity']
        revenue = quantity * tx['UnitPrice']

        if product not in product_summary:
            product_summary[product] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_summary[product]['total_quantity'] += quantity
        product_summary[product]['total_revenue'] += revenue

    # Step 2: Convert dictionary to list of tuples
    product_list = [
        (product,
         data['total_quantity'],
         data['total_revenue'])
        for product, data in product_summary.items()
    ]

    # Step 3: Sort by total quantity (descending)
    product_list.sort(key=lambda x: x[1], reverse=True)

    # Step 4: Return top n products
    return product_list[:n]

#--d)Customer Purchase Analysis--

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics
    """

    customer_data = {}

    # Step 1: Aggregate data per customer
    for tx in transactions:
        customer_id = tx['CustomerID']
        product = tx['ProductName']
        amount = tx['Quantity'] * tx['UnitPrice']

        if customer_id not in customer_data:
            customer_data[customer_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }

        customer_data[customer_id]['total_spent'] += amount
        customer_data[customer_id]['purchase_count'] += 1
        customer_data[customer_id]['products_bought'].add(product)

    # Step 2: Calculate average order value and convert sets to lists
    for customer in customer_data:
        total = customer_data[customer]['total_spent']
        count = customer_data[customer]['purchase_count']

        customer_data[customer]['avg_order_value'] = round(total / count, 2)
        customer_data[customer]['products_bought'] = list(
            customer_data[customer]['products_bought']
        )

    # Step 3: Sort customers by total_spent (descending)
    sorted_customers = dict(
        sorted(
            customer_data.items(),
            key=lambda item: item[1]['total_spent'],
            reverse=True
        )
    )

    return sorted_customers

#----------Task 2.2: Date-based Analysis----------

#--a)Daily Sales Trend--

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns: dictionary sorted by date
    """

    daily_data = {}

    # Step 1: Aggregate data by date
    for tx in transactions:
        date = tx['Date']
        revenue = tx['Quantity'] * tx['UnitPrice']
        customer = tx['CustomerID']

        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()
            }

        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['unique_customers'].add(customer)

    # Step 2: Convert customer sets to counts
    for date in daily_data:
        daily_data[date]['unique_customers'] = len(
            daily_data[date]['unique_customers']
        )

    # Step 3: Sort dictionary by date (chronologically)
    sorted_daily_data = dict(sorted(daily_data.items()))

    return sorted_daily_data

#--b)Find Peak Sales day--

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns: tuple (date, revenue, transaction_count)
    """

    daily_summary = {}

    # Step 1: Aggregate revenue and transaction count per date
    for tx in transactions:
        date = tx['Date']
        revenue = tx['Quantity'] * tx['UnitPrice']

        if date not in daily_summary:
            daily_summary[date] = {
                'revenue': 0.0,
                'transaction_count': 0
            }

        daily_summary[date]['revenue'] += revenue
        daily_summary[date]['transaction_count'] += 1

    # Step 2: Find date with maximum revenue
    peak_date = max(
        daily_summary.items(),
        key=lambda item: item[1]['revenue']
    )

    # Step 3: Return required tuple
    return (
        peak_date[0],
        peak_date[1]['revenue'],
        peak_date[1]['transaction_count']
    )

#----------Task 2.3: Product Performance----------

#--a)Low Performing Products--

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns: list of tuples
    (ProductName, TotalQuantity, TotalRevenue)
    """

    product_summary = {}

    # Step 1: Aggregate quantity and revenue per product
    for tx in transactions:
        product = tx['ProductName']
        quantity = tx['Quantity']
        revenue = quantity * tx['UnitPrice']

        if product not in product_summary:
            product_summary[product] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_summary[product]['total_quantity'] += quantity
        product_summary[product]['total_revenue'] += revenue

    # Step 2: Filter products below threshold
    low_products = [
        (product,
         data['total_quantity'],
         data['total_revenue'])
        for product, data in product_summary.items()
        if data['total_quantity'] < threshold
    ]

    # Step 3: Sort by total quantity (ascending)
    low_products.sort(key=lambda x: x[1])

    return low_products


