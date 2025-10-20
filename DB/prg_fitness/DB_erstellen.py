import psycopg

zeiten = [('Mo', '0800-1000'), ('Mo', '1000-1200'), ('Mo', '1200-1400'), ('Mo', '1400-1600'), ('Mo', '1600-1800'),
          ('Mo', '1800-2000'), ('Mo', '2000-2200'),
          ('Di', '0800-1000'), ('Di', '1000-1200'), ('Di', '1200-1400'), ('Di', '1400-1600'), ('Di', '1600-1800'),
          ('Di', '1800-2000'), ('Di', '2000-2200'),
          ('Mi', '0800-1000'), ('Mi', '1000-1200'), ('Mi', '1200-1400'), ('Mi', '1400-1600'), ('Mi', '1600-1800'),
          ('Mi', '1800-2000'), ('Mi', '2000-2200'),
          ('Do', '0800-1000'), ('Do', '1000-1200'), ('Do', '1200-1400'), ('Do', '1400-1600'), ('Do', '1600-1800'),
          ('Do', '1800-2000'), ('Do', '2000-2200'),
          ('Fr', '0800-1000'), ('Fr', '1000-1200'), ('Fr', '1200-1400'), ('Fr', '1400-1600'), ('Fr', '1600-1800'),
          ('Fr', '1800-2000'), ('Fr', '2000-2200'),
          ('Sa', '0800-1000'), ('Sa', '1000-1200'), ('Sa', '1200-1400'), ('Sa', '1400-1600'), ('Sa', '1600-1800'),
          ('Sa', '1800-2000'), ('Sa', '2000-2200'),
          ('So', '0800-1000'), ('So', '1000-1200'), ('So', '1200-1400'), ('So', '1400-1600'), ('So', '1600-1800'),
          ('So', '1800-2000'), ('So', '2000-2200'), ]
# -------------------------------------------------------------------------
# Verbindung mit postgres-DB
# -------------------------------------------------------------------------
try:
    db_conn: psycopg.Connection  # type-hint um es ggf einfacher zu machen
    with psycopg.connect(dbname="postgres",
                         user="postgres",
                         password="password",
                         host="localhost",
                         port="5432",
                         autocommit=True) as db_conn:
        cursor: psycopg.Cursor
        with db_conn.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS prg_fitness')
            cursor.execute('CREATE DATABASE prg_fitness')


except psycopg.errors.DuplicateDatabase:
    pass
except psycopg.DatabaseError as e:
    print(e, type(e))
# -------------------------------------------------------------------------
# Verbindung mit prg_fitness-DB
# -------------------------------------------------------------------------
try:
    with psycopg.connect(dbname="prg_fitness",
                         user="postgres",
                         password="password",
                         host="localhost",
                         port="5432",
                         autocommit=True) as db_conn:
        with db_conn.cursor() as cursor:
            # -------------------------------------------------------------------------
            # Tabellen buchung und zeitslot ververwerfen, wenn sie vorhanden sind
            # -------------------------------------------------------------------------
            try:
                cursor.execute('DROP TABLE if EXISTS buchung')
                cursor.execute('DROP TABLE if EXISTS zeitslot')
                cursor.execute('DROP TABLE if EXISTS buchung')
                cursor.execute('DROP TABLE if EXISTS bilder')
            except psycopg.errors.UndefinedTable:
                pass


            # -------------------------------------------------------------------------
            # --- Tabelle person anlegen ---
            # -------------------------------------------------------------------------
            try:
                cursor.execute('''CREATE TABLE person (
                    id    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    name  text    NOT NULL,
                    alter INTEGER NOT NULL
                )''')
            except psycopg.errors.DuplicateTable:
                pass



            # -------------------------------------------------------------------------
            # Tabelle zeitslot anlegen
            # -------------------------------------------------------------------------
            try:
                cursor.execute('''CREATE TABLE zeitslot (
                    id        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    wochentag text NOT NULL,
                    slotzeit  text NOT NULL,
                    UNIQUE (wochentag, slotzeit)
                )''')
            except psycopg.errors.DuplicateTable:
                pass

            # -------------------------------------------------------------------------
            # Zeitslots in Tabelle zeitslot einfügen
            # -------------------------------------------------------------------------
            cursor.executemany('INSERT INTO zeitslot (wochentag, slotzeit) VALUES (%s, %s)', zeiten)
            # print(cursor.rowcount)
            assert cursor.rowcount == 49, "Zu viele Einträge in der Zeitslot-Tabelle" #einfache sanity check, nicht sinnvoll, da Programm trotzdem weiterläuft

            # -------------------------------------------------------------------------
            # Tabelle buchung anlegen
            # -------------------------------------------------------------------------
            try:
                cursor.execute('''CREATE TABLE buchung (
                    person_id   INTEGER NOT NULL REFERENCES person (id) ON DELETE CASCADE,
                    zeitslot_id INTEGER NOT NULL REFERENCES zeitslot (id) ON DELETE CASCADE,
                    PRIMARY KEY (person_id, zeitslot_id)
                )''')
            except psycopg.errors.DuplicateTable:
                pass

            # -------------------------------------------------------------------------
            # Tabelle bilder anlegen
            # -------------------------------------------------------------------------
            try:
                cursor.execute('''
                               CREATE TABLE bilder (
                                   person INTEGER PRIMARY KEY,
                                   bild   BYTEA,
                                   FOREIGN KEY (person) REFERENCES person (id)
                               )''')
            except psycopg.errors.DuplicateTable:
                pass


except psycopg.errors.DuplicateDatabase:
    pass
except psycopg.DatabaseError as e:
    print(e, type(e))
