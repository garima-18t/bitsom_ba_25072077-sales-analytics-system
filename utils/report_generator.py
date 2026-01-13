from datetime import datetime

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    """

    # Ensure output directory exists
    import os
    os.makedirs("output", exist_ok=True)

    # ---------------- BASIC METRICS ----------------
    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = [tx['Date'] for tx in transactions]
    start_date, end_date = min(dates), max(dates)

    # ---------------- ANALYTICS ----------------
    region_stats = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, 5)
    customers = customer_analysis(transactions)
    daily_trend = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    # API enrichment stats
    enriched_success = [tx for tx in enriched_transactions if tx.get('API_Match')]
    failed_enrichment = [tx['ProductName'] for tx in enriched_transactions if not tx.get('API_Match')]
    success_rate = (len(enriched_success) / len(enriched_transactions)) * 100 if enriched_transactions else 0

    # ---------------- WRITE REPORT ----------------
    with open(output_file, "w", encoding="utf-8") as file:

        # HEADER
        file.write("=" * 44 + "\n")
        file.write("         SALES ANALYTICS REPORT\n")
        file.write(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"   Records Processed: {total_transactions}\n")
        file.write("=" * 44 + "\n\n")

        # OVERALL SUMMARY
        file.write("OVERALL SUMMARY\n")
        file.write("-" * 44 + "\n")
        file.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        file.write(f"Total Transactions:   {total_transactions}\n")
        file.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        file.write(f"Date Range:           {start_date} to {end_date}\n\n")

        # REGION-WISE PERFORMANCE
        file.write("REGION-WISE PERFORMANCE\n")
        file.write("-" * 44 + "\n")
        file.write("Region     Sales        % of Total   Transactions\n")
        for region, stats in region_stats.items():
            file.write(
                f"{region:<10} ₹{stats['total_sales']:>10,.2f}   "
                f"{stats['percentage']:>6.2f}%        {stats['transaction_count']}\n"
            )
        file.write("\n")

        # TOP 5 PRODUCTS
        file.write("TOP 5 PRODUCTS\n")
        file.write("-" * 44 + "\n")
        file.write("Rank  Product Name        Quantity   Revenue\n")
        for i, (name, qty, rev) in enumerate(top_products, start=1):
            file.write(f"{i:<5} {name:<18} {qty:<8} ₹{rev:,.2f}\n")
        file.write("\n")

        # TOP 5 CUSTOMERS
        file.write("TOP 5 CUSTOMERS\n")
        file.write("-" * 44 + "\n")
        file.write("Rank  Customer ID   Total Spent     Orders\n")
        for i, (cid, data) in enumerate(list(customers.items())[:5], start=1):
            file.write(
                f"{i:<5} {cid:<12} ₹{data['total_spent']:>10,.2f}   {data['purchase_count']}\n"
            )
        file.write("\n")

        # DAILY SALES TREND
        file.write("DAILY SALES TREND\n")
        file.write("-" * 44 + "\n")
        file.write("Date         Revenue        Transactions   Customers\n")
        for date, stats in daily_trend.items():
            file.write(
                f"{date}   ₹{stats['revenue']:>10,.2f}        "
                f"{stats['transaction_count']:<5}          {stats['unique_customers']}\n"
            )
        file.write("\n")

        # PRODUCT PERFORMANCE ANALYSIS
        file.write("PRODUCT PERFORMANCE ANALYSIS\n")
        file.write("-" * 44 + "\n")
        file.write(f"Best Selling Day: {peak_day[0]} "
                   f"(₹{peak_day[1]:,.2f}, {peak_day[2]} transactions)\n\n")

        if low_products:
            file.write("Low Performing Products:\n")
            for name, qty, rev in low_products:
                file.write(f"- {name}: {qty} units, ₹{rev:,.2f}\n")
        else:
            file.write("No low performing products.\n")
        file.write("\n")

        # API ENRICHMENT SUMMARY
        file.write("API ENRICHMENT SUMMARY\n")
        file.write("-" * 44 + "\n")
        file.write(f"Total Records Enriched: {len(enriched_success)}\n")
        file.write(f"Success Rate: {success_rate:.2f}%\n")
        if failed_enrichment:
            file.write("Products not enriched:\n")
            for p in set(failed_enrichment):
                file.write(f"- {p}\n")
        else:
            file.write("All products enriched successfully.\n")

    print(f"Sales report generated at {output_file}")
