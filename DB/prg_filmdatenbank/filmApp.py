import psycopg
import tkinter as tk

from psycopg.types.range import load_range_binary


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
    except psycopg.DatabaseError as e:
        print(e, type(e))


def detail_anzeigen():
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
                              WHERE erscheinungsjahr = %s''', (auswahl_film,))
            erscheinungsjahr = tk.StringVar(cursor.fetchone()[0])
            lbl_erscheinungsjahr_inhalt.config(textvariable=erscheinungsjahr)

            # Abfrage Ressigeur
            cursor.execute('''SELECT vorname, nachname
                              FROM person
                                       JOIN film ON person.person_id = film.fk_regie
                              WHERE film.titel = %s ''', (auswahl_film,))
            regisseur = tk.StringVar(cursor.fetchone()[0],cursor.fetchone()[1])
            lbl_regisseur_inhalt.config(textvariable=regisseur)

    except psycopg.DatabaseError as e:
        print(e, type(e))


# Fenster bauen
fenster = tk.Tk()
fenster.title("FilmApp")
fenster.geometry("400x300")
# Frames
frame_links = tk.Frame(fenster)
frame_links.pack(side=tk.LEFT)
frame_rechts = tk.Frame(fenster)
frame_rechts.pack(side=tk.LEFT)
# Listbox Filmtitel links
lb_filmtitel = tk.Listbox(frame_links, width=30, relief=tk.SUNKEN)
lb_filmtitel.pack(side=tk.TOP, fill=tk.Y, expand=True, padx=10, pady=10)
lb_filmtitel.bind("<<ButtonRelease-1>>", detail_anzeigen)

# Detail-Anzeige rechts
tk.Label(frame_rechts, text="Titel:", anchor=tk.W).pack(side=tk.TOP, fill=tk.X)

lbl_titel_inhalt = tk.Label(frame_rechts, anchor=tk.W)
lbl_titel_inhalt.pack(side=tk.TOP, fill=tk.X)

tk.Label(frame_rechts, text="Erscheinungsjahr:", anchor=tk.W).pack(side=tk.TOP, fill=tk.X)

lbl_erscheinungsjahr_inhalt = tk.Label(frame_rechts, anchor=tk.W)
lbl_erscheinungsjahr_inhalt.pack(side=tk.TOP, fill=tk.X)

tk.Label(frame_rechts, text="Regisseur:", anchor=tk.W).pack(side=tk.TOP, fill=tk.X)

lbl_regisseur_inhalt = tk.Label(frame_rechts, anchor=tk.W)
lbl_regisseur_inhalt.pack(side=tk.TOP, fill=tk.X)

tk.Label(frame_rechts, text="Schauspieler:", anchor=tk.W).pack(side=tk.TOP, fill=tk.X)

lbl_schauspiel_inhalt = tk.Label(frame_rechts, anchor=tk.W)
lbl_schauspiel_inhalt.pack(side=tk.TOP, fill=tk.X)

# Suchfeld rechts unten
suchfeld = tk.Entry(frame_rechts)
suchfeld.pack(side=tk.TOP)

filmtitel_auslesen()

fenster.mainloop()
