import psycopg2
from config import *
from ErrorPopUp import ErrorPopUp
from ErrorFormatter import  ErrorFormatter

error_window = None


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
    def value_formatter(values):
        output = ""
        for field in values:
            output += "'" + field + "', "
        output = output[:-2]
        return output

    @staticmethod
    def delete_formatter(ids, idname, idtype):
        output = ""
        if idtype is int:
            for field in ids:
                output += idname + " = " + field + " OR "
        else:
            for field in ids:
                output += idname + " LIKE '" + field + "' OR "
        output = output[:-4]
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
        try:
            cur.execute("SELECT " + columns +
                        " FROM " + tablename + ";")
        except psycopg2.Error as err:
            global error_window
            error_window = ErrorPopUp(ErrorFormatter.get_error(err.pgcode))
            error_window.show()

        res = cur.fetchall()
        cur.close()
        return res

    @staticmethod
    def get_filtered(tablename, columns, filters):
        cur = Connector.conn.cursor()
        columns = Connector.column_formatter(columns)
        try:
            cur.execute("SELECT " + columns +
                        " FROM " + tablename + filters + ";")
        except psycopg2.Error as err:
            global error_window
            print(err.pgerror)
            error_window = ErrorPopUp(ErrorFormatter.get_error(err.pgcode))
            error_window.show()

        res = cur.fetchall()
        cur.close()
        return res

    @staticmethod
    def get_record(tablename, columns, id, idname, idtype):
        cur = Connector.conn.cursor()
        columns = Connector.column_formatter(columns)
        try:
            if idtype is int:
                cur.execute("SELECT " + columns +
                            " FROM " + tablename +
                            " WHERE " + idname + " = " + str(id) + ";")
            else:
                cur.execute("SELECT " + columns +
                            " FROM " + tablename +
                            " WHERE " + idname + " LIKE " + id + ";")
        except psycopg2.Error as err:
            global error_window
            error_window = ErrorPopUp(ErrorFormatter.get_error(err.pgcode))
            error_window.show()

        res = cur.fetchone()
        cur.close()
        return res

    @staticmethod
    def insert_row(tablename, columns, values):
        cur = Connector.conn.cursor()
        columns = Connector.column_formatter(columns)
        values = Connector.value_formatter(values)
        try:
            cur.execute("INSERT INTO " + tablename +
                    " (" + columns + ") " +
                    "VALUES (" + values + ");")
        except psycopg2.Error as err:
            global error_window
            error_window = ErrorPopUp(ErrorFormatter.get_error(err.pgcode))
            error_window.show()

        cur.close()
        Connector.conn.commit()

    @staticmethod
    def delete_items(tablename, ids, idname, idtype):
        if ids:
            cur = Connector.conn.cursor()
            ids = Connector.delete_formatter(ids, idname, idtype)
            try:
                cur.execute("DELETE FROM " + tablename + " WHERE " + ids + ";")
            except psycopg2.Error as err:
                global error_window
                print(err.pgerror)
                error_window = ErrorPopUp(ErrorFormatter.get_error(err.pgcode))
                error_window.show()
            Connector.conn.commit()

    @staticmethod
    def close_connection():
        Connector.conn.close()
        print("Connection closed")


if __name__ == "__main__":
    Connector.table_names()
    print(Connector.get_table_data("jednostki", ["identyfikator", "nazwa"]))
    print(Connector.get_record("jednostki", None, 1, "identyfikator", int))
