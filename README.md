# 💹 Crypto Investment Platform Project

## 1. Project Overview

The Crypto Investment Platform project is developed using **Python**, **Tkinter**, and **MySQL**. The platform allows users to:

- Create accounts
- View and manage funds
- Buy and sell crypto assets
- View portfolios
- Perform secure, validated transactions via GUI and client-server communication

All user actions communicate with a server to update the database in real time. The project emphasizes ease of use, error handling, and data consistency using SQL for storage.

---

## 2. 📁 List of Files

- `crypto_investment_SQL.py`
- `assets.py`
- `server.py`
- `client_GUI.py`
- `crypto_investment_db.sql`

### Description of File Functionalities

- **`crypto_investment_SQL.py`**  
  Handles all MySQL database operations like managing accounts, assets, deposits, withdrawals, trades, and generating portfolio insights.

- **`server.py`**  
  Acts as a server handling client-side requests using socket communication. Integrates with `crypto_investment_SQL.py` and uses `pickle` for data transmission.

- **`client_GUI.py`**  
  A user-friendly graphical interface built with Tkinter for account management, asset trading, and portfolio viewing. Includes input fields, buttons, and validation.

- **`assets.py`**  
  Implements Object-Oriented Programming to define asset structures with methods for handling crypto asset data.

- **`crypto_investment_db.sql`**  
  Initializes the MySQL `crypto` database with 4 tables: `accounts`, `assets`, `transactions`, and `portfolio`, including seed data for various cryptocurrencies.

---

## 3. 🔧 Implementation Plan

### 3.1 Development Stages

1. **Text-Based Setup**
   - Created accounts with username/password/balance stored in `.txt` files
   - Displayed asset list, enabled buy/sell based on funds
   - Logged transactions in `transactions.txt`

2. **Object-Oriented Refactoring**
   - Defined `Asset` class with name, price, quantity
   - Added methods like `get_name()` and `get_current_price()`

3. **Client-Server Model**
   - Built server to handle logic (load assets, accounts, portfolio from `.txt`)
   - Client sends requests to perform actions like buy/sell/view assets

4. **Database Integration**
   - Migrated data from `.txt` to MySQL for better performance
   - SQL used for all CRUD operations (Create, Read, Update, Delete)

5. **GUI Implementation**
   - Built with Tkinter
   - 8 main buttons/functions (create account, deposit, withdraw, buy/sell, view portfolio, etc.)

---

## 4. 🚀 Running Instructions

### 4.1 Prerequisites

- Python 3.x installed
- MySQL installed and running
- Required libraries:
  ```bash
  pip install mysql-connector-python

---
## 5. Author  
👤 **Amin Kazemi**  
- GitHub: (https://github.com/Amino207)  
- LinkedIn: www.linkedin.com/in/amin-kazemi-0b86a4338
- Email: amin.kazemi207@gmail.com 
