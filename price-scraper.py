import re
import csv
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

SEARCH_URL = "https://www.tcgplayer.com/search/magic/product?q={query}&productLineName=magic&setName=final-fantasy"

# Put your geckodriver full path here:
GECKODRIVER_PATH = os.path.expanduser("~/Network/geckodriver")

# Setup Firefox headless
options = Options()
options.headless = True
service = Service(GECKODRIVER_PATH)
driver = webdriver.Firefox(service=service, options=options)

def get_lowest_price(card_name):
    search_url = SEARCH_URL.format(query=card_name.replace(" ", "+"))
    print(f"Searching for '{card_name}' at: {search_url}")

    driver.get(search_url)
    time.sleep(2)  # Wait for page + prices to load

    try:
        html = driver.page_source

        # Regex for first price inside <span class="inventory__price-with-shipping">...</span>
        price_pattern = r'<span[^>]*class="[^"]*inventory__price-with-shipping[^"]*"[^>]*>\s*\$?([\d.,]+)'
        price_match = re.search(price_pattern, html)
        if not price_match:
            print(f"Price not found for '{card_name}'")
            return None, None
        price = price_match.group(1)

        # Regex for first product URL (product link on search page)
        link_pattern = r'<a[^>]+href="([^"]+)"[^>]*class="[^"]*search-result__product[^"]*"'
        link_match = re.search(link_pattern, html)
        product_url = link_match.group(1) if link_match else None

        print(f"Found price: {price}, product URL: {product_url}")
        return price, product_url

    except Exception as e:
        print(f"Error getting price for '{card_name}': {e}")
        return None, None

def main():
    # Ensure the output directory exists
    output_dir = "prices"
    os.makedirs(output_dir, exist_ok=True)

    # Read cards from external file 'cards.txt'
    with open("cards.txt", "r", encoding="utf-8") as f:
        cards_raw = f.read()

    results = []

    for line in cards_raw.strip().split("\n"):
        line = line.strip()
        # Skip basic lands or empty lines
        if not line or any(x in line for x in ["Plains", "Mountain", "Island", "Forest", "Wastes"]):
            continue

        # Handle double-faced cards separated by //
        names = [n.strip() for n in line.split("//")]
        for name in names:
            price, url = get_lowest_price(name)
            results.append((name, price, url))
            time.sleep(1)  # Polite delay between requests

    # Save results to CSV inside the prices folder
    output_path = os.path.join(output_dir, "final_fantasy_prices.csv")
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Card Name", "Lowest Price", "URL"])
        writer.writerows(results)

    driver.quit()
    print(f"Done! Prices saved to {output_path}")

if __name__ == "__main__":
    main()
