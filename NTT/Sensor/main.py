import time
import sys
from Adafruit_IO import MQTTClient
AIO_FEED_ID = ["temp","humid","relay1","relay2"]
AIO_USERNAME = "trunggden"
AIO_KEY = "aio_okrC34V396bfScMNFBA7SW1SftmV"

def  connected(client):
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_ID:
        client.subscribe(feed)

# clients = MQTTClient(AIO_USERNAME , AIO_KEY)
# clients.on_connect = connected
# clients.connect()
# clients.loop_background()
def  message(client , feed_id , payload):
    print("Nhan du lieu: " +payload + " feed_id " + feed_id)
    if(feed_id=="relay1" and payload=="1"):
        setDevice1(True)
    elif(feed_id=="relay1" and payload=="0"):
        setDevice1(False)
    if (feed_id == "relay2" and payload == "1"):
        setDevice2(True)
    elif (feed_id == "relay2" and payload == "0"):
        setDevice2(False)



clients = MQTTClient(AIO_USERNAME , AIO_KEY)
clients.on_connect = connected
clients.on_message = message
clients.connect()
clients.loop_background()

print("Sensors and Actuators")
import serial.tools.list_ports
def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

portName = getPort()
print(portName)
if portName != "None":
    ser = serial.Serial(port=portName, baudrate=9600)

relay1_ON  = [0, 6,  0, 0, 0, 255,200, 91]
relay1_OFF = [0, 6, 0, 0, 0, 0, 136, 27]

def setDevice1(state):
    if state == True:
        ser.write(relay1_ON)
    else:
        ser.write(relay1_OFF)

relay2_ON  = [15, 6, 0, 0, 0, 255, 200, 164]
relay2_OFF = [15, 6, 0, 0, 0, 0, 136, 228]

def setDevice2(state):
    if state == True:
        ser.write(relay2_ON)
    else:
        ser.write(relay2_OFF)



def serial_read_data(ser):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        #print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
            return value
        else:
            return -1
    return 0

soil_temperature =[3, 3, 0, 0, 0, 1, 133, 232]
def readTemperature():
    serial_read_data(ser)
    ser.write(soil_temperature)
    time.sleep(1)
    value = serial_read_data(ser)
    clients.publish("temp", value/10)
    return value



soil_moisture = [3, 3, 0, 1, 0, 1, 212, 40]
def readMoisture():
    serial_read_data(ser)
    ser.write(soil_moisture)
    time.sleep(1)
    value = serial_read_data(ser)
    clients.publish("humid",value/10)
    return value

while True:
    # print("TEST MOTOR")
    # setDevice1(True)
    # time.sleep(2)
    # setDevice1(False)
    # time.sleep(2)
    #
    # setDevice2(True)
    # time.sleep(2)
    # setDevice2(False)
    # time.sleep(2)
    print("TEST SENSOR")
    print(readTemperature())
    time.sleep(2)
    print(readMoisture())
    time.sleep(2)
