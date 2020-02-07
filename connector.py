import psycopg2
from config import *

conn = psycopg2.connect(host=host, database=database, user=user, password=password)

cur = conn.cursor()

cur.execute("SELECT table_name " +
            "FROM information_schema.tables " +
            "WHERE table_schema='public' " +
            "AND table_type='BASE TABLE';")

res = cur.fetchall()

print(res)

cur.close()
conn.close()
