import socket
import pickle
from tkinter import *
from tkinter import messagebox

from crypto_investment_SQL import *

root = Tk()
root.title('Crypto Investment Project')
root.geometry('400x700')
root.configure(bg='black')

#Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5006))
print(s.recv(1024).decode('utf-8'))

#Create account function
def create_account(s):

    create_account_window = Toplevel(root)
    create_account_window.title('Crypto Investment Project - Create Account')
    create_account_window.geometry('400x500')
    create_account_window.configure(bg='black')

    #column configuration initially
    create_account_window.grid_columnconfigure(0, weight=1)
    create_account_window.grid_columnconfigure(1, weight=1)
    create_account_window.grid_columnconfigure(2, weight=1)

    #-------------------------- Submit / Back functions

    #submit account function
    def submit():
        #get user's inputs from entry box
        username = username_entry.get()
        password = password_entry.get()
        initial_deposit = fund_entry.get()

        #make sure entry filedes are not empty
        if username and password and initial_deposit:
            initial_deposit = float(initial_deposit)  # Convert the initial deposit to float

            # Send the Create Account request to the server
            s.send(f'CREATE,{username},{password},{initial_deposit}'.encode('utf-8'))

            # Receive response from server
            server_response = s.recv(1024).decode('utf-8')
            messagebox.showinfo('Account Created', server_response)

            #destroy the create account window after submitting the data
            create_account_window.destroy()


        else:
            messagebox.showerror(title='Error', message='Please fill all fields!')



    #back to main menu function
    def back():
        create_account_window.destroy()

        #------------------------------Label / entry box/ button

    Label(create_account_window, text='Create Account',
                                  font=('Impact', 22),
                                  fg='light yellow',
                                  bg='black').grid(row=0, column=0, columnspan=3, sticky='n', pady=20)


    #Username entry box
    username_label = Label(create_account_window,
                           text='Username :',
                           font=('Impact', 18),
                           fg='light yellow',
                           width=12,
                           bg='black')
    username_label.grid(row=1, column=0, pady=20, padx=20)

    username_entry = Entry(create_account_window,font=('Arial', 14),fg='light yellow',bg='#313131', width=18)
    username_entry.grid(row=1, column=1)


    #Password entry box
    password_label = Label(create_account_window,
                               text='Password :',
                               font=('Impact', 18),
                               fg='light yellow',
                               width=12,
                               bg='black')
    password_label.grid(row=2, column=0, pady=20, padx=20)

    password_entry = Entry(create_account_window, show='*',font=('Arial', 14),fg='light yellow', bg='#313131',width=18)
    password_entry.grid(row=2, column=1)


    # Initial deposit entry box
    fund_label = Label(create_account_window,
                           text='Initial Deposit :',
                           font=('Impact', 18),
                           fg='light yellow',
                           width=12,
                           bg='black')
    fund_label.grid(row=3, column=0, pady=20, padx=20)

    fund_entry = Entry(create_account_window, font=('Arial', 14),fg='light yellow', bg='#313131', width=18)
    fund_entry.grid(row=3, column=1)


    #Create button
    submit_button = Button(create_account_window,
                           text='Submit',
                           font=('Impact', 16),
                           width=10,
                           fg='#313131',
                           pady=10,
                           bd=3,
                           relief=SUNKEN,
                           command=submit
                        )
    submit_button.grid(row=4, column=0, pady=20, padx=20)

    back_button = Button(create_account_window,
                         text='Back',
                         font=('Impact', 16),
                         width=10,
                         fg='#313131',
                         pady=10,
                         bd=3,
                         relief=SUNKEN,
                         command=back
                         )
    back_button.grid(row=4, column=1, pady=20, padx=20)

