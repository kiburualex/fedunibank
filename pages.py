import tkinter as tk
from functools import partial
from tkinter.messagebox import showwarning
from tkinter.scrolledtext import ScrolledText

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graph import figure


class LoginPage(tk.Frame):

    def __init__(self, master, controller):
        super().__init__(master)

        self.pack()
        self.pin = ""
        self.controller = controller

        """ create the ui widgets """
        self.create_inputs_widgets()
        self.create_grid_widgets()

        """ bind keyboard events """
        """
            TODO: fix bindings to this frame not the master,
            then uncomment
        """
        # self.master.bind('<Return>', self.login)
        # self.master.bind('<Escape>', self.cancel)

    def create_inputs_widgets(self):

        """ create the label and the entry widgets """

        tk.Label(self, text="FedUni Banking", fg="black", font="none 32") \
            .pack(padx=20, pady=20)

        input_frame = tk.Frame(self)
        input_frame.pack(padx=20, pady=15, anchor="w")

        tk.Label(input_frame, text="Account Number/PIN", fg="black",
                 font="none 10").grid(row=0, column=0, sticky="w")

        """ accound id entry """
        self.account_id_entry = tk.Entry(input_frame, font="none 20", width=9, bg="white")
        self.account_id_entry.grid(row=0, column=1, sticky="e")

        """ pin entry """
        self.entry_var = tk.StringVar()

        self.pin_entry = tk.Entry(input_frame, textvariable=self.entry_var,
                                  font="none 20", width=8, bg="white",
                                  show="*", fg="black", disabledbackground='white',
                                  state='disabled')
        self.pin_entry.grid(row=0, column=2, sticky="e")

    def create_grid_widgets(self):

        """ create the button grid widgets """

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(padx=20, pady=15, anchor="w")

        """ create a loop to create the buttons dynamically """

        for row_index in range(3):
            tk.Grid.rowconfigure(buttons_frame, row_index, weight=1)
            for col_index in range(3):
                tk.Grid.columnconfigure(buttons_frame, col_index, weight=1)

                if row_index == 0:
                    step = col_index + 1
                elif row_index == 1:
                    step = col_index + 4
                else:
                    step = col_index + 7

                btn = tk.Button(buttons_frame, width=15, height=7,
                                text=step,
                                command=partial(self.add_pin, step))

                btn.grid(row=row_index, column=col_index, sticky="w")

        tk.Button(buttons_frame, text="Cancel / Clear", bg="#ff1e05", width=15,
                  height=7, fg="white", command=self.clear_pin
                  ).grid(row=3, column=0, sticky="w")

        tk.Button(buttons_frame, text="0", bg="#ececec", width=15, height=7, fg="black",
                  command=lambda: self.add_pin(0),
                  ).grid(row=3, column=1, sticky="w")

        tk.Button(buttons_frame, text="Log In", bg="#127c10", width=15, height=7, fg="white",
                  command=self.login
                  ).grid(row=3, column=2, sticky="w")

    def add_pin(self, number):

        self.pin += str(number)
        self.entry_var.set(str(self.pin))

    def clear_pin(self):
        self.pin = ""
        self.entry_var.set(str(self.pin))

    def login(self, event=None):
        if not self.pin_entry.get() or not self.account_id_entry.get():
            return self.popup_msg("Wrong Input detected. Please try again!")

        """ clear the entry widgets """
        self.clear_pin()
        self.account_id_entry.delete(0, tk.END)

        return self.controller.show_frame(AccountPage)

    def popup_msg(self, msg):
        showwarning("Error", msg)

    def cancel(self, event=None):
        self.master.destroy()
        exit()


class AccountPage(tk.Frame):

    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        """ create the top label and entry widgets """
        self.create_top_widgets()

        """ create the center text widget """
        self.create_center_widgets()

        """ create graph widget """
        self.create_graph_widgets()

    def create_top_widgets(self):

        tk.Label(self, text="FedUni Banking", fg="black", font="none 22") \
            .pack(padx=10, pady=15)

        """ info frame """
        info_frame = tk.Frame(self)
        info_frame.pack(padx=20, pady=0, anchor="w")

        """ message widget """
        self.message = tk.Message(info_frame, text="Account Number: 12345", aspect=350,
                                  justify="left")
        self.message.grid(row=0, column=0, sticky="w")

        """ balance label """
        self.balance_label = tk.Label(info_frame, text="Balance: $50000", width=15, fg="black")
        self.balance_label.grid(row=0, column=1, sticky="w")

        tk.Button(info_frame, text="Log Out", width=18, height=2, fg="black",
                  command=lambda: self.controller.show_frame(LoginPage)
                  ).grid(row=0, column=2, sticky="w")

        tk.Label(info_frame, text="Amount($)", fg="black", width=15
                 ).grid(row=4, column=0, sticky="w")

        """ amount entry """
        self.entry_var = tk.StringVar()

        self.pin_entry = tk.Entry(info_frame, textvariable=self.entry_var,
                                  font="none 22", width=8, bg="white", fg="black")
        self.pin_entry.grid(row=4, column=1, sticky="w")

        """ action_buttons_frame is a separate frame for proper button alignment """
        action_buttons_frame = tk.Frame(info_frame)
        action_buttons_frame.grid(row=4, column=2, sticky="w")

        tk.Button(action_buttons_frame, text="Deposit", width=7, height=2, fg="black",
                  ).grid(row=0, column=0, sticky="w")
        tk.Button(action_buttons_frame, text="Withdraw", width=7, height=2, fg="black",
                  command=self.change_plot_data
                  ).grid(row=0, column=1, sticky="w")

        """ TODO: use to adjsut the message """
        # self.message.configure(text="nice")

    def create_center_widgets(self):

        """ center frame """
        center_frame = tk.Frame(self)
        center_frame.pack(padx=20, pady=0, anchor="w")

        output = ScrolledText(center_frame, width=63, height=15, wrap=tk.WORD, background="white")
        output.grid(row=0, column=0, columnspan=1, sticky="w")

    def create_graph_widgets(self):

        """ graph frame """
        graph_frame = tk.Frame(self, bg="white")
        graph_frame.pack(padx=0, pady=0, anchor="w")

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def change_plot_data(self):
        print("change clicked")

