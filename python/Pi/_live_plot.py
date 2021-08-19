import matplotlib.pyplot as plt
from matplotlib import *
import matplotlib.animation as animation
from datetime import date
import csv, statistics,sys

csv.field_size_limit(sys.maxsize)

style.use('fivethirtyeight')

fig = plt.figure()
fig.canvas.manager.full_screen_toggle()
ax1 = fig.add_subplot(3,1,1)
ax2 = fig.add_subplot(3,1,2)
ax3 = fig.add_subplot(3,1,3)

def animate(i):
    global sd
    ts = []
    t1s = []
    t2s = []
    t3s = []
    h1s = []
    h2s = []
    h3s = []
    press = []
    d = date.today()

    try:
        with open('/home/pi/Sand 3D Printer Monitor System/data logs/data_log'+str(d)+'.csv', 'r', newline = '') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                ts.append(row[1])
                if row[2] == '':
                    if len(t1s)> 2:
                        t1m = statistics.mean(t1s)
                        t1s.append(t1m)
                else:
                    t1s.append(float(row[2]))

                if row[4] == '':
                    if len(t2s)> 2:
                        t2m = statistics.mean(t2s)
                        t2s.append(t2m)
                else:
                    t2s.append(float(row[4]))
                if row[6] == '':
                    if len(t3s)> 2:
                        t3m = statistics.mean(t3s)
                        t3s.append(t3m)
                else:
                    t3s.append(float(row[6]))
                if row[3] == '':
                    if len(h1s)> 2:
                        h1m = statistics.mean(h1s)
                        h1s.append(h1m)
                else:
                    h1s.append(float(row[3]))

                if row[5] == '':
                    if len(h2s)> 2:
                        h2m = statistics.mean(h2s)
                        h2s.append(h2m)
                else:
                    h2s.append(float(row[5]))
                if row[7] == '':
                    if len(h3s)> 2:
                        h3m = statistics.mean(h3s)
                        h3s.append(h3m)
                else:
                    h3s.append(float(row[7]))
                if row[8] == '':
                    if len(press)> 2:
                        pressm = statistics.mean(press)
                        press.append(pressm)
                else:
                    press.append(float(row[8]))

        ax1.clear()
        ax1.plot(ts, t1s, label='Printer Temp: ' + str(round(t1s[-1],2)))
        ax1.plot(ts, t2s, label='Outside Temp: ' + str(round(t2s[-1],2)))
        ax1.plot(ts, t3s, label='Room Temp: ' + str(round(t3s[-1],2)))
        ax1.set_xticks(ts[::60])
        ax1.set_yticks([50,60,70,80,90,100])
        ax1.legend()

        ax2.clear()
        ax2.plot(ts, h1s, label='Printer Humidity: ' + str(round(h1s[-1],2)))
        ax2.plot(ts, h2s, label='Outside Humidity: ' + str(round(h2s[-1],2)))
        ax2.plot(ts, h3s, label='Room Humidity: ' + str(round(h3s[-1],2)))
        ax2.set_xticks(ts[::60])
        ax2.set_yticks([10,20,30,40,50,60,70,80,90,100])
        ax2.legend()

        ax3.clear()
        ax3.plot(ts, press, label='Air Pressure: ' + str(round(press[-1],2)))
        ax3.set_xticks(ts[::60])
        ax3.set_yticks([0,20,40,60,80,100,120])
        ax3.legend()

    except FileNotFoundError:
        print('waiting for file data')


ani = animation.FuncAnimation(fig, animate,interval=5000)
plt.show()