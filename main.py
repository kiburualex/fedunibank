import tkinter as tk
from pages import AccountPage, LoginPage

""" graph imports """
import matplotlib.animation as animation
from graph import animate, figure


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("FedUni Banking")
        self.master.tk_setPalette(background='#ececec')
        self.master.minsize(440, 600)

        """ Gets the requested values of the height and width. """
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()

        position_right = int(self.master.winfo_screenwidth() / 2.5 - window_width / 2)
        position_down = int(self.master.winfo_screenheight() / 3 - window_height / 2)

        """ Positions the window in the center of the page. """
        self.master.geometry("+{}+{}".format(position_right, position_down))

        self.frames = {}

        for F in (LoginPage, AccountPage):
            frame = F(master, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    ani = animation.FuncAnimation(figure, animate, interval=1000)
    app.mainloop()
