import requests

def convert_currency(from_currency, to_currency, amount):
    url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"

    try:
        response = requests.get(url)
        data = response.json()

        if data["result"] == "success":
            rates = data["rates"]
            rate = rates.get(to_currency.upper())

            if rate:
                converted = amount * rate
                print(f"\n📈 Rate: 1 {from_currency.upper()} = {rate:.4f} {to_currency.upper()}")
                print(f"💰 {amount} {from_currency.upper()} = {converted:.2f} {to_currency.upper()}")
            else:
                print(f"❌ Currency code '{to_currency}' not found.")
        else:
            print("❌ Failed to fetch exchange rates.")
            print(data)
    except Exception as e:
        print("⚠️ An error occurred:", e)

def main():
    print("💱 Currency Converter")
    from_curr = input("Enter source currency (e.g., USD): ")
    to_curr = input("Enter target currency (e.g., EUR): ")
    try:
        amount = float(input("Enter amount to convert: "))
        convert_currency(from_curr, to_curr, amount)
    except ValueError:
        print("❌ Amount must be a valid number.")

if __name__ == "__main__":
    main()
