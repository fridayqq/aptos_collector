<div align="center">

# 🗑️ Aptos Garbage Collector

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Aptos](https://img.shields.io/badge/Aptos-Mainnet-black.svg?style=for-the-badge&logo=aptos&logoColor=white)](https://aptoslabs.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg?style=for-the-badge)](https://github.com/fridayqq/aptos_garbage_collector)

**🚀 A powerful Python toolkit for managing and consolidating APT tokens across multiple wallets**

[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg?style=flat-square)](https://github.com/fridayqq)
[![APT](https://img.shields.io/badge/Token-APT-blue.svg?style=flat-square)](https://coinmarketcap.com/currencies/aptos/)
[![Blockchain](https://img.shields.io/badge/Blockchain-Aptos-purple.svg?style=flat-square)](https://explorer.aptoslabs.com/)

---

</div>

## ✨ Features

- **💰 Balance Checker** (`checker.py`): Monitor APT and LSD token balances across multiple wallets
- **📤 Bulk Sender** (`sender.py`): Automatically transfer APT tokens from multiple wallets to specified recipients
- **💵 Real-time USD Conversion**: Fetches current APT prices from CoinGecko for USD value calculation
- **📊 Transaction Monitoring**: Tracks transaction status and provides explorer links
- **🔧 Automatic CoinStore Registration**: Handles APT CoinStore registration for new accounts
- **⚡ Gas Optimization**: Leaves small amounts for transaction fees

## 📋 Prerequisites

- ![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python&logoColor=white) Python 3.7+
- ![Internet](https://img.shields.io/badge/Internet-Connection-green) Active internet connection
- ![Wallet](https://img.shields.io/badge/Wallet-Seed_Phrases-orange) Valid Aptos seed phrases

## 🚀 Installation

1. Clone or download this repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### For Balance Checking

Create a `seed.txt` file with your seed phrases (one per line):
```
your seed phrase words here for wallet 1
your seed phrase words here for wallet 2
```

### For Token Transfers

Create a `to_send.txt` file with sender seed phrases and recipient addresses:
```
sender_seed_phrase_1; recipient_address_1
sender_seed_phrase_2; recipient_address_2
```

## 📖 Usage

### 📊 Check Balances

Run the balance checker to see APT and LSD balances across all wallets:

```bash
python checker.py
```

**Output includes:**
- 🏠 Wallet addresses derived from seed phrases
- 💰 APT balances in both tokens and USD value
- 🪙 LSD token balances
- 📈 Total portfolio value

### 💸 Send Tokens

Run the bulk sender to transfer APT tokens from multiple wallets:

```bash
python sender.py
```

**Features:**
- 🧮 Automatically calculates maximum sendable amount (balance - 0.01 APT for fees)
- 🔧 Handles CoinStore registration if needed
- 🔗 Provides transaction hashes and explorer links
- ⏱️ Monitors transaction confirmation status

## 🔐 Security Considerations

> ⚠️ **Important Security Notes:**
> - 🚫 Never share your seed phrases
> - 🔒 Keep `seed.txt` and `to_send.txt` files secure and private
> - 🧪 Consider using test networks before mainnet operations
> - ✅ Always verify recipient addresses before sending

## 📁 File Structure

```
aptos_garbage_collector/
├── 📖 README.md              # This file
├── 📦 requirements.txt       # Python dependencies
├── 📊 checker.py            # Balance checking utility
├── 📤 sender.py             # Bulk token sender
├── 🔑 seed.txt              # Your seed phrases
└── 📋 to_send.txt           # Transfer instructions
```

## 🌐 API Endpoints Used

- **🌍 Aptos Mainnet**: `https://fullnode.mainnet.aptoslabs.com/v1`
- **📈 CoinGecko**: `https://api.coingecko.com/api/v3/simple/price`
- **🔍 Explorer**: `https://explorer.aptoslabs.com`

## 🪙 Supported Tokens

- **APT**: Native Aptos token ![APT](https://img.shields.io/badge/-APT-black?style=flat)
- **LSD**: Liquid staking derivative token ![LSD](https://img.shields.io/badge/-LSD-purple?style=flat)

## 🛠️ Error Handling

The tools include comprehensive error handling for:
- ❌ Invalid seed phrases
- 🌐 Network connectivity issues
- 💸 Insufficient balances
- 🔄 Transaction failures
- ⏱️ API rate limits

## ⛽ Transaction Fees

| Parameter | Value |
|-----------|-------|
| 🏃‍♂️ Gas limit | 2000 units |
| 💰 Gas price | 100 units |
| 📊 Typical cost | ~0.002 APT |
| 🛡️ Fee buffer | 0.01 APT reserved |

## 📄 Example Output

### 📊 Balance Checker
```
1) Seed: word1 word2 word3...
    Address:     0x1234...abcd
    Balance:     5.67 APT (~ 45.36 $)
    LSD:         0.00 LSD
----------------------------------------
Total: 5.67 APT (~ 45.36 $)
```

### 📤 Bulk Sender
```
Wallet:    0x1234...abcd
Recipient: 0x5678...efgh
Balance:   5.67 APT
TX sent:   0xabcd1234...
Link:      https://explorer.aptoslabs.com/txn/0xabcd1234...
✅ Transaction confirmed!
```

---

<div align="center">

## 📜 Disclaimer

**This software is provided "as is" without warranty. Users are responsible for:**

🔐 Securing their seed phrases • ✅ Verifying transaction details • ⛽ Understanding Aptos network fees • 📋 Complying with applicable regulations

**⚠️ Use at your own risk. Always test with small amounts first.**

---

Made with ❤️ for the Aptos community

[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=social&logo=github)](https://github.com/fridayqq)
[![Aptos](https://img.shields.io/badge/Aptos-Explorer-blue?style=social&logo=aptos)](https://explorer.aptoslabs.com/)

</div>
