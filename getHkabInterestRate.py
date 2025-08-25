import requests
from bs4 import BeautifulSoup

# Request the target URL
def crawler():
    response = requests.get("https://www.hkab.org.hk/en/rates/hibor")
    response.raise_for_status()
    print(response.text)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table rows containing the interest rates
    rows = soup.select(".general_table_row")

    # Extract the maturity and interest rate from each row
    rates = {}
    for row in rows:
        cells = row.select(".general_table_cell")
        if len(cells) == 2:  # Ensure the row has two cells (Maturity and Rate)
            maturity = cells[0].get_text(strip=True)
            rate = cells[1].get_text(strip=True)
            rates[maturity] = rate

    return rates

# Execute the crawler and print the rates
rates = crawler()
print(rates)
