import tkinter as tk
from tkinter import messagebox

# from pylab import plot, show, xlabel, ylabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from bankaccount import BankAccount

win = tk.Tk()
win.title('FedUni Banking')

# define width and height of window
width = 440
height = 640

# get screen width and height
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

# calculate x and y coordinates for the Tk root window
position_x = (screen_width/2) - (width/2)
position_y = (screen_height/2) - (height/2)

# set the dimensions of the screen and its position
win.geometry('%dx%d+%d+%d' % (width, height, position_x, position_y))


# The account number entry and associated variable
account_number_var = tk.StringVar()
account_number_entry = tk.Entry(win, textvariable=account_number_var)
account_number_entry.focus_set()

# The pin number entry and associated variable.
# Note: Modify this to 'show' PIN numbers as asterisks (i.e. **** not 1234)
pin_number_var = tk.StringVar()
account_pin_entry = tk.Entry(win, textvariable=pin_number_var, show="*")

# The balance label and associated variable
balance_var = tk.StringVar()
balance_var.set('Balance: $0.00')
balance_label = tk.Label(win, textvariable=balance_var)

# The Entry widget to accept a numerical value to deposit or withdraw
amount_entry = tk.Entry(win)

# The transaction text widget holds text of the accounts transactions
transaction_text_widget = tk.Text(win, height=10, width=48)

# The bank account object we will work with
account = BankAccount()
account_file = None

# ---------- Button Handlers for Login Screen ----------


def clear_pin_entry():
    ''' Function to clear the PIN number entry when the Clear / Cancel button is clicked.
    '''
    pin_number_var.set("")

def handle_pin_button(event=None):
    ''' Function to add the number of the button clicked to the PIN number entry via its associated variable.
        @:param event=None helps to renable the button again not to remain active/
    '''

    input = event.widget["text"]
    pin = pin_number_var.get()
    new_pin = pin+str(input)

    # Limit to 4 chars in length
    if len(new_pin) > 4:
        return messagebox.showerror("Error", "wrong input format. Four digits only!")

    # Set the new pin number on the pin_number_var
    pin_number_var.set(new_pin)
    

def log_in(event=None):
    """ Function to log in to the banking system using a known account number and PIN."""
    global account
    global pin_number_var
    global account_number_var
    global account_number_entry
    global account_file


    # Create the filename from the entered account number with '.txt' on the end
    file_name = account_number_var.get()+".txt"

    # Try to open the account file for reading
    try:
        # Open the account file for reading
        account_file = open(file_name, 'r')

        # Read and split the data in a list
        data_list = account_file.read().split('\n')

        # First line is account number
        if data_list[0] and data_list[0] == account_number_var.get():
            account.account_number = data_list[0]
        else:
            raise Exception("Invalid account id - please try again!")

        # Second line is PIN number, raise exception if the PIN entered doesn't match account PIN read
        if data_list[1] and data_list[1] == pin_number_var.get():
            account.pin_number = data_list[1]
        else:
            raise Exception("Invalid pin number - please try again!")

        # Read third and fourth lines (balance and interest rate)
        if data_list[2] and data_list[3]:
            account.balance = float(data_list[2])
            account.interest_rate = float(data_list[3])

        # Set the balance of label
        balance_var.set('Balance: '+str(account.balance))

        # Section to read account transactions from file - start an infinite 'do-while' loop here

        # Attempt to read a line from the account file, break if we've hit the end of the file. If we
        # read a line then it's the transaction type, so read the next line which will be the transaction amount.
        # and then create a tuple from both lines and add it to the account's transaction_list

        """ sets the pointer to the beginning of the file, hence one can read more than once """
        account_file.seek(0, 0)

        while True:
            line = read_line_from_account_file()
            if not line:
                break
            """ detect only transaction lines """
            if line.startswith("Deposit") or line.startswith("Withdraw"):
                next_amount_line = read_line_from_account_file()
                account.transaction_list.append((line, next_amount_line))

        # Close the file now we're finished with it
        account_file.close()

    except Exception as errorMsg:
        # Catch exception if we couldn't open the file or PIN entered did not match account PIN

        if "No such file or directory" in str(errorMsg):
            errorMsg = "Invalid account id - please try again!"

        # Show error messagebox and & reset BankAccount object to default...
        messagebox.showerror("Error", errorMsg)
        account = BankAccount()

        #  ...also clear PIN entry and change focus to account number entry
        clear_pin_entry()
        account_number_entry.focus_set()
        return

    # Got here without raising an exception?
    # Then we can log in - so remove the widgets and display the account screen
    remove_all_widgets()
    create_account_screen()

