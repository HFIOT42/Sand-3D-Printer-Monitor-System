import RPi.GPIO as GPIO
import time,statistics
from message import *
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#define the pin that goes to the circuit
ERROR_PIN = 11
TIME_THRESH = 1100
MESS_TIMEOUT = 18000
LIGHT_DELAY = 120

global temp_tic
temp_tic = time.perf_counter()-MESS_TIMEOUT


def rc_time (ERROR_PIN):
    count = 0

    #Output on the pin for
    GPIO.setup(ERROR_PIN, GPIO.OUT)
    GPIO.output(ERROR_PIN, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(ERROR_PIN, GPIO.IN)

    #Count until the pin goes high
    while (GPIO.input(ERROR_PIN) == GPIO.LOW):
        count += 1
    #print(count)
    return count
def isLightOn(ERROR_PIN):
    t = []
    for i in range(0,10):
        t.append(rc_time(ERROR_PIN))
    if statistics.mean(t) < TIME_THRESH:
        return True
    else:
        return False

#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    start_time = 0
    while True:
        if isLightOn(ERROR_PIN):
            start_time = time.perf_counter()
            while isLightOn(ERROR_PIN):
                print('Light on')

                if (time.perf_counter() > temp_tic) and ((time.perf_counter()-start_time) > LIGHT_DELAY) :
                    print('no TIMEOUT')
                    temp_tic = time.perf_counter()+MESS_TIMEOUT
                    start_time = 0
                    sendMessage('There is an error with the 3d printer.')
            start_time = 0

except KeyboardInterrupt:
    GPIO.cleanup()
    pass
finally:
    GPIO.cleanup()