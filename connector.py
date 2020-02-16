import psycopg2
from config import *


class Connector:
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)

    @staticmethod
    def column_formatter(columns):
        if not columns:
            return "*"
        output = ""
        for field in columns:
            output += field + ", "
        output = output[:-2]
        return output

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
    def get_table_data(tablename, columns):
        cur = Connector.conn.cursor()
        columns = Connector.column_formatter(columns)
        cur.execute("SELECT " + columns +
                    " FROM " + tablename + ";")
        res = cur.fetchall()
        cur.close()
        return res

    @staticmethod
    def close_connection():
        Connector.conn.close()


if __name__ == "__main__":
    Connector.table_names()
    print(Connector.get_table_data("jednostki", ["identyfikator", "nazwa"]))
