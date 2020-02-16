import psycopg2
from config import *


class Connector:
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)

    @staticmethod
    def table_names():
        cur = Connector.conn.cursor()
        cur.execute("SELECT table_name " +
                "FROM information_schema.tables " +
                "WHERE table_schema='public' " +
                "AND table_type='BASE TABLE';")

        res = cur.fetchall()
        print(res)
        cur.close()

    @staticmethod
    def close_connection():
        Connector.conn.close()


Connector.table_names()