#----------------------------------------------------------------------------------------
def view_account(s):
    # Send the View Account request to the server
    s.send('VIEW,'.encode('utf-8'))

    # Fetch and deserialize the data from the server
    try:
        accounts = pickle.loads(s.recv(1024))
    except Exception as e:
        messagebox.showerror('Error', f'Failed to fetch account data: {e}')
        return

    # Create a new window for viewing accounts
    view_account_window = Toplevel(root)
    view_account_window.title('Crypto Investment Project - View Account')
    view_account_window.geometry('400x500')
    view_account_window.configure(bg='black')

    # Column configuration initially
    view_account_window.grid_columnconfigure(0, weight=1)
    view_account_window.grid_columnconfigure(1, weight=1)

    # Back function
    def back():
        view_account_window.destroy()

    # Title label
    Label(view_account_window,
          text='View Accounts',
          font=('Impact', 22),
          fg='light yellow',
          bg='black').grid(row=0, column=0, columnspan=2, pady=20)

    # Text box to display account details
    text_area = Text(view_account_window,
                     bg='light yellow',
                     font=('Arial', 14),
                     height=15,
                     width=40,
                     fg='black',
                     padx=5,
                     pady=5)
    text_area.grid(row=1, column=0, columnspan=2, pady=10)

    # Populate the text area with account information
    if accounts:
        for account in accounts:
            text_area.insert(END, f"Username: {account['username']}\n")
            text_area.insert(END, f"Balance: £{account['initial_deposit']:.2f}\n")
            text_area.insert(END, "-" * 30 + "\n")
    else:
        text_area.insert(END, "No accounts found.\n")

    text_area.config(state=DISABLED)  # Prevent editing the text area

    # Back button
    back_button = Button(view_account_window,
                         text='Back',
                         font=('Impact', 16),
                         width=10,
                         fg='#313131',
                         pady=10,
                         bd=3,
                         relief=SUNKEN,
                         command=back)
    back_button.grid(row=2, column=0, columnspan=2, pady=20)

#-----------------------------------------------------------------------------

def view_assets(s):
    # Send the View Asset request to the server
    s.send('ASSET,'.encode('utf-8'))

    # Fetch and deserialize the data from the server
    try:
        assets = pickle.loads(s.recv(1024))
    except Exception as e:
        messagebox.showerror('Error', f'Failed to fetch assets data: {e}')
        return

    # Create a new window for viewing Assets
    view_asset_window = Toplevel(root)
    view_asset_window.title('Crypto Investment Project - View Assets')
    view_asset_window.geometry('400x500')
    view_asset_window.configure(bg='black')

    # Column configuration initially
    view_asset_window.grid_columnconfigure(0, weight=1)
    view_asset_window.grid_columnconfigure(1, weight=1)

    # Back function
    def back():
        view_asset_window.destroy()

    # Title label
    Label(view_asset_window,
          text='View Assets',
          font=('Impact', 22),
          fg='light yellow',
          bg='black').grid(row=0, column=0, columnspan=2, pady=20)

    # Headers for asset name and price
    Label(view_asset_window,
          text='Asset Name',
          font=('Impact', 16),
          fg='light yellow',
          bg='black').grid(row=1, column=0, pady=10, padx=10)

    Label(view_asset_window,
          text='Price',
          font=('Impact', 18),
          fg='light yellow',
          bg='black').grid(row=1, column=1, pady=10, padx=10)

    # Display the assets
    if assets:
        row = 2  # Start displaying from row 2
        for asset in assets:
            # Asset Name on the left
            asset_name_label = Label(view_asset_window,
                                     text=asset['asset_name'],
                                     font=('Arial', 14),
                                     fg='light yellow',
                                     bg='black')
            asset_name_label.grid(row=row, column=0, pady=10, padx=10)

            # Asset Price on the right
            asset_price_label = Label(view_asset_window,
                                      text=f"${asset['price']}",
                                      font=('Arial', 14),
                                      fg='light yellow',
                                      bg='black')
            asset_price_label.grid(row=row, column=1, pady=10, padx=10)
            row += 1

    # Back button
    back_button = Button(view_asset_window,
                         text='Back',
                         font=('Impact', 16),
                         width=10,
                         fg='#313131',
                         pady=10,
                         bd=3,
                         relief=SUNKEN,
                         command=back)
    back_button.grid(row=row + 1, column=0, columnspan=2, pady=20)

#--------------------------------------------------------------------------------
# #Deposit /Withdraw function

