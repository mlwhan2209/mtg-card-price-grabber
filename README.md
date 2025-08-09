# TCGPlayer Final Fantasy Card Price Scraper

This Python script automates the process of fetching the lowest available prices and product URLs for Final Fantasy TCG cards from TCGPlayer.com. It reads card names from a `cards.txt` file, searches for each card, and saves the results into a CSV file.

## Features

- **Automated Price Retrieval**: Automatically searches TCGPlayer for card prices.
- **Batch Processing**: Reads multiple card names from a text file.
- **CSV Output**: Saves all retrieved data into a structured CSV file for easy analysis.
- **Headless Browsing**: Uses Firefox in headless mode, meaning no browser window will pop up during execution.

## Prerequisites

Before running the script, ensure you have the following installed:

- **Python 3**: The script is written in Python 3.
- **Firefox Browser**: Required as the script uses geckodriver to control it.
- **geckodriver**: The WebDriver for Firefox. Download it and place it in an accessible location.

## Setup

Follow these steps to prepare the script:

1. **Install Python Dependencies**

   Install requirements using pip and requirements.txt:

   ```bash
   pip install -r requirements.txt
   ```
   
2. **Configure GECKODRIVER_PATH in the Script**

   Open the `price_scraper.py` file and locate the line:

   ```python
   GECKODRIVER_PATH = os.path.expanduser("~/Network/geckodriver")
   ```

   Replace `os.path.expanduser("~/Network/geckodriver")` with the full path to your `geckodriver` executable. Examples:

   - **macOS/Linux**: `GECKODRIVER_PATH = "/usr/local/bin/geckodriver"` or `GECKODRIVER_PATH = "/Users/YourUsername/Downloads/geckodriver"`
   - **Windows**: `GECKODRIVER_PATH = "C:\\path\\to\\geckodriver.exe"` (use double backslashes or a raw string `r"C:\path\to\geckodriver.exe"`)

3. **Create cards.txt**

   In the same directory as your Python script, create a file named `cards.txt`. Each line should contain the exact name of a Final Fantasy TCG card to search for. Example:

   ```
   Sephiroth
   Cloud
   Aerith
   Zack
   Bahamut ZERO
   ```

   - Lines containing "Plains", "Mountain", "Island", "Forest", or "Wastes" will be skipped, as these are typically basic lands.

## Usage

Run the script from your terminal:

```
python price_scraper.py
```

The script will print progress to the console, showing which card it's searching for and the price it finds.

## Output

The script creates a `prices` directory (if it doesn't exist) in the same location as your script. Inside, it saves a CSV file named `final_fantasy_prices.csv` with the following columns:

- **Card Name**: The name of the card searched.
- **Lowest Price**: The lowest price found on TCGPlayer.
- **URL**: The direct URL to the product page on TCGPlayer.

## Limitations

- **Dependence on TCGPlayer HTML Structure**: The script relies on specific HTML class names and patterns (`inventory__price-with-shipping`, `search-result__product`) to extract prices and links. If TCGPlayer.com changes its website structure, the script may require updates to the regex patterns.
- **Error Handling**: Basic error handling is included, but complex website errors or network issues may cause unexpected behavior.
- **Rate Limiting**: `time.sleep()` calls prevent overwhelming the website, but aggressive usage might lead to temporary IP blocking or CAPTCHAs from TCGPlayer.
- **Specific to Final Fantasy TCG**: The `SEARCH_URL` is hardcoded to search within the "Final Fantasy" product line.
