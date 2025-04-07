import requests
import random

# Existing functions
def get_crypto_price(crypto):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        if crypto in data:
            price = data[crypto]['usd']
            return f"The current price of {crypto.capitalize()} is ${price}", price
        else:
            return "Sorry, I couldn't find that cryptocurrency.", None
    except:
        return "Error fetching price—check your connection or crypto name.", None

def trade_suggestion(crypto):
    tips = {
        "bitcoin": "Bitcoin is volatile. Consider using stop-loss orders.",
        "ethereum": "Ethereum often follows Bitcoin. Diversify your risk.",
        "dogecoin": "Dogecoin is community-driven. Watch out for hype."
    }
    return tips.get(crypto.lower(), "No trade suggestion available for this crypto.")

def get_top_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=1"
    try:
        response = requests.get(url)
        data = response.json()
        return "Top 5 Cryptos by Market Cap:\n" + "\n".join([f"{coin['name']} - ${coin['current_price']}" for coin in data])
    except:
        return "Error fetching top coins."

def get_crypto_info(crypto):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}"
    try:
        response = requests.get(url)
        data = response.json()
        desc = data['description']['en'].split('.')[0]
        return f"About {crypto.capitalize()}: {desc}."
    except:
        return "Sorry, I couldn't retrieve info for that cryptocurrency."

def compare_prices(crypto1, crypto2):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto1},{crypto2}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        if crypto1 in data and crypto2 in data:
            price1 = data[crypto1]['usd']
            price2 = data[crypto2]['usd']
            return f"{crypto1.capitalize()}: ${price1}, {crypto2.capitalize()}: ${price2}"
        else:
            return "One or both cryptos not found."
    except:
        return "Error comparing prices."

def get_crypto_joke():
    jokes = [
        "Why don’t crypto traders tell secrets on elevators? Because it’s full of snitches!",
        "I tried to invest in crypto… but my wallet said 'insufficient funds and intelligence'.",
        "Bitcoin is like a teenager — always broke, dramatic, and unpredictable."
    ]
    return random.choice(jokes)

# Price Alerts
alerts = {}

def set_price_alert(crypto, threshold):
    message, price = get_crypto_price(crypto)
    if price is None:
        return message
    alerts[crypto] = float(threshold)
    return f"Alert set for {crypto.capitalize()} at ${threshold}. I’ll check now: {message}"

def check_alerts():
    results = []
    for crypto, threshold in alerts.items():
        message, current_price = get_crypto_price(crypto)
        if current_price and current_price <= threshold:
            results.append(f"🚨 Alert! {crypto.capitalize()} dropped to ${current_price} (threshold: ${threshold})")
        elif current_price:
            results.append(f"{crypto.capitalize()} is at ${current_price}, above your threshold of ${threshold}")
    return "\n".join(results) if results else "No alerts set or triggered."



# Crypto Converter
def convert_crypto(crypto, amount, to_usd=True):
    message, price = get_crypto_price(crypto)
    if price is None:
        return message
    try:
        amount = float(amount)
        if to_usd:
            result = amount * price
            return f"{amount} {crypto.capitalize()} = ${result:.2f}"
        else:
            result = amount / price
            return f"${amount} = {result:.6f} {crypto.capitalize()}"
    except:
        return "Error converting—check your amount."

def chatbot():
    print("👋 Welcome to Crypto Mentor Bot!\nI can check prices (e.g., 'price of bitcoin'), set alerts,top 5, or convert crypto. Type 'exit' to quit.")
    while True:
        user_input = input("You: ").lower()

        if "price of" in user_input:
            crypto = user_input.split("price of")[-1].strip().replace(" ", "-")
            message, _ = get_crypto_price(crypto)
            print("Bot:", message)

        elif "suggestion" in user_input or "tip" in user_input:
            print("Bot: For which cryptocurrency?")
            crypto = input("Crypto: ").strip().lower().replace(" ", "-")
            print("Bot:", trade_suggestion(crypto))

        elif "top coins" in user_input or "top 5" in user_input:
            print("Bot:", get_top_coins())

        elif "info on" in user_input or "about" in user_input:
            crypto = user_input.split("on")[-1].strip().replace(" ", "-") if "on" in user_input else user_input.split("about")[-1].strip().replace(" ", "-")
            print("Bot:", get_crypto_info(crypto))

        elif "compare" in user_input and "and" in user_input:
            parts = user_input.split("compare")[-1].strip().split("and")
            crypto1 = parts[0].strip().replace(" ", "-")
            crypto2 = parts[1].strip().replace(" ", "-")
            print("Bot:", compare_prices(crypto1, crypto2))

        elif "joke" in user_input:
            print("Bot:", get_crypto_joke())

        elif "set alert" in user_input:
            try:
                parts = user_input.split("set alert for")[-1].strip().split(" at ")
                crypto = parts[0].strip().replace(" ", "-")
                threshold = parts[1].strip()
                print("Bot:", set_price_alert(crypto, threshold))
            except:
                print("Bot: Try 'set alert for bitcoin at 50000'.")

        elif "check alerts" in user_input:
            print("Bot:", check_alerts())


        elif "convert" in user_input:
            try:
                parts = user_input.split("convert")[-1].strip().split(" ")
                if "to usd" in user_input:
                    amount = parts[0]
                    crypto = parts[1].replace("to usd", "").strip().replace(" ", "-")
                    print("Bot:", convert_crypto(crypto, amount, to_usd=True))
                elif "to" in user_input and "usd" not in user_input:
                    amount = parts[0]
                    crypto = parts[-1].strip().replace(" ", "-")
                    print("Bot:", convert_crypto(crypto, amount, to_usd=False))
                else:
                    print("Bot: Try 'convert 1 bitcoin to usd' or 'convert 100 usd to bitcoin'.")
            except:
                print("Bot: Error converting—try 'convert 1 bitcoin to usd'.")

        elif user_input in ["hi", "hello"]:
            print("Bot: Hello! Ask me about crypto prices, alerts, news, or conversions!")

        elif user_input in ["exit", "bye", "quit"]:
            print("Bot: Bye! Trade smart. 🚀")
            break

        else:
            print("Bot: Try 'price of bitcoin', 'set alert for bitcoin at 50000', 'news', or 'convert 1 bitcoin to usd'.")

if __name__ == "__main__":
    chatbot() # type: ignore