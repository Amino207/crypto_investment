import mysql.connector as mysql
import datetime


def connect_to_db():
    """
    Establish connection to the database.
    """
    return mysql.connect(
        host="localhost",
        user="root",
        password="@Amino207208",  # Replace with your MySQL root password
        database="crypto"
    )


def create_account(username, password, initial_deposit):
    """
    Create a new account with username, password, and initial deposit.
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO accounts (username, password, initial_deposit) VALUES (%s, %s, %s)",
            (username, password, initial_deposit)
        )
        conn.commit()
        print(f"Account created for {username}. Initial deposit: £{initial_deposit}")
    except mysql.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def view_accounts():
    """
    Fetch all accounts from the database.
    """
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT username, initial_deposit FROM accounts")
        accounts = cursor.fetchall()
        return accounts
    except mysql.Error as e:
        print(f"Error fetching accounts: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def view_assets():
    """
    Fetch all assets from the database.
    """
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT asset_name, price FROM assets")
        assets = cursor.fetchall()
        return assets
    except mysql.Error as e:
        print(f"Error fetching assets: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def deposit_withdraw(username, action, amount):
    """
    Deposit or withdraw funds for a user.
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    #Selecting the initial_deposit from account table where username matches to that account
    cursor.execute("SELECT initial_deposit FROM accounts WHERE username = %s", (username,))
    result = cursor.fetchone()

    if not result:
        print(f"User {username} not found.")
        return
    balance = result[0] #Returns a tuple with one element which is initial_deposit. The reason it has one element because I only SELECT initial_deposit column
    if action == 'deposit':
        balance += amount
    elif action == 'withdraw' and balance >= amount:
        balance -= amount
    else:
        print("Insufficient funds.")
        cursor.close()
        conn.close()
        return

    #Updating the accounts table with new balance
    cursor.execute("UPDATE accounts SET initial_deposit = %s WHERE username = %s", (balance, username))
    conn.commit()
    print(f"Transaction successful. New balance: £{balance:.2f}")

    cursor.close()
    conn.close()





def buy_asset(username, asset_name, quantity):
    """
    Buy assets and update the user's portfolio.
    """
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT price FROM assets WHERE asset_name = %s", (asset_name,))
    asset = cursor.fetchone()

    if not asset:
        print(f"Asset {asset_name} not found.")
        return

    asset_price = asset[0]
    total_cost = asset_price * quantity

    #Fetching the initial_deposit from account to buy assets
    cursor.execute("SELECT initial_deposit FROM accounts WHERE username = %s", (username,))
    user_account = cursor.fetchone()

    if not user_account or user_account[0] < total_cost:
        print("Insufficient funds.")
        return
    #Calculate the total cost and UPDATE the balance in account table
    balance = user_account[0] - total_cost
    cursor.execute("UPDATE accounts SET initial_deposit = %s WHERE username = %s", (balance, username))

    # Inserting a new row into portfolio
    cursor.execute("""
        INSERT INTO portfolio (username, asset_name, quantity)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE quantity = quantity + %s
    """, (username, asset_name, quantity, quantity)) # The first quantity corresponds to the placeholder %s
    # ON DUPLICATE KEY: This part of the query tells MySQL to check if there is already a record with the same unique key (in this case,
#     a combination of username and asset_name). If such a record exists, it will not insert a new row but will instead update the existing row.
#     else it will UPDATE quantity = quantity + %s

    #Insert a new record into transaction table
    cursor.execute("""
        INSERT INTO transactions (datetime, username, action, asset_name, quantity)
        VALUES (%s, %s, %s, %s, %s)
    """, (datetime.datetime.now(), username, 'buy', asset_name, quantity))

    conn.commit()
    print(f"Bought {quantity} {asset_name}. Total cost: £{total_cost:.2f}")
    cursor.close()
    conn.close()


#---------------------------------------

def sell_asset(username, asset_name, quantity):
    """
    Sell assets and update the user's portfolio.
    """
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT quantity FROM portfolio WHERE username = %s AND asset_name = %s", (username, asset_name))
    portfolio_entry = cursor.fetchone()

    if not portfolio_entry or portfolio_entry[0] < quantity:
        print("Insufficient assets to sell.")
        return

    cursor.execute("SELECT price FROM assets WHERE asset_name = %s", (asset_name,))
    asset_price = cursor.fetchone()[0]

    total_revenue = asset_price * quantity
    #Updating the quantity in portfolio table
    cursor.execute("UPDATE portfolio SET quantity = quantity - %s WHERE username = %s AND asset_name = %s",
                   (quantity, username, asset_name))

    #Delete the asset from the table if quantity = 0
    cursor.execute("DELETE FROM portfolio WHERE quantity = 0")

    #Calculate the revenue and update the account balance
    cursor.execute("UPDATE accounts SET initial_deposit = initial_deposit + %s WHERE username = %s",
                   (total_revenue, username))

    cursor.execute("""
        INSERT INTO transactions (datetime, username, action, asset_name, quantity)
        VALUES (%s, %s, %s, %s, %s)
    """, (datetime.datetime.now(), username, 'sell', asset_name, quantity))

    conn.commit()
    print(f"Sold {quantity} {asset_name}. Total revenue: £{total_revenue:.2f}")
    cursor.close()
    conn.close()

#----------------------------------------------

def view_portfolio(username):
    """
    Fetch portfolio details for a user.
    """
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.asset_name, p.quantity, a.price, (p.quantity * a.price) AS total_value
        FROM portfolio p
        JOIN assets a ON p.asset_name = a.asset_name
        WHERE p.username = %s
    """, (username,))

    portfolio = cursor.fetchall()
    if not portfolio:
        return "Portfolio is empty or user does not exist."


    # total_value = 0
    # for row in portfolio:
    #     total_value += row['total_value']


    #fetchall, SQL query returns multiple rows, fetchall() returns them as a list of dictionaries (because dictionary=True).
    # without it, it returns a list of tuples. But fetchone returns a tuple as default.
    total_value = sum(row['total_value'] for row in portfolio)
    portfolio_summary = "\n".join(
        [f"{row['asset_name']}: {row['quantity']} units | £{row['price']:.2f} each => £{row['total_value']:.2f}"
         for row in portfolio]
    )
    portfolio_summary += f"\nTotal Portfolio Value: £{total_value:.2f}"
    return portfolio_summary
