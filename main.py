import time ,urllib3,json,serial,mraa


http = urllib3.PoolManager()


s = None
finger=None
step1 = '55AA000020000000000000000000000000000000000000001f01'
step2 = '55AA000060000200000000000000000000000000000000006101'
step3 = '55AA00006300060000000100F401000000000000000000005E02'

wellcom='cc010000bb'
goodbye='cc020000bb'
error='cc030000bb'



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



def DellAll():
    send_command='55AA0000440004000100F4010000000000000000000000003D02'
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
    global s,finger
    # open serial COM port to /dev/ttyS0, which maps to UART0(D0/D1)
    # the baudrate is set to 57600 and should be the same as the one
    # specified in the Arduino sketch uploaded to ATmega32U4.
    s = serial.Serial('/dev/ttyS1', 9600)
    finger=serial.Serial('/dev/ttyS0', 115200)



def loop():
    # send "1" to the Arduino sketch on ATmega32U4.
    # the sketch will turn on the LED attached to D13 on the board
    finger.write(step1.decode("hex"))
    time.sleep(0.1)
    read=finger.read(26)
    if ((hex(ord(read[0]))=='0xaa')) and (hex(ord(read[4]))=='0x20')and(hex(ord(read[8]))=='0x0'):
        print("True")
        finger.write(step2.decode("hex"))
        time.sleep(0.4)
        finger.flushInput()
        finger.flushOutput()
        finger.write(step3.decode("hex"))
        time.sleep(0.1)
        read = finger.read(26)
        print(" ".join(hex(ord(n)) for n in read))
        finger.flushInput()
        finger.flushOutput()
	if hex(ord(read[4]))=='0x63' and hex(ord(read[6]))=='0x2':
            return None
#        ab = http.request('GET','http://185.8.175.58/api/fingerprint/101/km1{0}/'.format(int(hex(ord(read[10]))[2:],16)))
        ab = http.request('GET','http://192.168.1.101/json/100/km1{0}/'.format(int(hex(ord(read[10]))[2:],16)))
        if ab.status==200:
            json_data=json.loads(ab.data)
            if json_data['enable']=="True":
                if json_data['status']=="Enter":#ab.data =='Enter':
                    print("Enter")
                    s.write(wellcom.decode("hex"))
                    time.sleep(1)

                elif json_data['status']=="Exit":#ab.data =='Exit':
                    print("Exit")
                    s.write(goodbye.decode("hex"))
                    time.sleep(1)

                # elif json_data['status']=="Enter":#ab.data=='False':
                #     s.write(error.decode("hex"))
                #     time.sleep(1)

                # else:
                #     print(int(hex(ord(read[10]))[2:],16))
                #     print(ab.read())

    elif (hex(ord(read[0]))=='0xaa')and(hex(ord(read[4]))=='0x20')and(hex(ord(read[8]))=='0x28'):
        print("False")


if __name__ == '__main__':
    setup()
    while True:
        loop()
