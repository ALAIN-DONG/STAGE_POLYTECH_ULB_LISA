import pyb
import os
from time import sleep
import uos
import uio
import machine
from pyboard_vl53l0x import VL53L0X
from filters import median_filter,freq_filter,mean_filter,mean_std_filter
import lighting
import utime
import handing_pin

# ### this script is ready to run ###
# def display(data):
#     print('"s" to toggle, "esc" to stop #### mm=%4d' % data)#, end = '\r')


def Read_Only_One_Sensor(SensorName, XPinName, Active, path):
    # # preparatory work

    # 0.configurate the pin 'XSHUT'
    handing_pin.Pin_TurnOn(XPinName)

    # 1.Initialize I2C bus and sensor.
    i2c = machine.I2C(sda='X10', scl='X9', freq=400000)  # sampling rate: 400 KHz => 2.5 us/time
    i2c.scan() # very important to add this sentence
    #print('All i2c device connected :', i2c.scan())  # show all i2c device

    # 2.link the I2C bus with the TOF sensor
    vl53 = VL53L0X(i2c, io_timeout_s=50) # origine = 2000f
    #print('VL53 sensor :', vl53)

    # 3.configurate the port USB so that we can control it via terminal
    # usb = pyb.USB_VCP()
    # data = usb.recv(10, timeout=500)  # we can import 's' or 'esc' ## recv(amount_of_the_bits, timeout_for_received_data)
    # # fin preparation work


    # # begin of the capture and the write into the file CSV

    for sample, new_val, hist in vl53.generator(None):
        # ## CORE CODE
        #print(myPin.value(), hist)  # display all the data in the terminal

        # ###part of the write into the file CSV
        content = ""
        if SensorName is "TOF2":
            content = str(hist['time']) + ',' + str(hist['#']) + ',' + str(hist['mm']) + ',' + ',' + ',' + '\n'
        elif SensorName is "TOF3":
            content = str(hist['time']) + ',' + ',' + ',' + str(hist['#']) + ',' + str(hist['mm']) + ',' + '\n'
        lighting.Light_EnTrainDeEcrire()  # indecate that it's in process of writing
        with uio.open(path, 'a') as file_Object:
            file_Object.write(content)
            print("write ok: ", content)
        # ### fin write
        break

    # for s, v, h in freq_filter(mean_std_filter(vl53.generator(1), 10)):
    #     # control the circulation via keyboard in terminal
    #     data = usb.recv(1, timeout=0)
    #     if data != b'':
    #         if data == b's':
    #             running = not running
    #         if data == b'\x1b':
    #             break
    #     # Or control the circulation via the button 'USR'
    #     if sw.value():
    #         running = not running
    #         lighting.Light_Feedback_Button()
    #     # fin control
    #     # # CORE CODE
    #     if running:
    #         # i += 1
    #         # display(h['mm'])
    #         print(h)  # display all the data in the terminal
    #         # part of the write into the file CSV
    #         content = str(h['mm']) + ',' + str(h['mean']) + ',' + str(h['std']) + ',' + str(h['us']) + '\n'
    #         with uio.open('data_csv/test.csv', 'a') as file_Object:
    #             file_Object.write(content)
    #             lighting.Light_EnTrainDeEcrire()  #indecate that it's in process of write
    #         # fin write
    #
    #     if running is not True:
    #         lighting.Light_Pause()

