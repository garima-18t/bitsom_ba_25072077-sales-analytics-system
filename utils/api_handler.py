#----------Task 3.1: Fetch Product Details----------

#--a)Fetch all products--

import requests


def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        # Send request to API
        response = requests.get(url)
        response.raise_for_status()  # Raises error for bad status codes

        # Convert response to JSON
        data = response.json()

        print("Successfully fetched products from API")

        # Return list of products
        return data.get("products", [])

    except requests.exceptions.RequestException as e:
        print("Failed to fetch products from API:", e)
        return []


#--b)Create Product Mapping--

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    """

    product_mapping = {}

    for product in api_products:
        product_id = product.get('id')

        product_mapping[product_id] = {
            'title': product.get('title'),
            'category': product.get('category'),
            'brand': product.get('brand'),
            'rating': product.get('rating')
        }

    return product_mapping


#----------Task 3.2: Enrich Sales Data----------

#---This function should enrich your transaction data AND save it back to a new file---

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """

    enriched_transactions = []

    for tx in transactions:
        enriched_tx = tx.copy()

        try:
            # Extract numeric ID from ProductID (P101 -> 101)
            product_id_str = tx.get("ProductID", "")
            numeric_id = int(product_id_str.replace("P", ""))

            if numeric_id in product_mapping:
                api_info = product_mapping[numeric_id]

                enriched_tx["API_Category"] = api_info["category"]
                enriched_tx["API_Brand"] = api_info["brand"]
                enriched_tx["API_Rating"] = api_info["rating"]
                enriched_tx["API_Match"] = True
            else:
                enriched_tx["API_Category"] = None
                enriched_tx["API_Brand"] = None
                enriched_tx["API_Rating"] = None
                enriched_tx["API_Match"] = False

        except Exception:
            enriched_tx["API_Category"] = None
            enriched_tx["API_Brand"] = None
            enriched_tx["API_Rating"] = None
            enriched_tx["API_Match"] = False

        enriched_transactions.append(enriched_tx)

    return enriched_transactions

#---Helper function---

import os


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    """

    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as file:
        # Write header
        header = [
            "TransactionID", "Date", "ProductID", "ProductName",
            "Quantity", "UnitPrice", "CustomerID", "Region",
            "API_Category", "API_Brand", "API_Rating", "API_Match"
        ]
        file.write("|".join(header) + "\n")

        # Write rows
        for tx in enriched_transactions:
            row = [
                str(tx.get("TransactionID")),
                str(tx.get("Date")),
                str(tx.get("ProductID")),
                str(tx.get("ProductName")),
                str(tx.get("Quantity")),
                str(tx.get("UnitPrice")),
                str(tx.get("CustomerID")),
                str(tx.get("Region")),
                str(tx.get("API_Category") or ""),
                str(tx.get("API_Brand") or ""),
                str(tx.get("API_Rating") or ""),
                str(tx.get("API_Match"))
            ]

            file.write("|".join(row) + "\n")

    print(f"Enriched sales data saved to {filename}")


