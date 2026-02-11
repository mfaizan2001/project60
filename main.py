#last edited on 20260211
# import requests
import time
from datetime import datetime

# Colored output for terminal
class bcolors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

# Portfolio
portfolio = {
    "AHCL": {"shares": 25, "avg_price": 17.15},
    "BOP": {"shares": 100, "avg_price": 40.62},
    "CPHL": {"shares": 7, "avg_price": 90.15},
    "GLAXO": {"shares": 5, "avg_price": 386.15},
    "KEL": {"shares": 100, "avg_price": 8.58},
    "LUCK": {"shares": 2, "avg_price": 492.50},
    "MEBL": {"shares": 3, "avg_price": 420.95},
    "OGDC": {"shares": 10, "avg_price": 280.61},
    "PAKQATAR": {"shares": 20, "avg_price": 22.84},
    "PTC": {"shares": 140, "avg_price": 50.25},
    #"SAZEW": {"shares": 3, "avg_price": 1746.91},
    "SYS": {"shares": 32, "avg_price": 155.21},
    "UBL": {"shares": 10, "avg_price": 496.86}
}

# Watchlist
watchlist = ["SAZEW","NCPL","IMAGE", "ANL", "CNERGY", "HASCOL"]

base_url = "https://dps.psx.com.pk/company/"
json_url = "https://dps.psx.com.pk/timeseries/int/"

log_file = "PSX_LOG.txt"

# Read old log (if exists)
try:
    with open(log_file, "r", encoding="utf-8") as f:
        old_logs = f.read()
except FileNotFoundError:
    old_logs = ""

# Start new log content
new_log_content = ""
start_time = datetime.now()
start_str = f"----- Portfolio Check Started at {start_time} -----\n\n"
print(start_str)
new_log_content += start_str + "\n"

total_value = 0
total_invested = 0

# Portfolio
print("YOUR PORTFOLIO:\n")
new_log_content += "YOUR PORTFOLIO:\n\n"

for stock, data in portfolio.items():
    try:
        response = requests.get(json_url + stock)
        result = response.json()
        if result and "data" in result and result["data"]:
            current_price = result["data"][0][1]
        else:
            current_price = None
    except Exception:
        current_price = None

    shares = data['shares']
    avg_price = data['avg_price']

    if current_price is not None:
        pl = (current_price - avg_price) * shares
        pct_gain = ((current_price - avg_price) / avg_price) * 100
        total_value += current_price * shares
        total_invested += avg_price * shares

        # Advice
        if pl > 0 and pct_gain > 5:
            advice = "You are in profit ✅, consider holding or selling some"
        elif pl > 0:
            advice = "You are gaining profit 📈, holding is good"
        elif pl < 0 and pct_gain < -5:
            advice = "You are in loss ⚠️, maybe wait for recovery"
        else:
            advice = "Slight loss, stay calm"

        # Sentence
        sentence = (
            f"You bought {shares} shares of {stock} at an average price of {avg_price}.\n"
            f"The current price is {current_price}, your total P/L is {pl:.2f} ({pct_gain:.2f}%). {advice}\n"
            f"More info: {base_url + stock}\n"
        )

        print(sentence)
        new_log_content += sentence + "\n"

    else:
        sentence = f"Price for {stock} is currently not available.\n"
        print(sentence)
        new_log_content += sentence + "\n"

    time.sleep(1)

# Total P/L
total_pl = total_value - total_invested
total_sentence = f"Your total portfolio P/L is {total_pl:.2f}\n"
print(total_sentence)
new_log_content += total_sentence + "\n"

# Watchlist
print("WATCHLIST:\n")
new_log_content += "WATCHLIST:\n\n"

for stock in watchlist:
    try:
        response = requests.get(json_url + stock)
        result = response.json()
        if result and "data" in result and result["data"]:
            current_price = result["data"][0][1]
            previous_close = result["data"][1][1] if len(result["data"]) > 1 else current_price
            pct_change = ((current_price - previous_close) / previous_close) * 100
        else:
            current_price = None
            pct_change = None
    except Exception:
        current_price = None
        pct_change = None

    if current_price is not None:
        if pct_change > 2:
            advice = "Trending up 📈, watch for buy"
        elif pct_change < -2:
            advice = "Trending down ⚠️, monitor closely"
        else:
            advice = "Stable, keep monitoring"

        pct_str = f"{pct_change:.2f}%"
        sentence = f"{stock} current price is {current_price} ({pct_str}). {advice}. More info: {base_url+stock}\n"
        print(sentence)
        new_log_content += sentence + "\n"
    else:
        sentence = f"Price for {stock} is currently not available.\n"
        print(sentence)
        new_log_content += sentence + "\n"

    time.sleep(1)

# End time
end_time = datetime.now()
end_str = f"----- Portfolio Check Ended at {end_time} -----\n\n"
print(end_str)
new_log_content += end_str + "\n"

# Write new log at the top
with open(log_file, "w", encoding="utf-8") as f:
    f.write(new_log_content + old_logs)
