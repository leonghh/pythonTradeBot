import pandas as pd
from polygon import RESTClient
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve the Polygon API key from the environment variables
key = os.getenv("POLYGON_API_KEY")

# Initialize the Polygon REST client with the API key
client = RESTClient(key)

# Define the ticker symbol and the date range for daily aggregate data
ticker = "AAPL"
aggs = []

# Fetch daily aggregate data for the specified date range
for day in client.get_aggs(ticker=ticker, multiplier=1, timespan="day", from_="2024-09-01", to="2024-09-23"):
    aggs.append(day)

# Print the first daily aggregate data point for debugging
print(aggs[0])

# Prepare the daily aggregate data for creating a DataFrame
data = []
for agg in aggs:
    data.append({
        "date": agg.timestamp,  # Timestamp of the data
        "open": agg.open,       # Opening price
        "low": agg.low,         # Lowest price
        "high": agg.high,       # Highest price
        "close": agg.close,     # Closing price
        "volume": agg.volume,   # Volume of trades
        "transactions": agg.transactions,  # Number of transactions
        "vwap": agg.vwap        # Volume-weighted average price
    })

# Print the prepared daily aggregate data for debugging
print(data)

# Create a DataFrame from the daily aggregate data
aapl = pd.DataFrame(data)

# Print the first few rows of the DataFrame for debugging
print(aapl.head())

# Convert the timestamp to a readable date format and set it as the index
aapl.index = pd.to_datetime(aapl.date, unit="ms").dt.date

# Drop the original timestamp column as it's no longer needed
aapl.drop(columns=["date"], inplace=True)

# Print the updated DataFrame with the formatted index for debugging
print(aapl.head())

# Define a list to store minute-level aggregate data
mins = []

# Fetch minute-level aggregate data for the specified date range
# Note: The limit is set to 50,000 to fetch a large number of records
for a in client.get_aggs(ticker=ticker, multiplier=1, timespan="minute", 
                         from_="2024-06-01", to="2024-09-23", limit=50000):
    mins.append(a)

# Prepare the minute-level aggregate data for creating a DataFrame
data_mins = []
for agg in mins:
    data_mins.append({
        "date": agg.timestamp,  # Timestamp of the data
        "open": agg.open,       # Opening price
        "low": agg.low,         # Lowest price
        "high": agg.high,       # Highest price
        "close": agg.close,     # Closing price
        "volume": agg.volume,   # Volume of trades
        "transactions": agg.transactions,  # Number of transactions
        "vwap": agg.vwap        # Volume-weighted average price
    })

# Create a DataFrame from the minute-level aggregate data
aapl_mins = pd.DataFrame(data_mins)

# Print the minute-level DataFrame for debugging
print(aapl_mins)

# Convert the timestamp in the "date" column to a readable datetime format
# and set it as the index of the DataFrame.
aapl_mins.index = pd.to_datetime(aapl_mins.date, unit="ms")

# Drop the original "date" column as it is no longer needed after setting it as the index.
aapl_mins.drop(columns=["date"], inplace=True)

# Display the last few rows of the DataFrame to verify the changes.
print(aapl_mins.tail())

# Get price action for the entire market (end-of-day)
prices = client.get_grouped_daily_aggs(date="2024-09-23", include_otc=False)
print(len(prices))