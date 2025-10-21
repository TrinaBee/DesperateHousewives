import psycopg
from psycopg.rows import dict_row

class Datenbank:
    def __init__(self, password: str):
        self.config = {'user': 'postgres',
                       'password': password,
                       'dbname': 'prg_fitness',
                       'host': 'localhost',
                       'port': 5432,
                       'autocommit': True}

    def personen(self):
        db_conn: psycopg.Connection
        try:
            with psycopg.connect(**self.config) as db_conn:
                with db_conn.cursor(row_factory=dict_row) as cursor:
                    return cursor.execute('SELECT id,name FROM person').fetchall()
        except psycopg.DatabaseError as e:
            raise ValueError('Fehler beim Aufrufen der Personen aus der Datenbank!')