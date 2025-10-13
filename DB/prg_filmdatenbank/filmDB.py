'''
In dieser Aufgabe haben Sie den Auftrag, das Programm CREATE_DB zu schreiben, das ähnlich wie im Unterricht die
Datenbank prg_filmdatenbank erstellen soll. Erzeugen Sie dazu eine Verbindung mit psycopg zu postgres und legen Sie im
ersten Schritt die Datenbank mit dem Namen prg_filmdatenbank an.
'''

import psycopg
import filmDB_Inhalt

db_conn: psycopg.Connection  # type hint für PyCharm
# ---------------------------------------------------------------------------------------------------------------------
# Verbindung mit der DB aufbauen
# ---------------------------------------------------------------------------------------------------------------------

try:
    with psycopg.connect(dbname="postgres",
                         user="postgres",
                         password="password",
                         host="localhost",
                         port="5432",
                         autocommit=True) as db_conn:
        # -------------------------------------------------------------------------------------------------------------
        # Datenbank erstellen
        # -------------------------------------------------------------------------------------------------------------

        with db_conn.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS prg_filmdatenbank;')
            cursor.execute('CREATE DATABASE prg_filmdatenbank;')

except psycopg.DatabaseError as e:
    print(e, type(e))

# ---------------------------------------------------------------------------------------------------------------------
# Verbindung mit der FilmDB aufbauen
# ---------------------------------------------------------------------------------------------------------------------

try:
    with psycopg.connect(dbname="prg_filmdatenbank",
                         user="postgres",
                         password="password",
                         host="localhost",
                         port="5432",
                         autocommit=True) as db_conn:
        # -------------------------------------------------------------------------------------------------------------
        # Tabellen erstellen
        # -------------------------------------------------------------------------------------------------------------

        with db_conn.cursor() as cursor:
            cursor.execute('''
                           CREATE TABLE person (
                               person_id  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                               nachname   TEXT NOT NULL,
                               vorname    TEXT NOT NULL,
                               geburtstag DATE NOT NULL
                           );
                           ''')
            cursor.execute('''
                           CREATE TABLE film (
                               film_id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                               titel            TEXT    NOT NULL,
                               erscheinungsjahr INTEGER NOT NULL,
                               fk_regie         BIGINT  NOT NULL REFERENCES person (person_id)
                                   ON UPDATE CASCADE ON DELETE RESTRICT
                           );
                           ''')
            cursor.execute('''
                           CREATE TABLE hat_mitgespielt_in (
                               fk_filme_id  BIGINT REFERENCES film (film_id),
                               fk_person_id BIGINT REFERENCES person (person_id),
                               rolle        TEXT NOT NULL,
                               PRIMARY KEY (fk_filme_id, fk_person_id)
                           );
                           ''')
            # ----------------------------------------------------------------------------------------------------------
            # Tabellen befüllen
            # ----------------------------------------------------------------------------------------------------------
            cursor.executemany("INSERT INTO person (nachname, vorname, geburtstag) VALUES (%s,%s,%s)",
                               filmDB_Inhalt.personen_liste)

            cursor.executemany("""INSERT INTO film(titel, erscheinungsjahr, fk_regie)
                                  VALUES (%s, %s, (SELECT person_id FROM person WHERE nachname = %s))""",
                               filmDB_Inhalt.filme_liste)

            cursor.executemany("""INSERT INTO hat_mitgespielt_in(fk_filme_id, fk_person_id, rolle)
                                  VALUES ((SELECT film_id FROM film WHERE titel LIKE %s),
                                          (SELECT person_id FROM person WHERE nachname = %s), %s)""",
                               filmDB_Inhalt.rollen_liste)

except psycopg.DatabaseError as e:
    print(e, type(e))
