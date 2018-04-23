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


def insert_data(id,fingerid,status,push):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(id,fingerid,Clock,status,push) VALUES ('{0}','{1}','{2}','{3}','{4}')".format(id,fingerid,str(jdatetime.datetime.now()),status,push))
    conn.commit()
    return True


def update_data(id,status):
    cursor = conn.cursor()
    # cursor.execute("INSERT INTO users(fingerid,time,status,push) VALUES ('Andy Hunter', '7/24/2012', 'Xplore Records', 1)")
    conn.execute("UPDATE users set status = ? where ID = ?",(status,id))
    conn.commit()


def LastLogin(fingerid):
    print("finger id",fingerid)
    cursor = conn.cursor()
    rows=cursor.execute("SELECT * FROM users WHERE (Clock = (SELECT MAX(Clock) FROM users) AND fingerid=?)",(fingerid,))
    for row in rows:
        return row

def GetEndId():
    cursor =conn.cursor()
    # rows = cursor.execute("SELECT * FROM users WHERE ID = (SELECT MAX(ID)  FROM users)")
    rows = cursor.execute("SELECT MAX(ID)  FROM users")
    for row in rows:
        return (int(row[0])+1)




if __name__ == '__main__':
    database = "pythonsqlite.sqlite3"

    # create a database connection
    conn = create_connection(database)
    # select_all_tasks(conn)
    # print(jdatetime.datetime.now())
    # insert_data(conn,'3','Exit',push=1)
    # print(LastLogin('Enter','1397-02-01 00:44:34.594588'))
    # rows =LastLogin('Enter','1397-02-01 00:44:34.594588').fetchall()
    print(GetEndId())
    insert_data(GetEndId(),'22','Enter',0)





