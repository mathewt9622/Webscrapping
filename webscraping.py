import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.amazon.in/s?k=sunglasses"  # Customize the search query

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

max_retries = 5
retry_delay = 5  # seconds

for retry in range(max_retries):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        break  # Exit the loop if the request is successful
    except requests.RequestException as e:
        print(f"Request error (Retry {retry + 1}/{max_retries}):", e)
        if retry < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Exiting.")
            exit()

soup = BeautifulSoup(response.content, "html.parser")
product_cards = soup.find_all("div", class_="s-result-item")

product_data = []

for product_card in product_cards:
    try:
        product_name = product_card.find("span", class_="a-text-normal").text.strip()
        product_price = product_card.find("span", class_="a-offscreen").text if product_card.find("span", class_="a-offscreen") else "N/A"
        product_rating = product_card.find("span", class_="a-icon-alt").text if product_card.find("span", class_="a-icon-alt") else "N/A"
        
        product_data.append({
            "Product Name": product_name,
            "Product Price": product_price,
            "Product Rating": product_rating
        })
    except Exception as e:
        print("Error in extracting product data:", e)

df = pd.DataFrame(product_data)
csv_filename = "amazon_sunglasses.csv"  # Customize the CSV filename
df.to_csv(csv_filename, index=False)

print(f"Data successfully extracted and CSV saved as '{csv_filename}'.")
