import psycopg
daten = [('Anton', 47), ('Brita', 53), ('Charlie', 23), ('Denise', 27), ('Emil', 64), ('Frank', 81)]

#-------------------------------------------------------------------------
# Verbindung mit prg_fitness-DB
#-------------------------------------------------------------------------
try:
    with psycopg.connect(dbname="prg_fitness",
                         user="postgres",
                         password="password",
                         host="localhost",
                         port="5432",
                         autocommit=True) as db_conn:
        with db_conn.cursor() as cursor:
            # -------------------------------------------------------------------------
            # --- Mehrere Daten gleichzeitig einfügen ---
            # -------------------------------------------------------------------------
            # cursor.executemany('INSERT INTO person (name,alter) VALUES (%s, %s)', daten)
            # print(cursor.fetch())

            # -------------------------------------------------------------------------
            # --- Zeilen aus Tabelle löschen ---
            # -------------------------------------------------------------------------
            # cursor.execute('''DELETE
            #                   FROM person
            #                   WHERE id > 16''')
            # print(cursor.rowcount)
            cursor.execute('''DELETE FROM bilder WHERE person = 11''')
            with open('Gesicht.png', 'rb') as datei:
                bild = datei.read()
                cursor.execute('INSERT INTO bilder (person,bild) VALUES (%s,%b)', (11, bild))

except psycopg.errors.DuplicateDatabase:
    pass
except psycopg.DatabaseError as e:
    print(e, type(e))