def fund(s):
    # Create a new window for depositing/withdrawing funds
    fund_window = Toplevel()
    fund_window.title('Crypto Investment Project - Deposit/Withdraw')
    fund_window.geometry('400x500')
    fund_window.configure(bg='black')

    # Column configuration
    fund_window.grid_columnconfigure(0, weight=1)
    fund_window.grid_columnconfigure(1, weight=1)

    # Title label
    Label(fund_window,
          text='Deposit & Withdraw',
          font=('Impact', 22),
          fg='light yellow',
          bg='black').grid(row=0, column=0, columnspan=2, pady=20)

    x = IntVar()

    # Create a frame for the radio buttons
    frame = Frame(fund_window, bg='black')
    frame.grid(row=1, column=0, columnspan=2, pady=20)

    # Create radio buttons for deposit and withdraw options
    deposit_button = Radiobutton(frame,
                                 text='Deposit',
                                 font=('Impact', 14),
                                 fg='light yellow',
                                 variable=x,
                                 value=0,
                                 bg='black')
    deposit_button.grid(row=0, column=0, padx=5, pady=5)

    withdraw_button = Radiobutton(frame,
                                  text='Withdraw',
                                  font=('Impact', 14),
                                  fg='light yellow',
                                  variable=x,
                                  value=1,
                                  bg='black')
    withdraw_button.grid(row=0, column=1, padx=5, pady=5)

    #Username entry
    username_entry = Entry(fund_window, font=('Arial', 14),fg='light yellow', bg='#313131', width=18)
    username_entry.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    username_entry.insert(0, 'Username')

    #Amount entry
    amount_entry = Entry(fund_window, font=('Arial', 14),fg='light yellow', bg='#313131', width=18)
    amount_entry.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    amount_entry.insert(0, 'Amount')

    #submit function
    def submit():
        username = username_entry.get()
        amount = amount_entry.get()

        if not username or not amount:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Error","Amount must be greater than zero.")

            # Based on radio button, either deposit or withdraw
            if x.get() == 0:  # Deposit
                action = "deposit"
                # Send deposit request to server
                s.send(f'FUNDS,{username},{action},{amount}'.encode('utf-8'))
                messagebox.showinfo("Server Response", message=s.recv(1024).decode('utf-8'))


            elif x.get() == 1:  # Withdraw
                action = "withdraw"
                # Send withdraw request to server
                s.send(f'FUNDS,{username},{action},{amount}'.encode('utf-8'))
                messagebox.showinfo("Server Response", message=s.recv(1024).decode('utf-8'))




        except Exception as e:
            messagebox.showerror(title='Error', message=f"An error occurred: {str(e)}")


    # Create buttons
    submit_button = Button(fund_window,
                           text='Submit',
                           font=('Impact', 16),
                           width=10,
                           fg='#313131',
                           pady=10,
                           bd=3,
                           relief=SUNKEN,
                           command=submit
                           )
    submit_button.grid(row=4, column=0, columnspan=2, pady=20)



    back_button = Button(fund_window,
                         text='Back',
                         font=('Impact', 16),
                         width=10,
                         fg='#313131',
                         pady=10,
                         bd=3,
                         relief=SUNKEN,
                         command=fund_window.destroy)
    back_button.grid(row=5, column=0, columnspan=2)


#------------------------------------------------------------------------
#Buy asset function
def buy_asset(s):
    # Create a new window for depositing/withdrawing funds
    buy_asset_window = Toplevel()
    buy_asset_window.title('Crypto Investment Project - Buy Asset')
    buy_asset_window.geometry('400x500')
    buy_asset_window.configure(bg='black')

    # Column configuration
    buy_asset_window.grid_columnconfigure(0, weight=1)
    buy_asset_window.grid_columnconfigure(1, weight=1)


   #Submit function
    def submit():
        username = entry_username.get()
        asset_name = entry_asset.get()
        quantity = float(entry_quantity.get())


        if not username or not asset_name or not quantity:
            messagebox.showerror("Error", "All fields are required!")
            return




        # Send the Buy request to the server
        s.send(f'BUY,{username},{asset_name},{quantity}'.encode('utf-8'))

        # Receive response from server
        server_response = s.recv(1024).decode('utf-8')
        messagebox.showinfo('Bought', server_response)

        # destroy the window after submitting the data
        buy_asset_window.destroy()




    # Title label
    Label(buy_asset_window,
          text='Buy Asset',
          font=('Impact', 22),
          fg='light yellow',
          bg='black').grid(row=0, column=0, columnspan=2, pady=20)


    #Create Labels / Entry
    Label(buy_asset_window,
          text='Username',
          font=('Impact', 16),
          bg='black',
          fg='light yellow',
          ).grid(row=1, column=0, pady=20)

    entry_username = Entry(buy_asset_window,font=('Arial', 14),fg='light yellow',bg='#313131', width=18)
    entry_username.grid(row=1, column=1)

    Label(buy_asset_window,
          text='Asset',
          font=('Impact', 16),
          bg='black',
          fg='light yellow',
          ).grid(row=2, column=0, pady=20)

    entry_asset = Entry(buy_asset_window, font=('Arial', 14),fg='light yellow', bg='#313131', width=18)
    entry_asset.grid(row=2, column=1)

    Label(buy_asset_window,
          text='Quantity',
          font=('Impact', 16),
          bg='black',
          fg='light yellow',
          ).grid(row=3, column=0, pady=20)

    entry_quantity = Entry(buy_asset_window, font=('Arial', 14),fg='light yellow', bg='#313131', width=18)
    entry_quantity.grid(row=3, column=1)

    submit_button = Button(buy_asset_window,
                           text='Submit',
                           font=('Impact', 16),
                           width=10,
                           fg='#313131',
                           pady=10,
                           bd=3,
                           relief=SUNKEN,
                           command=submit
                           )
    submit_button.grid(row=4, column=0, pady=20)

    back_button = Button(buy_asset_window,
                         text='Back',
                         font=('Impact', 16),
                         width=10,
                         fg='#313131',
                         pady=10,
                         bd=3,
                         relief=SUNKEN,
                         command=buy_asset_window.destroy)
    back_button.grid(row=4, column=1, pady=20)

