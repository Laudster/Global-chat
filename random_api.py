from requests import post

# Set your API key
api_key = '7f555670-c909-492a-91fb-1daecc8b5cf7'

# The URL for random.org's JSON-RPC API
url = 'https://api.random.org/json-rpc/4/invoke'

# The request payload to generate a single 6-digit random number
payload = {
    "jsonrpc": "2.0",
    "method": "generateIntegers",  
    "params": {
        "apiKey": api_key,
        "n": 1,                # Generate 1 random number
        "min": 100000,         # Minimum value (6 digits)
        "max": 999999,         # Maximum value (6 digits)
        "replacement": True    # Allow duplicates (though not relevant for one number)
    },
    "id": 1  # Request ID
}

def random_code():
    # Make the request
    response = post(url, json=payload)

    # Parse the response
    data = response.json()
    random_number = data['result']['random']['data'][0]  # Extract the generated number

    return random_number