import datenbank
import tkinter as tk

fenster = tk.Tk()
db = datenbank.Datenbank('password')

personen = db.personen()
tk.Label(fenster, text=str(personen)).pack()

fenster.mainloop()