# ---------- Button Handlers for Account Screen ----------


def save_and_log_out():
    '''Function  to overwrite the account file with the current state of
       the account object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''
    global account

    # Save the account with any new transactions
    account.export_to_account_file()
    
    # Reset the bank acount object
    account = BankAccount()

    # Reset the account number and pin to blank
    clear_pin_entry()
    account_number_var.set('')
    account_number_entry.focus_set()

    # Remove all widgets and display the login screen again
    remove_all_widgets()
    create_login_screen()
    

def perform_deposit():

    ''' Function to add a deposit for the amount in the amount entry to the
        account's transaction list.
    '''

    global account    
    global amount_entry
    global balance_label
    global balance_var

    # Try to increase the account balance and append the deposit to the account file
    try:

        # Get the cash amount to deposit. Note: We check legality inside account's deposit method
        amount_to_deposit = amount_entry.get()

        # Deposit funds
        deposit_results = account.deposit(amount_to_deposit)

        if "success" not in deposit_results:
            raise Exception(deposit_results)

        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.

        transaction_text_widget['state'] = 'normal'
        transaction_text_widget.delete(0.0, tk.END)
        transaction_text_widget.insert(tk.END, account.get_transaction_string())
        transaction_text_widget['state'] = 'disabled'

        # Change the balance label to reflect the new balance
        balance_var.set('Balance: ' + str(account.balance))

        # Clear the amount entry
        amount_entry.delete(0, 'end')

        # Update the interest graph with our new balance
        plot_interest_graph(account.interest_rate)

    except Exception as errorMsg:
        return messagebox.showerror("Transaction Error", errorMsg)


def perform_withdrawal():

    ''' Function to withdraw the amount in the amount entry from
        the account balance and add an entry to the transaction list. '''

    global account    
    global amount_entry
    global balance_label
    global balance_var

    # Try to increase the account balance and append the deposit to the account file
    try:

        # Get the cash amount to deposit. Note: We check legality inside account's withdraw method
        amount_to_withdraw = amount_entry.get()

        # Withdraw funds
        withdraw_results = account.withdraw(amount_to_withdraw)

        if "success" not in str(withdraw_results):
            raise Exception(withdraw_results)

        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        transaction_text_widget['state'] = 'normal'
        transaction_text_widget.delete(0.0, tk.END)
        transaction_text_widget.insert(tk.END, account.get_transaction_string())
        transaction_text_widget['state'] = 'disabled'

        # Change the balance label to reflect the new balance
        balance_var.set('Balance: ' + str(account.balance))

        # Clear the amount entry
        amount_entry.delete(0, 'end')

        # Update the interest graph with our new balance
        plot_interest_graph(account.interest_rate)

    except Exception as errorMsg:
        return messagebox.showerror("Transaction Error", errorMsg)

# ---------- Utility functions ----------


def remove_all_widgets():
    """Function to remove all the widgets from the window."""
    global win
    for widget in win.winfo_children():
        widget.grid_remove()

def read_line_from_account_file():
    """Function to read a line from the accounts file but not the last newline character.
       Note: The account_file must be open to read from for this function to succeed."""
    global account_file
    return account_file.readline()[0:-1]

def calculate_monthly_interests(amount, interest):
    """ get the interests and their amounts in the next 12 months """
    next_month_amount = amount
    totals = []
    totals.append((1, next_month_amount))

    """
        monthly interest = interest / 12
    """
    monthly_interest = interest/12

    for i in range(2, 13):
        c = next_month_amount * monthly_interest
        next_month_amount = round(c + next_month_amount, 2)
        totals.append((i, next_month_amount))

    return totals

def plot_interest_graph(interest_rate):
    """Function to plot the cumulative interest for the next 12 months here."""

    # YOUR CODE to generate the x and y lists here which will be plotted
    data_list = calculate_monthly_interests(float(account.balance),
                                                 float(interest_rate))
    x = []
    y = []
    for eachLine in data_list:
        if len(eachLine) > 1:
            a, b = eachLine
            x.append(a)
            y.append(b)
    
    # This code to add the plots to the window is a little bit fiddly so you are provided with it.
    # Just make sure you generate a list called 'x' and a list called 'y' and the graph will be plotted correctly.
    figure = Figure(figsize=(5,2), dpi=100)
    figure.suptitle('Cumulative Interest 12 Months')
    a = figure.add_subplot(111)
    a.plot(x, y, marker='o')
    a.grid()
    
    canvas = FigureCanvasTkAgg(figure, master=win)
    canvas.draw()
    graph_widget = canvas.get_tk_widget()
    graph_widget.grid(row=4, column=0, columnspan=5, sticky='nsew')

# ---------- UI Screen Drawing Functions ----------

def create_login_screen():
    '''Function to create the login screen.'''    
    
    # ----- Row 0 -----

    # 'FedUni Banking' label here. Font size is 32.
    tk.Label(win, text="FedUni Banking", fg="black", font="none 32"
             ).grid(row=0, column=0, columnspan=3, sticky='nsew')

    # ----- Row 1 -----

    # Acount Number / Pin label here
    tk.Label(win, text="Account Number/PIN", height=4, width=20
             ).grid(row=1, column=0, sticky="nsew")

    # Account number entry here
    account_number_entry.grid(row=1, column=1, sticky="nsew")

    # Account pin entry here
    account_pin_entry.grid(row=1, column=2, sticky="nsew")

    # ----- Row 2 -----

    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button_1 = tk.Button(win, text="1")
    button_1.grid(row=2, column=0, sticky="nsew")
    button_1.bind("<Button-1>", handle_pin_button)

    button_2 = tk.Button(win, text="2")
    button_2.grid(row=2, column=1, sticky="nsew")
    button_2.bind("<Button-1>", handle_pin_button)

    button_3 = tk.Button(win, text="3")
    button_3.grid(row=2, column=2, sticky="nsew")
    button_3.bind("<Button-1>", handle_pin_button)

    # ----- Row 3 -----

    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button_4 = tk.Button(win, text="4")
    button_4.grid(row=3, column=0, sticky="nsew")
    button_4.bind("<Button-1>", handle_pin_button)

    button_5 = tk.Button(win, text="5")
    button_5.grid(row=3, column=1, sticky="nsew")
    button_5.bind("<Button-1>", handle_pin_button)

    button_6 = tk.Button(win, text="6")
    button_6.grid(row=3, column=2, sticky="nsew")
    button_6.bind("<Button-1>", handle_pin_button)

    # ----- Row 4 -----

    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button_7 = tk.Button(win, text="7")
    button_7.grid(row=4, column=0, sticky="nsew")
    button_7.bind("<Button-1>", handle_pin_button)

    button_8 = tk.Button(win, text="8")
    button_8.grid(row=4, column=1, sticky="nsew")
    button_8.bind("<Button-1>", handle_pin_button)

    button_9 = tk.Button(win, text="9")
    button_9.grid(row=4, column=2, sticky="nsew")
    button_9.bind("<Button-1>", handle_pin_button)

    # ----- Row 5 -----

    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    tk.Button(win, text="Cancel/Clear", bg="red",
              activebackground="red", command=clear_pin_entry
              ).grid(row=5, column=0, sticky="nsew")

    # Button 0 here
    button_0 = tk.Button(win, text="0")
    button_0.grid(row=5, column=1, sticky="nsew")
    button_0.bind("<Button-1>", handle_pin_button)

    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    tk.Button(win, text="Login", bg="green",
              activebackground="green", command=log_in
              ).grid(row=5, column=2, sticky="nsew")

    # ----- Set column & row weights -----
    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)
    win.columnconfigure(0, weight=1)
    win.columnconfigure(1, weight=1)
    win.columnconfigure(2, weight=1)
    win.rowconfigure(0, weight=1)
    """ commented for the entry widget not be so big like the grid buttons """
    # win.rowconfigure(1, weight=1)
    win.rowconfigure(2, weight=1)
    win.rowconfigure(3, weight=1)
    win.rowconfigure(4, weight=1)
    win.rowconfigure(5, weight=1)


def create_account_screen():
    ''' Function to create the account screen. '''

    global amount_text
    global amount_label
    global transaction_text_widget
    global balance_var
    
    # ----- Row 0 -----

    # FedUni Banking label here. Font size should be 24.
    tk.Label(win, text="FedUni Banking", font="none 24"
             ).grid(row=0, column=0, sticky='nsew', columnspan=5)

    # ----- Row 1 -----

    # Account number label here
    account_label = "Account Number: "+str(account_number_var.get())
    tk.Label(win, text=account_label, height=4, width=28
             ).grid(row=1, column=0, sticky='nsew')

    # Balance label here
    balance_label.grid(row=1, column=1, sticky='nsew')

    # Log out button here
    tk.Button(win, text="Log Out", command=save_and_log_out
              ).grid(row=1, column=2, sticky="nsew", columnspan=2)

    # ----- Row 2 -----

    # Amount label here
    tk.Label(win, text="Amount ($)").grid(row=2, column=0, sticky='nsew')

    # Amount entry here
    amount_entry.grid(row=2, column=1, sticky='nsew')

    # Deposit button here
    tk.Button(win, text="Deposit", command=perform_deposit, width=12
              ).grid(row=2, column=2, sticky="nsew")

    # Withdraw button here
    tk.Button(win, text="Withdraw", command=perform_withdrawal, width=8
              ).grid(row=2, column=3, sticky="nsew")

    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.
    
    
    # ----- Row 3 -----

    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)
    yscrollbar = tk.Scrollbar(win)
    yscrollbar.grid(row=3, column=1, columnspan=5, sticky='nse')
    
    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal')
    # for it to be edited
    transaction_text_widget['wrap'] = tk.NONE
    transaction_text_widget['bd'] = 0
    transaction_text_widget['state'] = 'disabled'
    transaction_text_widget['yscrollcommand'] = yscrollbar.set
    transaction_text_widget.grid(row=3, column=0, columnspan=5, sticky='nsew')

    # Now add the scrollbar and set it to change with the yview of the text widget
    yscrollbar.config(command=transaction_text_widget.yview)

    # refresh the label and the scroll_text widgets data
    transaction_text_widget['state'] = 'normal'
    transaction_text_widget.delete(0.0, tk.END)
    transaction_text_widget.insert(tk.END, account.get_transaction_string())
    transaction_text_widget['state'] = 'disabled'

    # Change the balance label to reflect the new balance
    balance_var.set('Balance: ' + str(account.balance))

    # ----- Row 4 - Graph -----

    # Call plot_interest_graph() here to display the graph
    plot_interest_graph(0)
    

    # ----- Set column & row weights -----

    # Set column and row weights here - there are 5 rows and 5 columns (numbered 0 through 4 not 1 through 5!)


# ---------- Display Login Screen & Start Main loop ----------

create_login_screen()
win.mainloop()
