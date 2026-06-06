# Niyam - Crypto Exchange API Toolkit

Welcome to the **Niyam** repository! This project contains a comprehensive suite of Python scripts designed to automate and interact with cryptocurrency exchange APIs (such as Binance Futures). It provides a modular approach to managing everything from wallet balances and account preferences to complex order execution and position management.

This toolkit is built for algorithmic traders, developers, and quants who need a reliable, programmatic way to execute trades and manage their exchange accounts.

---

## 📁 Directory Structure & Features

The repository is organized into 5 core modules, each handling a specific domain of the exchange API:

### 1. `Exchange/`
Manages account-level settings and preferences for derivatives trading.
* **`update_leverage.py`**: Programmatically adjust the leverage for specific trading pairs.
* **`update_preference.py`**: Configure position modes (e.g., One-way mode vs. Hedge mode).

### 2. `Orders/`
The core trading engine. Contains scripts for the full lifecycle of order execution and margin management.
* **Order Placement**: `place_order.py`, `multiple_orders.py`, `linked_orders.py`
* **Order Management**: `order_edit.py`, `delete_order.py`, `cancel_all_orders.py`
* **Advanced Orders**: `split_TP_SL.py` (Split Take-Profit and Stop-Loss)
* **Order Queries**: `open_orders.py`, `order_details.py`, `order_history.py`, `referenced_order.py`
* **Margin Management**: `add_margin.py`, `reduce_margin.py`, `fetch_margin_history.py`

### 3. `Positions/`
Monitors and controls active market positions.
* **`positions.py`**: Retrieve current open positions and Unrealized PNL.
* **`positions_status.py`**: Get detailed risk metrics and liquidation prices.
* **`close_all_positions.py`**: Emergency script to market-close all open positions instantly.

### 4. `UserData/`
Fetches historical user data for accounting and performance tracking.
* **`trade_history.py`**: Retrieve a detailed log of all filled trades.
* **`transaction_history.py`**: Track deposits, withdrawals, and internal transfers.

### 5. `Wallets/`
Monitors capital allocation across different exchange wallets.
* **`futures_wallet.py`**: Check available USDT/USDC balances for derivatives trading.
* **`funding_wallet.py`**: Monitor the funding wallet for deposits and P2P transfers.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.8+
* An active exchange account with API Keys enabled (Ensure you have granted Futures/Trading permissions to the API key).

### Setup Instructions

1. **Clone the repository** (or pull the latest changes):
   ```bash
   git clone https://github.com/soumen888/Niyam.git
   cd Niyam
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory to securely store your API credentials.
   ```bash
   touch .env
   ```
   Add your keys to the `.env` file:
   ```env
   API_KEY=your_exchange_api_key_here
   API_SECRET=your_exchange_api_secret_here
   ```

> [!CAUTION]
> **Never commit your `.env` file to version control!** This repository is already configured with a `.gitignore` that ignores the `.env` file to keep your credentials safe.

### Usage
Run any script from the root directory using Python. For example, to check your open positions:
```bash
python Positions/positions.py
```

---

## 🛡️ Best Practices & Security
* **IP Whitelisting**: Always whitelist your server or local IP address on your exchange's API management page.
* **Read-Only First**: Test the query scripts (like `futures_wallet.py` or `open_orders.py`) before running any script that executes trades or changes account settings.
* **Testnet**: If your exchange provides a Testnet (sandbox environment), consider modifying the base URLs in the scripts to point to the Testnet while developing and testing your strategies.
