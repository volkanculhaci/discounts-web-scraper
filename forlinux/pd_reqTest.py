import pandas as pd
import requests

# Sample URL to fetch data (replace with your own URL)
url = "https://example.com"

# Use Requests to fetch data from the URL
response = requests.get(url)

if response.status_code == 200:
    # Parse HTML content into a DataFrame (for demonstration purposes)
    # Replace this with your actual data parsing logic
    df = pd.read_html(response.text)[0]

    # Display the first few rows of the DataFrame
    print(df.head())
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
