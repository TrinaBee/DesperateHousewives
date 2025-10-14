import psycopg
from psycopg.rows import dict_row
import tkinter as tk

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
            # cursor.execute('''SELECT id,name,alter
            #                   FROM person''')
            # # while True:
            # #     zeile = cursor.fetchone()
            # #     if zeile is None:
            # #         break
            # #     print(zeile)
            # for zeile in cursor.fetchall():
            #     print(zeile)
        #     for zeile in cursor.execute("SELECT id,alter,name FROM person"):
        #         print(zeile)
        #
        # with db_conn.cursor(row_factory=dict_row) as cursor:
        #     cursor.execute('''SELECT id, name, alter
        #                       FROM person''')
        #     for row in cursor.fetchall():
        #         print(row)
            cursor.execute('''SELECT bild
                              FROM bilder
                              WHERE person = 11''')
            fenster = tk.Tk()
            bild = tk.PhotoImage(data=cursor.fetchone()[0])
            tk.Label(fenster, image=bild).pack()
            fenster.mainloop()

except psycopg.DatabaseError as e:
    print(e, type(e))