# ForenChain

**Forensic Analysis and Detection of Illicit Transactions in Bitcoin Network**

## Abstract
This project detects illicit Bitcoin transactions using rule-based analysis on blockchain transaction data. It focuses on high-value transfers, unusual fees, and suspicious address links. The Python-based framework achieved 88% accuracy using the Elliptic++ dataset and is designed to assist law enforcement in regulatory compliance.

## Introduction
Bitcoin's rise in the financial world has also facilitated illegal activities such as money laundering and terrorism financing. This project presents a forensic tool to detect such illicit activities using a rule-based framework without machine learning.

## Proposed Methodology
1. **Data Collection**: 
   Collected transaction data from academic and industry sources to identify key transaction       factors that may indicate suspicious behavior.

2. **Rule Definition**: 
   Developed threshold and heuristic rules based on empirical data to flag suspicious Bitcoin      transactions.

3. **Framework Development**: 
   Implemented a Python-based system to integrate these rule sets and analyze transaction data.

4. **Feature Extraction**: 
   Extracted features such as transaction fees, values, and address involvement from the           Elliptic++ dataset to enhance detection accuracy.

5. **Evaluation**: 
   The framework was tested on the Elliptic++ dataset, achieving 88% accuracy, and includes a      user-friendly interface for real-time analysis.

## Project Structure
### 1. Illicit Transaction Detection (illicit_transaction_detection.py)
  This module identifies illicit Bitcoin transactions by analyzing block data, transactions, and addresses against predefined heuristic rules.

### 2. Transaction Hash Details (transaction_details.py)
  This module allows the user to fetch detailed information about a specific transaction hash, including transaction inputs, outputs, addresses, and fee information.

## Future Work
* **Anomaly Detection**: Incorporate advanced anomaly detection techniques to identify transactions beyond predefined heuristics.
* **Real-Time Analysis**: Integrate real-time transaction analysis for continuous monitoring of blockchain activity.

## Usage
### Prerequisites
* Python 3.x
* Requests Library (pip install requests)
* CSV module for Python
