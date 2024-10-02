import requests
import csv
import time

# Function to fetch transaction data using transaction hash with retry mechanism
def fetch_transaction_data(tx_hash, retries=3):
    url = f"https://blockchain.info/rawtx/{tx_hash}"
    for attempt in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            transaction_data = response.json()
            return transaction_data
        else:
            print(f"Attempt {attempt + 1} failed to fetch transaction data for transaction hash {tx_hash}")
            time.sleep(1)  # Wait for 1 second before retrying
    return None

# Function to fetch block data using block height with retry mechanism
def fetch_block_data(block_height, retries=3):
    url = f"https://blockchain.info/block-height/{block_height}?format=json"
    for attempt in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            block_data = response.json()
            return block_data.get("blocks")
        else:
            print(f"Attempt {attempt + 1} failed to fetch block data for block height {block_height}")
            time.sleep(1)  # Wait for 1 second before retrying
    return None

# Function to fetch transactions from a given block with retry mechanism
def fetch_transactions_from_block(block_hash, retries=3):
    url = f"https://blockchain.info/rawblock/{block_hash}"
    for attempt in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            block_data = response.json()
            return block_data.get("tx")
        else:
            print(f"Attempt {attempt + 1} failed to fetch transactions for block {block_hash}")
            time.sleep(1)  # Wait for 1 second before retrying
    return None

# Load known bad addresses from CSV
def load_bad_addresses_from_csv(csv_file):
    bad_addresses = {}
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            address, label = row
            bad_addresses[address] = label
    return bad_addresses

# Enhanced anomaly detection logic
def is_anomalous_transaction(transaction, bad_addresses):
    high_value_threshold = 100000000000  # High value threshold in Satoshi
    low_fee_threshold = 1000  # Low transaction fee threshold in Satoshi

    total_output_value = sum(output.get("value", 0) for output in transaction.get("out", []))
    if total_output_value > high_value_threshold:
        return True, transaction.get('hash'), "high threshold value"
    if "fee" in transaction and transaction["fee"] < low_fee_threshold:
        return True, transaction.get('hash'), "low transaction fee"

    # Checking for known bad addresses involvement
    for input in transaction.get("inputs", []):
        if input.get("prev_out", {}).get("addr") in bad_addresses:
            return True, transaction.get('hash'), "known bad address involvement"
    for output in transaction.get("out", []):
        if output.get("addr") in bad_addresses:
            return True, transaction.get('hash'), "known bad address involvement"

    return False, None, None

# Function to analyze transactions within a block for anomalies
def analyze_block(block_hash, block_number, bad_addresses):
    transactions = fetch_transactions_from_block(block_hash)
    if transactions:
        suspicious_transactions = set()
        for tx in transactions:
            is_suspicious, tx_hash, reason = is_anomalous_transaction(tx, bad_addresses)
            if is_suspicious:
                suspicious_transactions.add((tx_hash, reason))

        if suspicious_transactions:
            print(f"Anomalous Transactions Found in Block {block_number}:")
            for tx_hash, reason in suspicious_transactions:
                analyze_related_transactions(tx_hash, reason, bad_addresses)
        else:
            print(f"No illegal transactions found in Block {block_number}.")

def analyze_related_transactions(tx_hash, reason, bad_addresses):
    # Fetch transaction data
    transaction_data = fetch_transaction_data(tx_hash)
    if transaction_data:
        print(f"This transaction looks suspicious because of {reason}: {tx_hash}")
        # Get input and output addresses
        input_addresses = [inp.get('prev_out', {}).get('addr') for inp in transaction_data.get('inputs', [])]
        output_addresses = [out.get('addr') for out in transaction_data.get('out', [])]

        # Second Phase: Check history of involved addresses
        for address in input_addresses + output_addresses:
            if address in bad_addresses:
                print(f"Address {address} ({bad_addresses[address]}) involved in suspicious activity.")
                analyze_address_history(address, bad_addresses)
            else:
                analyze_address_history(address, bad_addresses)

def analyze_address_history(address, bad_addresses, retries=3):
    # Fetch transactions for the address
    url = f"https://blockchain.info/rawaddr/{address}"
    for attempt in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            address_data = response.json()
            transactions = address_data.get('txs', [])
            suspicious_activity_found = False

            # Analyze each transaction
            for tx in transactions:
                is_suspicious, tx_hash, reason = is_anomalous_transaction(tx, bad_addresses)
                if is_suspicious:
                    suspicious_activity_found = True
                    print(f"Suspicious activity found in history for address {address}: {tx_hash} ({reason})")

            if suspicious_activity_found:
                print(f"Address {address} has a history of suspicious activities.")
                print()
            else:
                print(f"Address {address} has no history of illegal activities.")
                print()
            break  # Exit the retry loop if successful
        else:
            print(f"Attempt {attempt + 1} failed to fetch transaction history for address: {address}")
            time.sleep(1)  # Wait for 1 second before retrying

# Main function
def main(start_block, end_block):
    bad_addresses = load_bad_addresses_from_csv('bad_addresses.csv')
    for block_height in range(start_block, end_block + 1):
        block_data = fetch_block_data(block_height)
        if block_data:
            block_hash = block_data[0].get("hash")
            block_number = block_data[0].get("height")
            print(f"Analyzing Block {block_number}:")
            analyze_block(block_hash, block_number, bad_addresses)
            print("\n")
        else:
            print(f"Failed to fetch block data for block height {block_height}.")

if __name__ == "__main__":
    start_block = 000000  # Replace with the start block height of the range you want to analyze
    end_block = 000000  # Replace with the end block height of the range you want to analyze
    main(start_block, end_block)
