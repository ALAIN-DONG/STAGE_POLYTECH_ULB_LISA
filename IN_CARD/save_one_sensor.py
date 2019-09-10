import serial
import json
import os
import io
import xlrd
import xlwt
from xlutils.copy import copy


def write_excel_xls(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    #print("xls格式表格写入数据成功！")


def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    #print("xls格式表格【追加】写入数据成功！")


def read_excel_xls(path):
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    for i in range(0, worksheet.nrows):
        for j in range(0, worksheet.ncols):
            print(worksheet.cell_value(i, j), "\t", end="")  # 逐行逐列读取数据
        print()


SensorList = ['TOF0', 'TOF1', 'TOF2']


# Step I : open the gate
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1, parity=serial.PARITY_EVEN, rtscts=1)
print(ser.isOpen())


# Step II : write the datas into the file CSV while capturing
# 1, create a folder
dir_name = "data_csv"
path_dir = "/home/alain/stage" + "/" + dir_name
if dir_name not in os.listdir("/home/alain/stage"):
    os.mkdir(path_dir)

# 2, create the file CSV
# content = "time,NB.TOF2,mmTOF2,NB.TOF3,mmTOF3\n"  # the columns head of the file csv
FILL_NAME = "test1"
path_file = '/home/alain/stage/data_csv/' + FILL_NAME + '.csv'
content_title = "time,mm.TOF0,mm.TOF1,mm.TOF2," + "\n"
if os.path.exists(path_file) is not True:
    os.mknod(path_file)
with io.open(path_file, 'w') as file_Object:
    file_Object.write(content_title)


file_name = 'data_obtient.xls'
sheet_name = 'test2'
file_path = '/home/alain/stage/' + file_name
title_xls = [["time", "value"], ]
write_excel_xls(file_path, sheet_name, title_xls)


while True:
    #print(ser.readline().decode('utf-8'))
    data_recvc = ser.readline().decode('utf-8')
    #print(data_recvc)
    if data_recvc is b"":
        pass
    elif data_recvc is not b"":
        data_dict = json.loads(data_recvc)
        # print('sensor_name : ', data_dict['sensor_name'], end=" ")
        # print('time : ', data_dict['time'], end=" ")
        # print('value : ', data_dict['value'])

        num_sensor = SensorList.index(data_dict['sensor_name'])
        if num_sensor is 0:
            content = [data_dict['time'], data_dict['value']]
            data_write = [content, ]
            print(data_write)
            write_excel_xls_append(file_path, data_write)



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

