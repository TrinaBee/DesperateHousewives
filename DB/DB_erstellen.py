import psycopg

try:
    with psycopg.connect(dbname="postgres",
                         user="postgres",
                         password="password",
                         host="localhost",
                         port="5432",
                         autocommit=True) as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute('CREATE DATABASE prg_fitness')


except psycopg.errors.DuplicateDatabase:
    pass
except psycopg.DatabaseError as e:
    print(e, type(e))

try:
    with psycopg.connect(dbname="prg_fitness",
                         user="postgres",
                         password="password",
                         host="localhost",
                         port="5432",
                         autocommit=True) as db_conn:
        with db_conn.cursor() as cursor:
            try:
                cursor.execute('''CREATE TABLE person (
                                    id    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                                    name  text    NOT NULL,
                                    alter INTEGER NOT NULL
                                    )''')
            except psycopg.errors.DuplicateTable:
                pass

except psycopg.errors.DuplicateDatabase:
    pass
except psycopg.DatabaseError as e:
    print(e, type(e))
