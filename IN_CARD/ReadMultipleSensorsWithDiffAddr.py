import pyb
import os
from time import sleep
import uos
import uio
import machine

from filters import median_filter,freq_filter,mean_filter,mean_std_filter
import lighting
import utime
from pyb import Pin
import handing_pin
import handing_file

from pyboard_vl53l0x import VL53L0X
#from new_vl53lox import VL53L0X
import handing_button
import handing_time_transition




def capture(SC_TOF0 = False, SC_TOF1 = False, SC_TOF2 = False, DELAY = 48, TIMEOUT_CAPTURE = 50, TIMEOUT_BUTTON = 500):
    # SC_TOF0 = False
    # SC_TOF1 = True
    # SC_TOF2 = False

    # write_while_capturing = False


    # FILL_NAME = "DATA_CUPTURED"  # the csv file name. Acquiescently, the file csv will save in the folder /data_csv

    # TIMEOUT_CAPTURE = 50  
    # TIMEOUT_BUTTON = 500  # constant for distinguish the long press and short press
    # DELAY = 48


    XSHUT_PIN_TOF_0 = "X6"
    XSHUT_PIN_TOF_1 = "X7"
    XSHUT_PIN_TOF_2 = "X8"

    ADDR_TOF_0 = 0x3C
    ADDR_TOF_1 = 0x3A
    ADDR_TOF_2 = 0x30





    # Step I : configure the different sensors so that they will have different address
    # 1, configure the Xshut pins for sensors
    pin_for_TOF_0 = pyb.Pin(XSHUT_PIN_TOF_0, pyb.Pin.OUT)
    pin_for_TOF_1 = pyb.Pin(XSHUT_PIN_TOF_1, pyb.Pin.OUT)
    pin_for_TOF_2 = pyb.Pin(XSHUT_PIN_TOF_2, pyb.Pin.OUT)

    # 2, shutdown all pins
    handing_pin.Pin_TurnOff_C(pin_for_TOF_0)
    handing_pin.Pin_TurnOff_C(pin_for_TOF_1)
    handing_pin.Pin_TurnOff_C(pin_for_TOF_2)

    # 3, create a new i2c object
    i2c = machine.I2C(sda='X10', scl='X9', freq=400000)


    # 4, configure TOF1's address
    if SC_TOF0:
        handing_pin.Pin_TurnOn_C(pin_for_TOF_0)
        pyb.delay(10)
        Tof0 = VL53L0X(i2c)
        Tof0.set_timeout(TIMEOUT_CAPTURE)
        Tof0.set_address(ADDR_TOF_0)
        Tof0.init()


    # 5, configure TOF1's address
    if SC_TOF1:
        handing_pin.Pin_TurnOn_C(pin_for_TOF_1)  # turn on the pin of Xshut for the sensor TOF1
        pyb.delay(10)  # necessary delay for the response of the change of pin's level
        Tof1 = VL53L0X(i2c)  # connect the i2c bus with the sensor and initialize
        Tof1.set_timeout(TIMEOUT_CAPTURE)  # configure the interval of the sampling
        Tof1.set_address(ADDR_TOF_1)  # configure the address of the sensor TOF1
        Tof1.init()  # redo the initialization of the sensor after change its address and timeout


    # 6, configure TOF2's address
    if SC_TOF2:
        handing_pin.Pin_TurnOn_C(pin_for_TOF_2)
        pyb.delay(10)
        Tof2 = VL53L0X(i2c)
        Tof2.set_timeout(TIMEOUT_CAPTURE)
        Tof2.set_address(ADDR_TOF_2)
        Tof2.init()

    # fin configuration of the address of the sensors




    # Step II : range the captured datas and send them to PC via USB

    while True:


        lighting.Light_Script_Ready()
        # ##*********** The script is ready now, start your show *************##

        # prepairing for initial information
        running = True
        start_time = utime.ticks_ms()
        ms_time = utime.ticks_ms()
        time_now = ms_time

        while True:

            sw = pyb.Switch()
            if sw.value():
                if handing_button.button_control(TIMEOUT_BUTTON) == "L":
                    running = False
                    lighting.Light_FinDeEcrire()
                    break
                elif handing_button.button_control(TIMEOUT_BUTTON) == "S":
                    running = not running
            if running:
                if SC_TOF0:
                    while (utime.ticks_diff(time_now, ms_time) < DELAY):
                        time_now = utime.ticks_ms()
                        pass
                    ms_time = utime.ticks_ms()
                    handing_file.organiser_content("TOF0", time_now, Tof0.range)
                if SC_TOF1:
                    while (utime.ticks_diff(time_now, ms_time) < DELAY):
                        time_now = utime.ticks_ms()
                        pass
                    ms_time = utime.ticks_ms()
                    handing_file.organiser_content("TOF1", time_now, Tof1.range)
                if SC_TOF2:
                    while (utime.ticks_diff(time_now, ms_time) < DELAY):
                        time_now = utime.ticks_ms()
                        pass
                    ms_time = utime.ticks_ms()
                    handing_file.organiser_content("TOF2", time_now, Tof2.range)

                lighting.Light_EnTrainDeEcrire()
            if running is not True:
                lighting.Light_Pause()

        lighting.Light_EnRepos()


