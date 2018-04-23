import sqlite3
from sqlite3 import Error

import jdatetime


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def select_all_tasks(conn):
    # """
    # Query all rows in the tasks table
    # :param conn: the Connection object
    # :return:
    # """
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM tasks")
    #
    # rows = cur.fetchall()
    #
    # for row in rows:
    #     print(row)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, fingerid TEXT,
                           Clock TEXT, status TEXT , push BOOL)
    ''')
    conn.commit()

def insert_data(conn,id,status,push):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(fingerid,Clock,status,push) VALUES ('{0}','{1}','{2}', {3})".format(id,str(jdatetime.datetime.now()),status,push))
    conn.commit()


def update_data(conn,id,status):
    cursor = conn.cursor()
    # cursor.execute("INSERT INTO users(fingerid,time,status,push) VALUES ('Andy Hunter', '7/24/2012', 'Xplore Records', 1)")
    conn.execute("UPDATE users set status = ? where ID = ?",(status,id))
    conn.commit()

def LastLogin(fingerid):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE (Clock = (SELECT MAX(Clock) FROM users) AND fingerid=?)",fingerid)
    return cursor

def GetEndId():
    cursor =conn.cursor()
    rows=cursor.execute("SELECT * FROM users WHERE ID = (SELECT MAX(ID)  FROM users)")
    for row in rows:
        return row[1]


if __name__ == '__main__':
    database = "pythonsqlite.sqlite3"

    # create a database connection
    conn = create_connection(database)
    # select_all_tasks(conn)
    # print(jdatetime.datetime.now())
    # insert_data(conn,'3','Exit',push=1)
    # print(LastLogin('Enter','1397-02-01 00:44:34.594588'))
    # rows =LastLogin('Enter','1397-02-01 00:44:34.594588').fetchall()

    rows = LastLogin('3')
    for row in rows:
        print(row)

    # print(GetEndId())





