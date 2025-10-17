import psycopg
import tkinter as tk

def befuellen():
    try:
        with psycopg.connect(dbname="prg_fitness",
                             user="postgres",
                             password="password",
                             host="localhost",
                             port="5432",
                             autocommit=True) as db_conn:
            with db_conn.cursor() as cursor:
                cursor: psycopg.cursor

                personen = []
                for person in cursor.execute('''SELECT id,name,alter FROM person'''):
                    personen.append(person)

                for elem in personen:
                    lb_person.insert(tk.END,elem)

                zeitslots = []
                for zeitslot in cursor.execute('''SELECT id,wochentag, slotzeit FROM zeitslot'''):
                    zeitslots.append(zeitslot)

                for elem in zeitslots:
                    lb_zeitslot.insert(tk.END,elem)

    except psycopg.DatabaseError as e:
        print(e, type(e))

def eintragen():

    if len(lb_person.curselection()) == 0 or len(lb_zeitslot.curselection()) == 0:
        lbl_info.config(text="Bitte wählen Sie eine Person und eine Zeitslot aus!")
        return

    try:
        with psycopg.connect(dbname="prg_fitness",
                             user="postgres",
                             password="password",
                             host="localhost",
                             port="5432",
                             autocommit=True) as db_conn:
            with db_conn.cursor() as cursor:
                cursor:psycopg.cursor

                personen_id = lb_person.get(lb_person.curselection()[0])[0]
                zeitslot_id = lb_zeitslot.get(lb_zeitslot.curselection()[0])[0]

                cursor.execute('''INSERT INTO buchung(person_id, zeitslot_id) VALUES (%s, %s)''', (personen_id, zeitslot_id))



    except psycopg.DatabaseError as e:
        print(e, type(e))

def austragen():
    ...

fenster = tk.Tk()
fenster.title("Fitness-App")
fenster.geometry("300x300")

frame_oben = tk.Frame(fenster)
frame_oben.pack(side="top", fill="x")

frame_mitte = tk.Frame(fenster)
frame_mitte.pack(side=tk.TOP, fill=tk.X)

frame_unten = tk.Frame(fenster)
frame_unten.pack(side=tk.TOP, fill=tk.X)

lbl_info = tk.Label(frame_oben, text="Fitness-App")
lbl_info.pack(fill=tk.Y)

btn_eintragen = tk.Button(frame_mitte, command=eintragen, text="Eintragen")
btn_eintragen.pack(side=tk.LEFT, fill=tk.BOTH)
btn_austragen = tk.Button(frame_mitte,command=austragen, text="Austragen")
btn_austragen.pack(side=tk.RIGHT, fill=tk.BOTH)

lb_person = tk.Listbox(frame_unten, exportselection=tk.FALSE)
lb_person.pack(side=tk.LEFT, fill=tk.Y)
lb_zeitslot = tk.Listbox(frame_unten, exportselection=tk.FALSE)
lb_zeitslot.pack(side=tk.RIGHT, fill=tk.Y)

befuellen()

fenster.mainloop()