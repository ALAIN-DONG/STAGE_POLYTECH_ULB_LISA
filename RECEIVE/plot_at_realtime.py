import serial
import json
import os
import io
import matplotlib
import time
import matplotlib.pyplot as plt
from math import *
import time_translation

from collections import deque


SensorList = ['TOF0', 'TOF1', 'TOF2']


# Step I : open the gate
ser = serial.Serial('/dev/ttyACM0', 19200, timeout=2, parity=serial.PARITY_EVEN, rtscts=1)
print(ser.isOpen())


# Step II : configurate the plot tool

# FIRST METHOD
plt.ion()
plt.figure(1)
t0 = deque([0])
t1 = deque([0])
t2 = deque([0])
data_0 = deque([0])
data_1 = deque([0])
data_2 = deque([0])

for i in range(0, 50):
    t0.append(int(i))
    t1.append(int(i))
    t2.append(int(i))
    data_0.append(int(i))
    data_1.append(int(i))
    data_2.append(int(i))


flag_first_time = True
first_time = 0
while True:
    #print(ser.readline().decode('utf-8'))
    data_recvc = ser.readline() #.decode('utf-8')
    #print(data_recvc)
    if data_recvc is b"":
        pass
    elif data_recvc is not b"":
        data_dict = json.loads(data_recvc)

        if flag_first_time is True:
            first_time = int(data_dict['time'])
            flag_first_time = False


        if data_dict['sensor_name'] == "TOF0":
            #t_now = time_translation.calc_time_pseudo(first_time, data_dict['time'])
            data_now = int(data_dict['value'])
            t_now = data_dict['time']
            if data_now > 1000:
                data_now = 1000
            t0.append(t_now)
            data_0.append(data_now)

        elif data_dict['sensor_name'] == "TOF1":
            #t_now = time_translation.calc_time_pseudo(first_time, data_dict['time'])
            data_now = int(data_dict['value'])
            t_now = data_dict['time']
            if data_now > 1000:
                data_now = 1000
            t1.append(t_now)
            data_1.append(data_now)

        elif data_dict['sensor_name'] == "TOF2":
            #t_now = time_translation.calc_time_pseudo(first_time, data_dict['time'])
            t_now = data_dict['time']
            data_now = int(data_dict['value'])
            if data_now > 1000:
                data_now = 1000
            t2.append(t_now)
            data_2.append(data_now)

        plt.clf()

        plt.plot(t0, data_0, color='green')
        plt.plot(t1, data_1, color="red")
        plt.plot(t2, data_2, color='blue')

        if data_dict['sensor_name'] == "TOF0":
            t0.popleft()
            data_0.popleft()
        if data_dict['sensor_name'] == "TOF1":
            t1.popleft()
            data_1.popleft()
        if data_dict['sensor_name'] == "TOF2":
            t2.popleft()
            data_2.popleft()




        plt.pause(0.0001)




        #print("time :", t_now, "data :", data_now)

# FIN FIRST METHOD

# #
# # SECOND METHOD
# plt.ion()
# plt.figure(1)
#
# flag_first_time = True
# first_time = 0
# while True:
#     #print(ser.readline().decode('utf-8'))
#     data_recvc = ser.readline() #.decode('utf-8')
#     #print(data_recvc)
#     if data_recvc is b"":
#         pass
#     elif data_recvc is not b"":
#         data_dict = json.loads(data_recvc)  # restore the dictionary which contain all information
#
#         # store the start moment
#         if flag_first_time is True:
#             #first_time = int(data_dict['time'])
#             first_time = 0
#             flag_first_time = False
#
#         # just plot TOF0 for test
#         t_now = time_translation.calc_time_pseudo(first_time, data_dict['time'])
#
#         data_now = int(data_dict['value'])
#         if data_now > 1000:
#             data_now = 400
#
#         print(data_dict['sensor_name'])
#
#         if data_dict['sensor_name'] == "TOF0":
#             plt.plot(t_now, data_now, '-o')
#         # elif data_dict['sensor_name'] == "TOF1":
#         #     plt.plot(t_now, data_now, '-*')
#         # elif data_dict['sensor_name'] == "TOF2":
#         #     plt.plot(t_now, data_now, '-x')
#
#         plt.pause(0.1)





        # print('sensor_name : ', data_dict['sensor_name'], end=" ")
        # print('time : ', data_dict['time'], end=" ")
        # print('value : ', data_dict['value'])

        # num_sensor = SensorList.index(data_dict['sensor_name'])
        # content = str(data_dict['time']) + ","
        # for i in range(0, num_sensor):
        #     content = content + ","
        #
        # content = content + str(data_dict['value']) + ","
        #
        # for i in range(0, (len(SensorList) - num_sensor - 1)):
        #     content = content + ","
        #
        # content = content + "\n"
        #
        # with io.open(path_file, 'a') as file_Object:
        #     file_Object.write(content)
        #     print("write_correct : " + content)
