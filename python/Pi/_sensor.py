import adafruit_dht

import csv, board, time, statistics
import multiprocessing
from datetime import datetime
from datetime import date
from smbus import SMBus
from message import *
#Set DATA pin

dht1 = adafruit_dht.DHT22(board.D4, False)
dht2 = adafruit_dht.DHT22(board.D5, False)
dht3 = adafruit_dht.DHT22(board.D6, False)

READ_FREQ = 60 #in seconds

outputmax = 15099494
outputmin = 1677722
i2cbus = SMBus(1)  # Create a new I2C bus
i2caddress = 0x28
cmd = [0x00, 0x00]

TEMP_THRESH_1 = 90
HUMIDITY_THRESH_1 = 60
TEMP_THRESH_2 = 60
HUMIDITY_THRESH_2 = 60
TEMP_THRESH_3 = 85
HUMIDITY_THRESH_3 = 60
PRESS_THRESH = 80
TIMEOUT = 900

global d8
d8 = ''
global times
times = []

print("starting...")

#header = ['Time','Temp1','Humidity1','Temp2','Humidity2','Temp3','Humidity3']
global temp_tic, hum_tic
temp_tic = time.perf_counter()-TIMEOUT
hum_tic = time.perf_counter()-TIMEOUT

def isFirstError(date):
    global d8
    if date.today() == d8:
        return False
    else:
        d8 = date.today()
        return True

def readPress(date):
    i2cbus.write_i2c_block_data(0x28, 0xAA, cmd)  # Update configuration register
    time.sleep(0.5)
    data = i2cbus.read_i2c_block_data(0x28, 0x60)
    press_counts = data[3] + data[2] * 256 + data[1] * 65536  # calculate digital pressure counts
    temp_counts = data[6] + data[5] * 256 + data[4] * 65536  # calculate digital temperature counts
    temperature = (temp_counts * 200 / 16777215) - 50  # calculate temperature in deg c
    percentage = (press_counts / 16777215) * 100  # calculate pressure as percentage of full scale

    pressure = ((press_counts - outputmin) * (150 - 0)) / (outputmax - outputmin) + 0;
    #print(temperature)
    #print(percentage)
    print(pressure)
    if (pressure < PRESS_THRESH) and isFirstError(date):
        print("Message")
        sendMessage('PRESS_THRESH '+str(PRESS_THRESH)+' met: P = '+str(pressure))
    return [round(pressure,2),round(temperature,2)]

def readHumSensor(sensor,date,TEMP_THRESH,HUM_THRESH):
    try:
        tt=sensor.temperature
    except RuntimeError as error:
        #print(error.args[0])
        tt = ''
    except Exception as error:
        sensor.exit()
        raise error
    try:
        th=sensor.humidity
    except RuntimeError as error:
        th = ''
    except Exception as error:
        sensor.exit()
        raise error
    return [tt,th]

def Sensors():
    TIME_THRESH = time.perf_counter()+READ_FREQ
    TEMP_THRESH = [TEMP_THRESH_1,TEMP_THRESH_2,TEMP_THRESH_3]
    HUM_THRESH = [HUMIDITY_THRESH_1,HUMIDITY_THRESH_2,HUMIDITY_THRESH_3]
    while TIME_THRESH > time.perf_counter():
        t = {'sensor 1':[],
            'sensor 2':[],
            'sensor 3':[]}
        h = {'sensor 1':[],
            'sensor 2':[],
            'sensor 3':[]}
        sens = {'sensor 1':readHumSensor(dht1,date,TEMP_THRESH_1,HUMIDITY_THRESH_1),
                'sensor 2':readHumSensor(dht2,date,TEMP_THRESH_2,HUMIDITY_THRESH_2),
                'sensor 3':readHumSensor(dht3,date,TEMP_THRESH_3,HUMIDITY_THRESH_3)}
        for s in sens:
            if sens[s][0] != '' and not(sens[s][0] is None):
                t[s].append(int(float(sens[s][0]))* (9 / 5) + 32)
            if sens[s][1] != '' and not(sens[s][1] is None):
                h[s].append(int(float(sens[s][1])))
        time.sleep(.5)

    ft = [round(statistics.mean(t['sensor 1']),2),
        round(statistics.mean(t['sensor 2']),2),
        round(statistics.mean(t['sensor 3'])+2,2)]

    fh = [round(statistics.mean(h['sensor 1'])+20,2),
        round(statistics.mean(h['sensor 2']),2),
        round(statistics.mean(h['sensor 3'])-10,2)]

    for i in [0,2]:
        if ft[i] > TEMP_THRESH[i]:
            if isFirstError(date):
                print("Message"+str(i))
                Thresh = TEMP_THRESH[i]
                temp = ft[i]
                sendMessage(f"TEMP_THRESH {Thresh} exceeded")
    for i in [0,2]:
        if fh[i] > HUM_THRESH[i]:
            if isFirstError(date):
                print("Message"+str(i))
                Thresh = HUM_THRESH[i]
                hum = fh[i]
                sendMessage(f"HUM_THRESH {Thresh} exceeded")
    return [ft[0],fh[0],ft[1],fh[1],ft[2],fh[2]]

def logData(datas,press,date):
    date = date.today()
    loc = "/home/pi/Sand 3D Printer Monitor System/data logs/data_log"+str(date)+".csv"
    try:
        with open(loc, 'a', newline = '') as csvfile:
            data = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            now = datetime.now()
            t = now.strftime("%H:%M:%S")
            data.writerow([date]+[t] + [datas[0]] + [datas[1]] + [datas[2]] + [datas[3]] + [datas[4]] + [datas[5]] + [press[0]] + [press[1]])

    except IOError:
        print("Could not open file! Please close Excel. Press Enter to retry.")

while True:
    try:
        vals = Sensors()
        print(vals)
        [ap,at] = readPress(date)
        logData(vals,[ap,at],date)
 #       while True:
  #          print(readHumSensor(dht1,date,TEMP_THRESH_1,HUMIDITY_THRESH_1))
  #          time.sleep(1)
            #print(readPress(date))
    except statistics.StatisticsError as error:
        print(error.args[0])