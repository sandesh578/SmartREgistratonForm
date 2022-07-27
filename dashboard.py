from tkinter import ttk
import tkinter as tk
from db import Admin
from crypto import Crypto

treev = None
window = None


def Delete(email):
    db.deleteUser(email)


def generateData():
    database = db.get_database()
    db.setCollection(database)
    test = list(db.getUsers())
    crypto = Crypto()
    privateKey, publicKey = crypto.loadKeys()
    i = 1
    for data in test:
        treev.insert('', 'end', iid=i,
                     values=(i, data['name'], data['roll'], data['email'], crypto.Decrypt(data['password'], privateKey)))
        i = i+1


def Dashboard():
    global window
    global treev
    window = tk.Tk()
    window.title("Admin Dashboard")
    window.resizable(width=1, height=1)
    treev = ttk.Treeview(window, selectmode='browse')
    treev.grid(row=1, column=1, columnspan=4, padx=20, pady=20)

    global db
    db = Admin()

    # Defining number of columns
    treev["columns"] = ("1", "2", "3", "4", "5")

    # Defining heading
    treev['show'] = 'headings'

    # Assigning the width and anchor to  the
    # respective columns
    treev.column("1", width=100, anchor='c')
    treev.column("2", width=100, anchor='c')
    treev.column("3", width=100, anchor='c')
    treev.column("4", width=100, anchor='c')
    treev.column("5", width=300, anchor='c')

    # Assigning the heading names to the
    # respective columns
    treev.heading("1", text="SN")
    treev.heading("2", text="Name")
    treev.heading("3", text="Roll")
    treev.heading("4", text="Email")
    treev.heading("5", text="Decrypted Password")
    generateData()
    window.mainloop()
