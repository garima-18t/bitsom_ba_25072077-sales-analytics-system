# Import the read_sales_data function from file_handler
# This function reads the sales data file and handles encoding issues
# Import the function to parse and clean the raw sales data

from utils.file_handler import read_sales_data
from utils.file_handler import parse_transactions

# Validate and optionally filter transactions
from utils.file_handler import validate_and_filter

# Call the function to read the sales data file
# The file should be present in the project root directory

data = read_sales_data("sales_data.txt")

# Print the total number of records read from the file

print("Total records read:", len(data))

# Print the first 3 records to verify the output

print("First 3 records:")
for record in data[:3]:
    print(record)

raw_data = read_sales_data("sales_data.txt")
clean_data = parse_transactions(raw_data)

print("Parsed records:", len(clean_data))
print(clean_data[0])

raw_lines = read_sales_data("sales_data.txt")
parsed_data = parse_transactions(raw_lines) 

# Apply validation and filtering
valid_data, invalid_count, summary = validate_and_filter(
    parsed_data,
    region="North",
    min_amount=1000
)

# Display results
print("\nInvalid transactions:", invalid_count)
print("Summary:", summary)
print("Final valid records:", len(valid_data))


from utils.data_processor import calculate_total_revenue

total_revenue = calculate_total_revenue(valid_data)
print("Total Revenue:", total_revenue)


from utils.data_processor import region_wise_sales

# Validation ONLY (no filters)
valid_data, invalid_count, summary = validate_and_filter(parsed_data)

region_summary = region_wise_sales(valid_data)

print("\nRegion-wise Sales Summary:")
for region, stats in region_summary.items():
    print(region, "->", stats)


from utils.data_processor import top_selling_products

top_products = top_selling_products(valid_data)

print("\nTop Selling Products:")
for product in top_products:
    print(product)

from utils.data_processor import customer_analysis

customer_summary = customer_analysis(valid_data)

print("\nCustomer Purchase Analysis:")
for customer, stats in customer_summary.items():
    print(customer, "->", stats)

from utils.data_processor import daily_sales_trend

daily_trends = daily_sales_trend(valid_data)

print("\nDaily Sales Trend:")
for date, stats in daily_trends.items():
    print(date, "->", stats)

from utils.data_processor import find_peak_sales_day

peak_day = find_peak_sales_day(valid_data)

print("\nPeak Sales Day:")
print(peak_day)


from utils.data_processor import low_performing_products

low_products = low_performing_products(valid_data, threshold=10)

print("\nLow Performing Products:")
for product in low_products:
    print(product)

from utils.api_handler import fetch_all_products

products = fetch_all_products()

print("Number of products fetched:", len(products))

if products:
    print("Sample product:")
    print(products[0])


from utils.api_handler import fetch_all_products, create_product_mapping

products = fetch_all_products()
product_map = create_product_mapping(products)

print("\nProduct Mapping Sample:")
print(list(product_map.items())[0])


from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

# Fetch API products
api_products = fetch_all_products()

# Create product mapping
product_mapping = create_product_mapping(api_products)

# Enrich transactions
enriched_data = enrich_sales_data(valid_data, product_mapping)

# Save enriched data to file
save_enriched_data(enriched_data)

from utils.report_generator import generate_sales_report

generate_sales_report(valid_data, enriched_data)



