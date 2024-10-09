import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import psycopg2

dbname = "dvdrental"
user = "postgres"
password = "root"
host = "localhost"

conn = psycopg2.connect(database=dbname,user=user,password=password,host=host)
cur = conn.cursor()

def try_execute_sql(sql: str):
    try:
        cur.execute(sql)
        result = cur.fetchall()
        for i in result:
            print(i)
        conn.commit()
    except Exception as e:
        print(f"Not found table due to exception:{e}")
        conn.rollback()


def show_table():

    show_table_sql= """ select first_name from actor; """
    try_execute_sql(show_table_sql)
    cur.close()
    conn.close()

if __name__ == "__main__":
    show_table()