#------------------------------------------------------------------------
#Sell asset function
def sell_asset(s):
    # Create a new window for depositing/withdrawing funds
    sell_asset_window = Toplevel()
    sell_asset_window.title('Crypto Investment Project - Sell Asset')
    sell_asset_window.geometry('400x500')
    sell_asset_window.configure(bg='black')

    # Column configuration
    sell_asset_window.grid_columnconfigure(0, weight=1)
    sell_asset_window.grid_columnconfigure(1, weight=1)


   #Submit function
    def submit():
        username = entry_username.get()
        asset_name = entry_asset.get()
        quantity = float(entry_quantity.get())


        if not username or not asset_name or not quantity:
            messagebox.showerror("Error", "All fields are required!")
            return




        # Send the Buy request to the server
        s.send(f'SELL,{username},{asset_name},{quantity}'.encode('utf-8'))

        # Receive response from server
        server_response = s.recv(1024).decode('utf-8')
        messagebox.showinfo('Sold', server_response)

        # destroy the window after submitting the data
        sell_asset_window.destroy()



    # Title label
    Label(sell_asset_window,
          text='Sell Asset',
          font=('Impact', 22),
          fg='light yellow',
          bg='black').grid(row=0, column=0, columnspan=2, pady=20)


    #Create Labels / Entry
    Label(sell_asset_window,
          text='Username',
          font=('Impact', 16),
          bg='black',
          fg='light yellow',
          ).grid(row=1, column=0, pady=20)

    entry_username = Entry(sell_asset_window,font=('Arial', 14),fg='light yellow',bg='#313131', width=18)
    entry_username.grid(row=1, column=1)

    Label(sell_asset_window,
          text='Asset',
          font=('Impact', 16),
          bg='black',
          fg='light yellow',
          ).grid(row=2, column=0, pady=20)

    entry_asset = Entry(sell_asset_window, font=('Arial', 14),fg='light yellow', bg='#313131', width=18)
    entry_asset.grid(row=2, column=1)

    Label(sell_asset_window,
          text='Quantity',
          font=('Impact', 16),
          bg='black',
          fg='light yellow',
          ).grid(row=3, column=0, pady=20)

    entry_quantity = Entry(sell_asset_window, font=('Arial', 14),fg='light yellow', bg='#313131', width=18)
    entry_quantity.grid(row=3, column=1)

    submit_button = Button(sell_asset_window,
                           text='Submit',
                           font=('Impact', 16),
                           width=10,
                           fg='#313131',
                           pady=10,
                           bd=3,
                           relief=SUNKEN,
                           command=submit
                           )
    submit_button.grid(row=4, column=0, pady=20)

    back_button = Button(sell_asset_window,
                         text='Back',
                         font=('Impact', 16),
                         width=10,
                         fg='#313131',
                         pady=10,
                         bd=3,
                         relief=SUNKEN,
                         command=sell_asset_window.destroy)
    back_button.grid(row=4, column=1, pady=20)


#---------------------------------------------------------------------------------
#Veiw portfolio function

