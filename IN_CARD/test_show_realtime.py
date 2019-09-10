import serial
import json

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=10, parity=serial.PARITY_EVEN, rtscts=1)
print(ser.isOpen())

while True:
    data_recvc = ser.readline().decode('utf-8')
    #print(data_recvc)
    data_dict = json.load(data_recvc)
    print('sensor_name : ', data_dict['sensor_name'], end=" ")
    print('time : ', data_dict['time'], end=" ")
    print('value : ', data_dict['value'])

