import requests
import uuid

# Define the API URL
url = "https://training-api.lexautolease.co.uk/api/v1/quotes/calculate"

# Define the headers (Ensure the token is correct and has necessary permissions)
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxYWJjMmRlZjM0ZyIsIm5iZiI6MTU3Mjk2ODY4OSwiZXhwIjoxNTczNTczNDg5LCJpYXQiOjE1NzI5Njg2ODIsImxiZ19tYWpvcl9kZWFsZXJpZCI6IjEyMzQ1NiIsImxiZ19taW5vcl9kZWFsZXJpZCI6IkExMjM0In0.AACq5TKTYF8Zz-hR41KDyzne8m6rYVGINVNpIDaQfCo",
    "Content-Type": "application/json",
    "X-Lbg-Request-Id": str(uuid.uuid4())  # Generate a GUID
}

# Define the example JSON request body
request_body = {
    "asset": {
        "cap_id": 12345,
        "cap_code": "XXXX19125SBDTM2 L",
        "model_year": 2020.5,
        "options": ["12345"]
    },
    "accessories": [
        {
            "type": "DealerFit",
            "description": "Accessory 1",
            "price": 100.00
        },
        {
            "type": "DealerFit",
            "description": "Accessory 2",
            "price": 299.99
        },
        {
            "type": "ThirdParty",
            "description": "Accessory 3",
            "price": 109.99
        }
    ],
    "financials": {
        "contract_type_id": 3,
        "plan": 106,
        "term": 36,
        "mileage": 12000,
        "relief_vehicle": 0,
        "customer_initial_payment": 2500.00,
        "estimated_sales_value": None,
        "cust_reference": "Any text"
    },
    "adjustments": {
        "off_invoice_support": None,
        "otrp": None,
        "commission": None,
        "discount": None,
        "customer_terms": 1,
        "co2_emission": 180
    }
}

# Send the POST request
response = requests.post(url, headers=headers, json=request_body)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    quote_details = response.json()
    print("Quote Details:")
    print(quote_details)
else:
    print(f"Failed to calculate quote. Status code: {response.status_code}")
    print("Response:", response.text)

    # Additional error handling
    if response.status_code == 403:
        print("Access Denied. Please check your authorization token and permissions.")
