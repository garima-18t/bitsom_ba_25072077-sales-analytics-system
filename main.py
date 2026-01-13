from utils.file_handler import read_sales_data
from utils.file_handler import parse_transactions
from utils.file_handler import validate_and_filter

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

from utils.report_generator import generate_sales_report


def main():
    """
    Main execution function
    """

    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # 1. Read sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # 2. Parse and clean
        print("\n[2/10] Parsing and cleaning data...")
        parsed_transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_transactions)} records")

        # 3. Display filter options
        print("\n[3/10] Filter Options Available:")
        regions = sorted(set(tx['Region'] for tx in parsed_transactions if tx.get('Region')))
        print("Regions:", ", ".join(regions))

        amounts = [tx['Quantity'] * tx['UnitPrice'] for tx in parsed_transactions]
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        apply_filter = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region_filter = None
        min_amount = None
        max_amount = None

        if apply_filter == 'y':
            region_filter = input("Enter region (or press Enter to skip): ").strip() or None

            min_amt = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_amt = input("Enter maximum amount (or press Enter to skip): ").strip()

            min_amount = float(min_amt) if min_amt else None
            max_amount = float(max_amt) if max_amt else None

        # 4. Validate and filter
        print("\n[4/10] Validating transactions...")
        valid_data, invalid_count, summary = validate_and_filter(
            parsed_transactions,
            region=region_filter,
            min_amount=min_amount,
            max_amount=max_amount
        )

        print(f"✓ Valid: {len(valid_data)} | Invalid: {invalid_count}")

        # 5. Analysis
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_data)
        region_wise_sales(valid_data)
        top_selling_products(valid_data)
        customer_analysis(valid_data)
        daily_sales_trend(valid_data)
        find_peak_sales_day(valid_data)
        low_performing_products(valid_data)
        print("✓ Analysis complete")

        # 6. Fetch API products
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # 7. Enrich sales data
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_data = enrich_sales_data(valid_data, product_mapping)

        enriched_count = sum(1 for tx in enriched_data if tx.get("API_Match"))
        success_rate = (enriched_count / len(enriched_data)) * 100 if enriched_data else 0
        print(f"✓ Enriched {enriched_count}/{len(enriched_data)} transactions ({success_rate:.1f}%)")

        # 8. Save enriched data
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_data)
        print("✓ Saved to: data/enriched_sales_data.txt")

        # 9. Generate report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_data, enriched_data)
        print("✓ Report saved to: output/sales_report.txt")

        # 10. Done
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ An error occurred:")
        print(str(e))
        print("Please check inputs or files and try again.")


if __name__ == "__main__":
    main()
