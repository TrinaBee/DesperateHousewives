import psycopg
import tkinter as tk


def filmtitel_auslesen():
    film_titel = []
    try:
        db_conn = psycopg.connect(dbname="prg_filmdatenbank",
                                  user="postgres",
                                  password="password",
                                  host="localhost",
                                  port="5432",
                                  autocommit=True)
        with db_conn.cursor() as cursor:
            cursor: psycopg.Cursor
            for titel in cursor.execute('''SELECT titel
                                           FROM film'''):
                film_titel.append(titel[0])
        lb_filmtitel.delete(0, tk.END)
        lb_filmtitel.insert(0, *film_titel)
        lb_filmtitel.selection_set(0)
        lb_filmtitel.event_generate("<<Selected>>")
    except psycopg.DatabaseError as e:
        print(e, type(e))


def detail_anzeigen(event):
    auswahl_film = lb_filmtitel.get(lb_filmtitel.curselection()[0])
    lbl_titel_inhalt.config(text=auswahl_film)
    try:
        db_conn = psycopg.connect(dbname="prg_filmdatenbank",
                                  user="postgres",
                                  password="password",
                                  host="localhost",
                                  port="5432",
                                  autocommit=True)
        with db_conn.cursor() as cursor:
            cursor: psycopg.Cursor
            # Abfrage Erscheinugnsjahr
            cursor.execute('''SELECT erscheinungsjahr
                              FROM film
                              WHERE titel = %s''', (auswahl_film,))
            erscheinungsjahr = cursor.fetchone()[0]
            lbl_erscheinungsjahr_inhalt.config(text=erscheinungsjahr)
            # Abfrage Ressigeur
            cursor.execute('''SELECT vorname, nachname
                              FROM person
                                       JOIN film ON person.person_id = film.fk_regie
                              WHERE film.titel = %s ''', (auswahl_film,))
            regisseur = cursor.fetchone()
            lbl_regisseur_inhalt.config(text=f'{regisseur[0]} {regisseur[1]}')

            # Abfrage Schauspieler
            cursor.execute('''SELECT p.vorname, p.nachname, hmi.rolle
                              FROM person p
                                       JOIN hat_mitgespielt_in hmi ON p.person_id = hmi.fk_person_id
                                       JOIN film f ON f.film_id = hmi.fk_filme_id
                              WHERE f.titel = %s''', (auswahl_film,))
            schauspieler = cursor.fetchall()
            # print(schauspieler)
            schauspieler_text = ""
            for figur in schauspieler:
                schauspieler_text += f'{figur[0]} {figur[1]} -> {figur[2]}\n'
            lbl_schauspiel_inhalt.config(text=schauspieler_text)
    except psycopg.DatabaseError as e:
        print(e, type(e))


# Fenster bauen
fenster = tk.Tk()
fenster.title("FilmApp")
fenster.geometry("700x500")
# Frames
frame_links = tk.Frame(fenster, padx=10, pady=10)
frame_links.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
frame_rechts = tk.Frame(fenster, padx=10, pady=10)
frame_rechts.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
# Listbox Filmtitel links
lbl_filme = tk.Label(frame_links, text="Filme:").pack(anchor=tk.W, pady=(0, 5))
lb_filmtitel = tk.Listbox(frame_links, width=35, relief=tk.SUNKEN)
lb_filmtitel.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=10, pady=10)
lb_filmtitel.bind("<<ListboxSelect>>", detail_anzeigen)

# Detail-Anzeige rechts
tk.Label(frame_rechts, text="Titel:", anchor=tk.W).pack(side=tk.TOP, fill=tk.X)

lbl_titel_inhalt = tk.Label(frame_rechts, anchor=tk.W)
lbl_titel_inhalt.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

tk.Label(frame_rechts, text="Erscheinungsjahr:", anchor=tk.W).pack(side=tk.TOP, fill=tk.X)

lbl_erscheinungsjahr_inhalt = tk.Label(frame_rechts, anchor=tk.W)
lbl_erscheinungsjahr_inhalt.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

tk.Label(frame_rechts, text="Regisseur:", anchor=tk.W).pack(side=tk.TOP, fill=tk.X)

lbl_regisseur_inhalt = tk.Label(frame_rechts, anchor=tk.W)
lbl_regisseur_inhalt.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

tk.Label(frame_rechts, text="Schauspieler:", anchor=tk.W).pack(side=tk.TOP, fill=tk.X)

lbl_schauspiel_inhalt = tk.Label(frame_rechts, anchor=tk.W, justify=tk.LEFT)
lbl_schauspiel_inhalt.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

# Suchfeld rechts unten
suchfeld = tk.Entry(frame_rechts)
suchfeld.pack(side=tk.TOP)

filmtitel_auslesen()

fenster.mainloop()
