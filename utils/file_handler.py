#-----Task 1.1: Read Sales Data with Encoding Handling-----

def read_sales_data(filename):
    """
    Reads sales data from a file while handling encoding issues.

    Parameters:
        filename (str): Path to the sales data file ('sales_data.txt')

    Returns:
        list: A list of raw transaction lines as strings
              (header removed, empty lines skipped)
    """

    # List of encodings to try (file may not be UTF-8)
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']

    # Try reading the file using each encoding
    for encoding in encodings_to_try:
        try:
            # Open the file safely using 'with' statement
            # This ensures the file is closed automatically
            with open(filename, 'r', encoding=encoding) as file:
                all_lines = file.readlines()

            # This list will store only valid data lines
            cleaned_lines = []

            # Skip the first line because it is the header
            for line in all_lines[1:]:
                # Remove leading/trailing whitespace and newline characters
                line = line.strip()

                # Ignore empty lines
                if line:
                    cleaned_lines.append(line)

            # If reading was successful, return the data lines
            return cleaned_lines

        except UnicodeDecodeError:
            # If this encoding fails, try the next one
            continue

        except FileNotFoundError:
            # If the file does not exist, show an error message
            print(f"Error: File '{filename}' not found.")
            return []

    # If none of the encodings worked
    print("Error: Unable to read file using supported encodings.")
    return []

#-----Task 1.2: Parse and Clean Data-----

def parse_transactions(raw_lines):
    """
    Parses raw sales data lines into a clean list of dictionaries.

    Parameters:
        raw_lines (list): List of raw transaction strings

    Returns:
        list: List of dictionaries with cleaned and typed data
    """

    transactions = []

    # Loop through each raw line
    for line in raw_lines:
        # Split the line using pipe delimiter
        fields = line.split('|')

        # Skip rows with incorrect number of fields
        if len(fields) != 8:
            continue

        # Unpack fields into variables
        transaction_id = fields[0].strip()
        date = fields[1].strip()
        product_id = fields[2].strip()
        product_name = fields[3].strip()
        quantity = fields[4].strip()
        unit_price = fields[5].strip()
        customer_id = fields[6].strip()
        region = fields[7].strip()

        # Handle commas in ProductName (e.g., "Mouse,Wireless")
        product_name = product_name.replace(',', ' ')

        try:
            # Remove commas from numeric fields and convert types
            quantity = int(quantity.replace(',', ''))
            unit_price = float(unit_price.replace(',', ''))

        except ValueError:
            # Skip rows where conversion fails
            continue

        # Create transaction dictionary
        transaction = {
            'TransactionID': transaction_id,
            'Date': date,
            'ProductID': product_id,
            'ProductName': product_name,
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'CustomerID': customer_id,
            'Region': region
        }

        # Add cleaned transaction to list
        transactions.append(transaction)

    return transactions

#-----Task 1.3: Data Validation and Filtering-----

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.

    Returns:
        tuple: (valid_transactions, invalid_count, filter_summary)
    """

    valid_transactions = []
    invalid_count = 0

    required_fields = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region'
    ]

    # ---------------- VALIDATION ----------------
    for tx in transactions:
        # Check all required fields exist
        if not all(field in tx for field in required_fields):
            invalid_count += 1
            continue

        # Validation rules
        if tx['Quantity'] <= 0:
            invalid_count += 1
            continue

        if tx['UnitPrice'] <= 0:
            invalid_count += 1
            continue

        if not tx['TransactionID'].startswith('T'):
            invalid_count += 1
            continue

        if not tx['ProductID'].startswith('P'):
            invalid_count += 1
            continue

        if not tx['CustomerID'].startswith('C'):
            invalid_count += 1
            continue

        # If all checks pass, add to valid list
        valid_transactions.append(tx)

    # ---------------- DISPLAY OPTIONS ----------------
    regions = sorted({tx['Region'] for tx in valid_transactions})
    amounts = [tx['Quantity'] * tx['UnitPrice'] for tx in valid_transactions]

    print("Available regions:", regions)
    print("Transaction amount range:",
          min(amounts) if amounts else 0,
          "to",
          max(amounts) if amounts else 0)

    total_input = len(transactions)

    # ---------------- FILTERING ----------------
    filtered_by_region = 0
    filtered_by_amount = 0

    filtered_transactions = valid_transactions

    # Apply region filter
    if region:
        before = len(filtered_transactions)
        filtered_transactions = [
            tx for tx in filtered_transactions if tx['Region'] == region
        ]
        filtered_by_region = before - len(filtered_transactions)
        print(f"After region filter ({region}):", len(filtered_transactions))

    # Apply amount filters
    if min_amount is not None or max_amount is not None:
        before = len(filtered_transactions)

        def amount_valid(tx):
            amount = tx['Quantity'] * tx['UnitPrice']
            if min_amount is not None and amount < min_amount:
                return False
            if max_amount is not None and amount > max_amount:
                return False
            return True

        filtered_transactions = [
            tx for tx in filtered_transactions if amount_valid(tx)
        ]

        filtered_by_amount = before - len(filtered_transactions)
        print("After amount filter:", len(filtered_transactions))

    # ---------------- SUMMARY ----------------
    summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(filtered_transactions)
    }

    return filtered_transactions, invalid_count, summary
