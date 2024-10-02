# Finding details from trans hash

import requests
from datetime import datetime
import pytz

transaction_hash = '000000000000000000000000000000000000000000000000' # Replace 'TRANSACTION_HASH' with the actual hash of the transaction you're interested in
url = f'https://blockchain.info/rawtx/{transaction_hash}'

# Get the current Bitcoin price in USD
price_url = 'https://blockchain.info/ticker'
price_response = requests.get(price_url)
btc_price_usd = price_response.json()['USD']['last'] if price_response.status_code == 200 else None

response = requests.get(url)
if response.status_code == 200 and btc_price_usd:
    transaction_details = response.json()

    # Convert Unix timestamp to datetime in IST
    timestamp = transaction_details.get("time")
    if timestamp:
        utc_time = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
        ist_time = utc_time.astimezone(pytz.timezone('Asia/Kolkata'))
        date_time_ist = ist_time.strftime('%Y-%m-%d %H:%M:%S IST')
    else:
        date_time_ist = "N/A"

    # Print transaction details
    print("Transaction Hash:", transaction_details.get("hash", "N/A"))
    print("Block Height:", transaction_details.get("block_height", "N/A"))
    print("Date and Time (IST):", date_time_ist)

    # Inputs
    print("\nInputs:")
    for input in transaction_details.get("inputs", []):
        address = input.get("prev_out", {}).get("addr", "Unknown")
        value_satoshi = input.get("prev_out", {}).get("value", "Unknown")
        value_btc = value_satoshi / 100_000_000 if value_satoshi != "Unknown" else "Unknown"
        value_usd = value_btc * btc_price_usd if value_btc != "Unknown" else "Unknown"

        # Fetch and display details of input address
        input_address_url = f'https://blockchain.info/rawaddr/{address}'
        input_address_response = requests.get(input_address_url)
        input_address_data = input_address_response.json() if input_address_response.status_code == 200 else None

        print(f"Address: {address}")
        print(f"Value (Satoshi): {value_satoshi}")
        print(f"Value (BTC): {value_btc}")
        print(f"Value (USD): {value_usd}")
        if input_address_data:
            print()
            print("Input Address Details:")
            print(f"Total Received: {input_address_data.get('total_received', 0)} Satoshi")
            print(f"Total Sent: {input_address_data.get('total_sent', 0)} Satoshi")
            print(f"Final Balance: {input_address_data.get('final_balance', 0)} Satoshi")
            print("Number of Transactions:", input_address_data.get("n_tx"))

    # Outputs
    print("\nOutputs:")
    for index, output in enumerate(transaction_details.get("out", []), start=1):
        address = output.get("addr", "Unknown")
        value_satoshi = output.get("value", "Unknown")
        value_btc = value_satoshi / 100_000_000 if value_satoshi != "Unknown" else "Unknown"
        value_usd = value_btc * btc_price_usd if value_btc != "Unknown" else "Unknown"

        # Fetch and display details of output address
        output_address_url = f'https://blockchain.info/rawaddr/{address}'
        output_address_response = requests.get(output_address_url)
        output_address_data = output_address_response.json() if output_address_response.status_code == 200 else None

        print(f"Output {index}:")
        print(f"Address: {address}")
        print(f"Value (Satoshi): {value_satoshi}")
        print(f"Value (BTC): {value_btc}")
        print(f"Value (USD): {value_usd}")
        if output_address_data:
            print()
            print("Output Address Details:")
            print(f"Total Received: {output_address_data.get('total_received', 0)} Satoshi")
            print(f"Total Sent: {output_address_data.get('total_sent', 0)} Satoshi")
            print(f"Final Balance: {output_address_data.get('final_balance', 0)} Satoshi")
            print("Number of Transactions:", output_address_data.get("n_tx"))
        print()

    # Fees
    fee_satoshi = transaction_details.get("fee", "N/A")
    fee_btc = fee_satoshi / 100_000_000 if fee_satoshi != "N/A" else "N/A"
    fee_usd = fee_btc * btc_price_usd if fee_btc != "N/A" else "N/A"
    print(f"Fees (Satoshi): {fee_satoshi}")
    print(f"Fees (BTC): {fee_btc}")
    print(f"Fees (USD): {fee_usd}")

    # Confirmations (if available)
    confirmations = transaction_details.get("confirmations")
    if confirmations is not None:
        print(f"\nConfirmations: {confirmations}")
    else:
        print("\nConfirmations: N/A")
else:
    print(f'Failed to retrieve data: {response.status_code} or BTC price unavailable')
