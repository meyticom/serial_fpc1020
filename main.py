#!/usr/bin/python
import time ,urllib3,json,serial,mraa,jdatetime
import sqlite3
from sqlite3 import Error


http = urllib3.PoolManager()

green = mraa.Gpio(6)
blue = mraa.Gpio(18)
red = mraa.Gpio(19)
interupt=mraa.Gpio(37)


green.dir(mraa.DIR_OUT)
blue.dir(mraa.DIR_OUT)
red.dir(mraa.DIR_OUT)
interupt.dir(mraa.DIR_IN)




serial_budrate='55AA000002000500030500000000000000000000000000000E01'#set serital budrate to 115200
serial_security_level='55AA000002000500010100000000000000000000000000000801'#set security leve to 1

s = None
finger=None
step1 = '55AA000020000000000000000000000000000000000000001f01'
step2 = '55AA000060000200000000000000000000000000000000006101'
step3 = '55AA00006300060000000100F401000000000000000000005E02'

wellcome='cc010000bb'
goodbye='cc020000bb'
error='cc030000bb'



##############databaise ###############################################
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
                           time TEXT, status TEXT , push BOOL)
    ''')
    conn.commit()

def insert_data(conn,id,status,push):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(fingerid,time,status,push) VALUES ('{0}','{1}','{2}', {3})".format(id,jdatetime.datetime.now(),status,push))
    conn.commit()


def update_data(conn,id,status):
    cursor = conn.cursor()
    # cursor.execute("INSERT INTO users(fingerid,time,status,push) VALUES ('Andy Hunter', '7/24/2012', 'Xplore Records', 1)")
    conn.execute("UPDATE users set status = ? where ID = ?",(status,id))
    conn.commit()


def EmptyId():
    send_command='55AA0000450004000100F4010000000000000000000000003E02'
    #recive_command='AA55010045000400000001000000000000000000000000004A01'
    finger.write(send_command.decode("hex"))
    time.sleep(0.1)
    read = finger.read(26)
    finger.flushInput()
    finger.flushOutput()
    if (hex(ord(read[0]))=='0xaa')and(hex(ord(read[4]))=='0x45')and(hex(ord(read[24]))=='0x4a'):
        return int(hex(ord(read[10]))[2:],16) #important
    else:
        return None


def checksum(data):
    k=sum(map(ord, data))
    data+=k
    print("dddddddddd",k)
    return sum(map(ord, data))


def DellAll():
    send_command='\x55\xAA\x00\x00\x44\x00\x04\x00\x01\x00\xF4\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    #recive_command='AA55010044000200000000000000000000000000000000004601'
    finger.write(send_command.decode("hex"))
    time.sleep(0.1)
    finger.flushInput()
    finger.flushOutput()

def DellId(id):
    send_command='55AA000044000400010001000000000000000000000000004901'
    finger.write(send_command.decode("hex"))
    time.sleep(0.1)
    finger.flushInput()
    finger.flushOutput()

def Register():
    send_command_1='55AA000046000200030000000000000000000000000000004A01'#start enroll with template number 3
    finger.write(send_command_1.decode("hex"))
    time.sleep(0.1)
    #recive command_1 ='AA 55 01 00 46 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 49 01'
    read = s.read(26)
    finger.flushInput()
    finger.flushOutput()
    #if (hex(ord(read[0]))=='0xaa')and(hex(ord(read[4]))=='0x46')and(hex(ord(read[6]))=='0x03'):



def setup():
    global s,finger,read,conn,hours_enter,minute_enter,hours_exit,minute_exit

    hours_enter=9
    minute_enter=0
    hours_exit=12
    minute_exit=0

    # open serial COM port to /dev/ttyS0, which maps to UART0(D0/D1)
    # the baudrate is set to 57600 and should be the same as the one
    # specified in the Arduino sketch uploaded to ATmega32U4.
    database = "pythonsqlite.sqlite3"

    # create a database connection
    conn = create_connection(database)

    #select_all_tasks(conn)

    # s = serial.Serial('COM3', 9600)
    # finger=serial.Serial('COM4', 115200)#921600


    s = serial.Serial('/dev/ttyS1', 9600)
    finger=serial.Serial('/dev/ttyS0', 115200)#921600
    blue.write(1)
    time.sleep(2)
    finger.write(serial_security_level.decode("hex"))
    time.sleep(1)
    #finger.flushInput()
    #finger.flushOutput()
    wellcome='cc010000bb'
    s.write(wellcome.decode("hex"))


def loop():
    # send "1" to the Arduino sketch on ATmega32U4.
    # the sketch will turn on the LED attached to D13 on the board
    rfid=""
    while interupt.read()==1:
        finger.close()
        return
    finger.flushInput()
    # finger.flushOutput()
    while(s.inWaiting()):
        rfid +=s.read()
    print("rfid",rfid)
    while False:
        ab = http.request('GET', 'http://185.8.175.58/json/101/km1{0}/'.format('999'),
                          timeout=3.0)
    blue.write(1)
    green.write(0)
    red.write(0)
    finger.write(step1.decode("hex"))
    time.sleep(0.1)
    read=finger.read(26)
    finger.flushInput()
    print(" ".join(hex(ord(n)) for n in read))
    if ((hex(ord(read[0]))=='0xaa')) and (hex(ord(read[4]))=='0x20')and(hex(ord(read[8]))=='0x0'):
        print("True")
        finger.flushInput()
        finger.write(step2.decode("hex"))
        time.sleep(0.4)
        read = finger.read(26)
        print(" ".join(hex(ord(n)) for n in read))
        finger.flushInput()
        finger.write(step3.decode("hex"))
        time.sleep(0.2)
        read = finger.read(26)
        print(" ".join(hex(ord(n)) for n in read))
        finger.flushInput()
        if hex(ord(read[4]))=='0x63' and hex(ord(read[6]))=='0x2':
            blue.write(0)
            green.write(0)
            red.write(1)
            time.sleep(1)
            return None
        blue.write(0)
        green.write(1)
        red.write(0)
        now = jdatetime.datetime.now()
        try:
            ab = http.request('GET','http://185.8.175.58/json/101/km1{0}/'.format(int(hex(ord(read[10]))[2:],16)),timeout=3.0)
        except urllib3.exceptions.HTTPError:
            check_enter = now.replace(hour=hours_enter, minute=minute_enter)
            check_exit = now.replace(hour=hours_exit, minute=minute_exit)
            if now < check_enter:
                print("Enter")
                insert_data(conn,(int(hex(ord(read[10]))[2:],16)),'enter')
            elif now >check_exit:
                print("Exit")
                insert_data(conn, (int(hex(ord(read[10]))[2:], 16)),'exit')
            print('Connection failed. Http')
            error='cc030000bb'
            s.write(error.decode("hex"))
            #insert_data(conn, '2')
            time.sleep(6)
            return None
#        ab = http.request('GET','http://192.168.1.101/json/100/km1{0}/'.format(int(hex(ord(read[10]))[2:],16)))
        try:
            json_data=json.loads(ab.data)
            if json_data['enable']=="True":
                if json_data['status']=="Enter":#ab.data =='Enter':
                    print("Enter")
                    wellcome='cc01{0}bb'.format(read[9:11].encode("hex"))
                    s.write(wellcome.decode("hex"))
                    time.sleep(1.5)

                elif json_data['status']=="Exit":#ab.data =='Exit':
                    print("Exit")
                    goodbye='cc02{0}bb'.format(read[9:11].encode("hex"))
                    s.write(goodbye.decode("hex"))
                    time.sleep(1.5)

                # elif json_data['status']=="Enter":#ab.data=='False':
                #     s.write(error.decode("hex"))
                #     time.sleep(1)

                # else:
                #     print(int(hex(ord(read[10]))[2:],16))
                #     print(ab.read())
            elif json_data['enable']=='False':
                if json_data['status']=="NotActivate":
                        message='cc1b0000bb'
                        s.write(message.decode("hex"))
                        time.sleep(3)
                elif json_data['status']=="Register":
                        message='cc1c0000bb'
                        s.write(message.decode("hex"))
                        time.sleep(3)
        except:
             return None

    elif (hex(ord(read[0]))=='0xaa')and(hex(ord(read[4]))=='0x20')and(hex(ord(read[8]))=='0x28'):
        print("False")


if __name__ == '__main__':
    setup()
    while True:
        loop()


#4901
# def checksum(data):
#     k=sum(map(ord, data))
#     print("sum",hex(k))
#     print("a")
#     if len(hex(k)[2:])%2 != 0:
#         first= hex(k)[2:][1:3]
#         scond=('0' + hex(k)[2:][:1])
#         data += '\x'+first+'\x' +scond
#         print("first",first)
#         print("scond",scond)
#         print("out",data)
#         return data
#     else:
#         first=hex(k)[2:][2:]
#         scond=hex(k)[2:][:2]
#         data += first + scond
#         print("out",data)
#         return data
#
#
# checksum('\x55\xAA\x00\x00\x44\x00\x04\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
