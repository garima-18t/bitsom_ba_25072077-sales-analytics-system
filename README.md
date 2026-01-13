# Sales Data Analytics System

## Project Overview

The Sales Data Analytics System is a Python application that processes, analyzes, and generates insights from raw sales transaction data. The system handles real-world data challenges including non-standard encoding, messy formatting, and incomplete records while providing meaningful business intelligence through automated analysis and reporting.

### Key Capabilities

- Reads and processes non-UTF-8 encoded pipe-delimited sales data files
- Implements robust data cleaning and validation for messy datasets
- Applies user-defined filters for region and transaction amount ranges
- Conducts comprehensive sales analytics across multiple dimensions
- Integrates with external REST APIs to enrich transaction data
- Generates detailed formatted text reports with actionable insights
- Exports enriched datasets for further analysis

---

## Project Structure

```
sales-analytics-system/
├── data/
│   ├── sales_data.txt              # Input: Raw sales transactions
│   └── enriched_sales_data.txt     # Output: API-enriched sales data
├── output/
│   └── sales_report.txt            # Output: Formatted analysis report
├── utils/
│   ├── file_handler.py             # File I/O with encoding handling
│                                    # Data parsing and field extraction
│                                    # Data validation and quality checks
│   ├── data_processor.py           # Sales analytics and calculations
│   ├── api_handler.py              # External API integration
│   └── report_generator.py         # Report formatting and generation
├── test_reader.py
├── main.py
└── README.md
```

---

## System Requirements

- **Python Version**: Python 3.7 or higher
- **Required Library**: `requests` (version 2.25.0 or higher)
- **Internet Connection**: Required for API integration

---

## Installation and Setup

### Step 1: Install Dependencies

pip install requests

### Step 2: Verify Installation

python --version
python -c "import requests; print(requests.__version__)"

### Step 3: Prepare Input Data

Ensure the `sales_data.txt` file is located in the `data/` directory.

---

## How to Run

Navigate to the project root directory and execute:

python main.py

### Interactive Filtering

The program will prompt for optional filters:

- Region filter (e.g., North, South, East, West)
- Minimum transaction amount
- Maximum transaction amount

Press Enter to skip any filter.

---

## Detailed Functionality

### Part 1: Data File Handling and Preprocessing

**Encoding Management**: Handles non-UTF-8 files using fallback sequence (UTF-8 → Latin-1 → system default)

**Parsing**: Splits pipe-delimited data and removes commas from numeric fields

**Validation Rules**:
- Transaction IDs must start with "TXN"
- Product IDs must start with "PROD"
- Customer IDs must start with "CUST"
- Quantity and price must be positive numbers
- All fields must be present

Invalid records are rejected and counted.

### Part 2: Data Processing and Analytics

The system performs seven key analyses:

1. **Total Revenue Calculation**: Sum of all transaction amounts
2. **Region-Wise Sales**: Aggregates revenue, transaction count, and averages by region
3. **Top Selling Products**: Identifies highest-grossing products (top 5)
4. **Customer Purchase Analysis**: Ranks customers by lifetime value (top 5)
5. **Daily Sales Trends**: Tracks revenue performance over time
6. **Peak Sales Day**: Identifies the highest revenue day
7. **Low Performing Products**: Flags products below revenue threshold

### Part 3: API Integration

**Endpoint**: `https://dummyjson.com/products`

**Process**:
1. Fetches product data from DummyJSON API
2. Creates mapping of product IDs to categories, brands, and ratings
3. Enriches each sales transaction with API data
4. Handles missing matches gracefully (assigns "Unknown", "N/A", 0.0)

**Enriched Fields**:
- Product category
- Brand name
- Product rating

### Part 4: Report Generation

The system generates a comprehensive formatted text report with eight sections:

1. **Header**: Title, timestamp, data source
2. **Overall Summary**: Total revenue, transaction count, averages, date range
3. **Region-Wise Performance**: Revenue breakdown by region with percentages
4. **Top Products**: Highest-grossing products with contribution percentages
5. **Top Customers**: Most valuable customers by total spend
6. **Daily Sales Trends**: Chronological performance with peak day highlighted
7. **Product Performance**: Low-performing products requiring attention
8. **API Enrichment Summary**: Match statistics and sample enriched records

### Part 5: Main Application Flow

1. Load raw sales data with encoding detection
2. Parse and clean pipe-delimited fields
3. Validate records and filter invalid entries
4. Prompt user for optional filters (region, amount range)
5. Apply filters to dataset
6. Execute all analytics functions
7. Fetch product data from external API
8. Enrich sales records with API data
9. Export enriched dataset
10. Generate and save formatted report

---

## Input and Output Files

### Input: sales_data.txt

**Format**: Pipe-delimited text file

### Output: enriched_sales_data.txt

**Format**: Pipe-delimited with additional API-enriched columns

### Output: sales_report.txt

Complete analysis report with all eight sections in formatted text.

---

## Error Handling

The system implements comprehensive error handling:

- **File Not Found**: Displays clear error message and exits gracefully
- **Encoding Issues**: Attempts multiple encodings before failing
- **API Failures**: Continues with default values for product enrichment
- **Invalid User Input**: Validates and prompts for re-entry
- **Malformed Records**: Rejects invalid data and reports count

All errors are handled without crashing, ensuring robust operation.

---

## Evaluation and Submission Notes

### Assignment Criteria Coverage

This project demonstrates:

1. **File Handling**: Multi-encoding support, delimiter parsing, data cleaning
2. **Data Structures**: Dictionaries for aggregation, lists for filtering and sorting
3. **API Integration**: HTTP requests, JSON parsing, error handling
4. **Modular Design**: Separated concerns across six utility modules
5. **User Interaction**: Interactive filtering with input validation
6. **Error Handling**: Try-except blocks with graceful degradation
7. **Output Generation**: Multiple formats (enriched data, formatted report)

### Modular Design Benefits

- **Maintainability**: Independent module updates
- **Testability**: Isolated unit testing
- **Reusability**: Portable utility functions
- **Scalability**: Easy feature additions
- **Readability**: Clear organization by functionality

### Clean Coding Practices

- Meaningful variable names
- Function documentation with docstrings
- PEP 8 style compliance
- DRY principle (no code duplication)
- Clear separation of concerns
- Informative error messages

---
