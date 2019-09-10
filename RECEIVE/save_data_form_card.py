import serial
import json
import os
import io

SensorList = ['TOF0', 'TOF1', 'TOF2']
path_root = "/media/alain/DOCUMENT/stage"  ## top file name
dir_name = "data_csv"  ## folder for storing the data files



def check_json_format(raw_msg):

    if isinstance(raw_msg, str):
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False


def receive_data_from_pyboard(fill_name=None):
    
    
    # Step I : open the gate
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=10, parity=serial.PARITY_EVEN, rtscts=1)
    print(ser.isOpen())
    
    
    # Step II : write the datas into the file CSV while capturing
    
    # 1, create a folder
    path_dir = path_root + "/" + dir_name
    if dir_name not in os.listdir(path_root):
        os.mkdir(path_dir)
    
    # 2, create the file CSV
    # content = "time,NB.TOF2,mmTOF2,NB.TOF3,mmTOF3\n"  # the columns head of the file csv
    path_file = path_dir + '/' + fill_name + '.csv'
    
    content_title = "time,TOF0,TOF1,TOF2," + "\n"  # the title of the table
    if os.path.exists(path_file) is not True:
        os.mknod(path_file)
    with io.open(path_file, 'w') as file_Object:
        file_Object.write(content_title)
    
    
    time_mem = 0
    while True:
        data_recvc = ser.readline().decode('utf-8')
    
        if check_json_format(data_recvc):
            if data_recvc is b"":
                pass
            if data_recvc is b"AT":
                pass
            elif data_recvc is not b"":
                data_dict = json.loads(data_recvc, strict=False)
                # print('sensor_name : ', data_dict['sensor_name'], end=" ")
                # print('time : ', data_dict['time'], end=" ")
                # print('value : ', data_dict['value'])
    
                num_sensor = SensorList.index(data_dict['sensor_name'])
    
                if num_sensor is 0:
                    content = str(data_dict['time']) + "," + str(data_dict['value']) + "," + "," + "," + "\n"
    
                if num_sensor is 1:
                    content = str(data_dict['time']) + "," + "," + str(data_dict['value']) + "," + "," + "\n"
    
                if num_sensor is 2:
                    content = str(data_dict['time']) + "," + "," + "," + str(data_dict['value']) + "," + "\n"
    
                content = str(content)
                with io.open(path_file, 'a') as file_Object:
                    file_Object.write(content)
                    print("write_correct into file " + fill_name + " : " + content)


receive_data_from_pyboard(fill_name="data_for_reconstruction_FINAL")

