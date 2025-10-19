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
                cursor:psycopg.Cursor

                personen_id = lb_person.get(lb_person.curselection()[0])[0]
                zeitslot_id = lb_zeitslot.get(lb_zeitslot.curselection()[0])[0]

                cursor.execute('''INSERT INTO buchung(person_id, zeitslot_id) VALUES (%s, %s)''', (personen_id, zeitslot_id))
                lbl_info.config(text="Sie sind eingetragen!")
    except psycopg.errors.UniqueViolation:
                lbl_info.config(text="Sie sind für diesen Slot schon eingetragen!")


    except psycopg.DatabaseError as e:
        print(e, type(e))

def austragen():
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
                cursor:psycopg.Cursor

                personen_id = lb_person.get(lb_person.curselection()[0])[0]
                zeitslot_id = lb_zeitslot.get(lb_zeitslot.curselection()[0])[0]

                cursor.execute('''DELETE FROM buchung WHERE person_id = %s and zeitslot_id = %s''', (personen_id,zeitslot_id))
                lbl_info.config(text="Sie sind ausgetragen!")
    # except psycopg.errors.UniqueViolation:
    #             lbl_info.config(text="Sie hatten diesen Slot nicht gebucht!")


    except psycopg.DatabaseError as e:
        print(e, type(e))
def refresh():
    aktuelle_buchung = []
    frequence_slots = {}
    try:
        with psycopg.connect(dbname="prg_fitness",
                             user="postgres",
                             password="password",
                             host="localhost",
                             port="5432",
                             autocommit=True) as db_conn:
            with db_conn.cursor() as cursor:
                cursor:psycopg.Cursor

                for zeile in cursor.execute('''SELECT person_id, zeitslot_id FROM buchung'''):
                    aktuelle_buchung.append(zeile)

    except psycopg.DatabaseError as e:
        print(e, type(e))

    auswahl = int(mehrals_auswahl.get()[1])
    for buchung in aktuelle_buchung:
        if buchung[1] not in frequence_slots:
            frequence_slots[buchung[1]] = 1
        else:
            frequence_slots[buchung[1]] += 1
    # print(frequence_slots)
    for i in range(lb_zeitslot.size()):
        lb_zeitslot.itemconfigure(i,background='white')
        if auswahl == 0:
            lb_zeitslot.itemconfigure(i, background='green')
    for zeitslot in frequence_slots:
        if auswahl == 0:
            lb_zeitslot.itemconfigure(zeitslot, background='white')
        elif frequence_slots[zeitslot] > auswahl:
            lb_zeitslot.itemconfigure(zeitslot,background='red')










fenster = tk.Tk()
fenster.title("Fitness-App")


frame_oben = tk.Frame(fenster)
frame_oben.pack(side=tk.TOP, fill=tk.BOTH,padx=10,pady=10)

frame_unten = tk.Frame(fenster)
frame_unten.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

frame_mitte = tk.Frame(fenster)
frame_mitte.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

lbl_info = tk.Label(frame_oben, text="Fitness-App",height=4, relief=tk.SUNKEN)
lbl_info.pack(fill=tk.BOTH)

btn_eintragen = tk.Button(frame_unten, command=eintragen, text="Eintragen")
btn_eintragen.pack(side=tk.LEFT, fill=tk.BOTH,padx=5,pady=5)
btn_austragen = tk.Button(frame_unten, command=austragen, text="Austragen")
btn_austragen.pack(side=tk.LEFT, fill=tk.BOTH,padx=5,pady=5)
btn_refresh = tk.Button(frame_unten, command=refresh, text="Aktuallisieren")
btn_refresh.pack(side=tk.LEFT, fill=tk.BOTH,padx=5,pady=5)
mehrals = ["=0",">1",">2",">3",">4",">5",">6",">7"]
mehrals_auswahl = tk.StringVar(value=mehrals[0])
om_mehr_als = tk.OptionMenu(frame_unten, mehrals_auswahl,*mehrals)
om_mehr_als.pack(side=tk.LEFT, fill=tk.BOTH,padx=5,pady=5)

lb_person = tk.Listbox(frame_mitte, exportselection=tk.FALSE)
lb_person.pack(side=tk.LEFT, fill=tk.Y)
lb_zeitslot = tk.Listbox(frame_mitte, exportselection=tk.FALSE)
lb_zeitslot.pack(side=tk.RIGHT, fill=tk.Y)

befuellen()
refresh()
fenster.mainloop()