def view_portfolio(s):
    # Create a new window for depositing/withdrawing funds
    portfolio_window = Toplevel()
    portfolio_window.title('Crypto Investment Project - View Portfolio')
    portfolio_window.geometry('400x500')
    portfolio_window.configure(bg='black')

    # Column configuration
    portfolio_window.grid_columnconfigure(0, weight=1)
    portfolio_window.grid_columnconfigure(1, weight=1)


    #Submit function
    def submit():
        username = entry_username.get().strip()
        if not username:
            messagebox.showerror("Error", "Username cannot be empty!")
            return

        # Send the request to the server
        request = f"PORTO,{username}".encode('utf-8')
        s.send(request)

        try:
            # Receive the portfolio summary from the server
            response = pickle.loads(s.recv(1024))
            if type(response) == str: #  string
                text_area.config(state=NORMAL)
                text_area.delete(1.0, END)
                text_area.insert(END, response)
                text_area.config(state=DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch portfolio: {e}")


    # Title label
    Label(portfolio_window,
          text='Your Portfolio',
          font=('Impact', 22),
          fg='light yellow',
          bg='black').grid(row=0, column=0, columnspan=2, pady=20)

    # Create Labels / Entry
    Label(portfolio_window,
          text='Username',
          font=('Impact', 16),
          bg='black',
          fg='light yellow',
          ).grid(row=1, column=0, pady=20)

    entry_username = Entry(portfolio_window, font=('Arial', 14),fg='light yellow', bg='#313131', width=18)
    entry_username.grid(row=1, column=1)

    # Text box to display account details
    text_area = Text(portfolio_window,
                     bg='light yellow',
                     font=('Arial', 14),
                     height=15,
                     width=40,
                     fg='black',
                     padx=5,
                     pady=5)
    text_area.grid(row=2, column=0, columnspan=2, pady=10)

    submit_button = Button(portfolio_window,
                           text='Submit',
                           font=('Impact', 16),
                           width=10,
                           fg='#313131',
                           pady=10,
                           bd=3,
                           relief=SUNKEN,
                           command=submit
                           )
    submit_button.grid(row=3, column=0, pady=20)

    back_button = Button(portfolio_window,
                         text='Back',
                         font=('Impact', 16),
                         width=10,
                         fg='#313131',
                         pady=10,
                         bd=3,
                         relief=SUNKEN,
                         command=portfolio_window.destroy)
    back_button.grid(row=3, column=1, pady=20)

#----------------------------------------------------------------------
#Exit function
def exit(s):
    s.send('EXIT,'.encode('utf-8'))
    messagebox.showinfo('Exit', 'Goodbye!')
    root.destroy()
    s.close()



#add btc icon to main menu
logo_btc_icon = PhotoImage(file='image/btc.png')

def main_menu():
    label = Label(root,
                  text='Welcome to Crypto Platform',
                  font=('Impact', 20),
                  fg='light yellow',
                  bg='black',
                  image=logo_btc_icon,
                  compound=LEFT
                  ).pack(pady=(20,10))

    #create_account_button
    Button(root,
           text='Create Account',
           font=('Impact', 15),
           width=15,
           height=2,
           bd=2,
           relief=SUNKEN,
           command=lambda: create_account(s)).pack(pady=(30,10))

    #view_account_button
    Button(root,
           text='View Account',
           font=('Impact', 15),
           width=15,
           height=2,
           bd=2,
           relief=SUNKEN,
           command=lambda: view_account(s)).pack(pady=(10, 10))



    #view_assets_button
    Button(root,
           text='View Assets',
           font=('Impact', 15),
           width=15,
           height=2,
           bd=2,
           relief=SUNKEN,
           command=lambda: view_assets(s)).pack(pady=(10, 10))
    # #funds_button
    Button(root,
           text='Deposit/Withdraw fund',
           font=('Impact', 15),
           width=15,
           height=2,
           bd=2,
           relief=SUNKEN,
           command=lambda: fund(s)).pack(pady=(10, 10))

    #buy_asset_button
    Button(root,
           text='Buy Asset',
           font=('Impact', 15),
           width=15,
           height=2,
           bd=2,
           relief=SUNKEN,
           command=lambda: buy_asset(s)).pack(pady=(10, 10))

    #sell_assets_button
    Button(root,
           text='Sell Asset',
           font=('Impact', 15),
           width=15,
           height=2,
           bd=2,
           relief=SUNKEN,
           command=lambda: sell_asset(s)).pack(pady=(10, 10))


    #view_portfolio_button
    Button(root,
           text='Portfolio',
           font=('Impact', 15),
           width=15,
           height=2,
           bd=2,
           relief=SUNKEN,
           command=lambda: view_portfolio(s)).pack(pady=(10, 10))

    #exit_button
    Button(root,
           text='Exit',
           font=('Impact', 15),
           width=15,
           height=2,
           bd=2,
           relief=SUNKEN,
           command=lambda: exit(s)).pack(pady=(10, 10))



main_menu()

root.mainloop()