import psycopg2
from config import *
from ErrorPopUp import ErrorPopUp
from ErrorFormatter import ErrorFormatter

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
    def update_formatter(columns, values):
        output = ""
        for i, x in enumerate(columns, 0):
            if type(values[i]) is str:
                temp = "'" + values[i] + "'"
            else:
                temp = values[i]
            output += x + " = " + temp + ", "
        output = output[:-2]
        return output

    @staticmethod
    def get_enum(name):
        cur = Connector.conn.cursor()
        cur.execute("SELECT unnest(enum_range(NULL::" + name + "))")
        res = cur.fetchall()
        cur.close()
        arr = []
        for x in res:
            arr.append(x[0])
        return arr

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
    def get_dict(tablename, columns, id, idname, idtype):
        dict = {}
        res = Connector.get_record(tablename, columns, id, idname, idtype)
        for i, x in enumerate(res, 0):
            dict[columns[i]] = x
        return dict

    @staticmethod
    def get_filtered(tablename, columns, filters):
        cur = Connector.conn.cursor()
        columns = Connector.column_formatter(columns)
        try:
            cur.execute("SELECT " + columns +
                        " FROM " + tablename + filters + ";")
        except psycopg2.Error as err:
            global error_window
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
                            " WHERE " + idname + " LIKE '" + id + "';")
        except psycopg2.Error as err:
            global error_window
            error_window = ErrorPopUp(ErrorFormatter.get_error(err.pgcode))
            error_window.show()

        res = cur.fetchone()
        cur.close()
        return res

    @staticmethod
    def insert_row(tablename, columns, values):
        correct = True
        cur = Connector.conn.cursor()
        columns = Connector.column_formatter(columns)
        values = Connector.value_formatter(values)
        try:
            cur.execute("INSERT INTO " + tablename +
                        " (" + columns + ") " +
                        "VALUES (" + values + ");")
        except psycopg2.Error as err:
            correct = False
            global error_window
            error_window = ErrorPopUp(ErrorFormatter.get_error(err.pgcode))
            error_window.show()

        cur.close()
        Connector.conn.commit()
        return correct

    @staticmethod
    def update_row(tablename, columns, values, id, idname, idtype):
        correct = True
        cur = Connector.conn.cursor()
        data = Connector.update_formatter(columns, values)
        try:
            if idtype is int:
                cur.execute("UPDATE " + tablename + " SET " + data +
                            " WHERE " + idname + " = " + str(id) + ";")
            else:
                cur.execute("UPDATE " + tablename + " SET " + data +
                            " WHERE " + idname + " LIKE '" + id + "';")
        except psycopg2.Error as err:
            correct = False
            global error_window
            error_window = ErrorPopUp(ErrorFormatter.get_error(err.pgcode))
            error_window.show()

        cur.close()
        Connector.conn.commit()
        return correct

    @staticmethod
    def create_vehicle(input):
        for x in input:
            if x is None:
                x = "NULL"
            x = str(x)
        cur = Connector.conn.cursor()
        try:
            cur.execute("CALL public.create_vehicle(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", input)
        except psycopg2.Error as err:
            global error_window
            error_window = ErrorPopUp(ErrorFormatter.get_error(err.pgcode))
            error_window.show()
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
                error_window = ErrorPopUp(ErrorFormatter.get_error(err.pgcode))
                error_window.show()
            Connector.conn.commit()

    @staticmethod
    def close_connection():
        Connector.conn.close()
        print("Connection closed")


if __name__ == "__main__":
    # print(Connector.get_dict("jednostki", ["identyfikator"], 1, "identyfikator", int))
    # Connector.create_vehicle(['Samochód', 'Jeep', 'Wrangler2', 2340, 5, 600, 'Dostępny', 2015, 'UA54320', 1, None])
    #print(Connector.get_enum("status_type"))
    Connector.update_row("pojazdy", ["model", "masa"], ["Mały", "2"], 0, "id_pojazdu", int)