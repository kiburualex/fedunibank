import tkinter as tk
from functools import partial
from tkinter.messagebox import showwarning


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master.title("FedUni Banking")
        self.master.tk_setPalette(background='#ececec')
        self.master.minsize(440, 600)
        self.pin = ""

        # Gets the requested values of the height and width.
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()

        position_right = int(self.master.winfo_screenwidth() / 2.5 - window_width / 2)
        position_down = int(self.master.winfo_screenheight() / 3 - window_height / 2)

        # Positions the window in the center of the page.
        self.master.geometry("+{}+{}".format(position_right, position_down))

        self.create_inputs_widgets()
        self.create_grid_widgets()

    def create_inputs_widgets(self):

        """ create the label and the entry widgets """

        tk.Label(self, text="FedUni Banking", fg="black", font="none 32")\
            .pack(padx=20, pady=20)

        input_frame = tk.Frame(self)
        input_frame.pack(padx=20, pady=15, anchor="w")

        tk.Label(input_frame, text="Account Number/PIN", fg="black", font="none 10") \
            .grid(row=0, column=0, sticky="w")

        self.account_id_entry = tk.Entry(input_frame, font="none 20", width=9, bg="white")
        self.account_id_entry.grid(row=0, column=1, sticky="e")

        self.entry_var = tk.StringVar()
        self.pin_entry = tk.Entry(input_frame, textvariable=self.entry_var, font="none 20", width=8, bg="white", show="*")
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

        tk.Button(buttons_frame, text="Cancel / Clear", bg="#ff1e05", width=15, height=7, fg="white",
                  command=self.clear_pin
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

    def login(self):
        print(self.pin_entry.get())
        print(self.account_id_entry.get())
        if not self.pin_entry.get() or not self.account_id_entry.get():
            return self.popupmsg("Wrong Input detected. Please try again!")

        return print("Login Successful")

    def popupmsg(self, msg):
        showwarning("Error", msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
