import uos
import uio
import ujson
import pyb
import lighting


usb_pyboard = pyb.USB_VCP()

SensorList = ['TOF0', 'TOF1', 'TOF2']
sw_send_to_terminal = True


def YoN_in_list(senser_name):
    return senser_name in SensorList


def send_to_terminal(sensor_name, time, value):
    # the form of the data sent to terminal is the 'directory'
    dict_data = {"sensor_name": sensor_name, "time": time, "value": value}
    usb_pyboard.send(ujson.dumps(dict_data))
    usb_pyboard.send("\n")


def organiser_content(sensor_name, time, value):
    num_sensor = SensorList.index(sensor_name)
    #content = str(time) + ","
    #for i in range(0, num_sensor):
    #    content = content + ","

    #content = content + str(value) + ","

    #for i in range(0, (len(SensorList)-num_sensor-1)):
    #    content = content + ","

    #content = content + "\n"

    # ##send to terminal
    if sw_send_to_terminal:
        if usb_pyboard.isconnected():
            send_to_terminal(sensor_name, time, value)

    #return content

#
# def rewrite_title(path):
#     content = "time" + ","
#     if len(SensorList) is not 0:
#         for sensorName in SensorList:
#             content = content + sensorName + ","
#     lighting.Light_Test_Ok(10)
#     with uio.open(path, 'r+') as file_Object:
#         cont = file_Object.read()
#         file_Object.seed(0, 0)
#         lighting.Light_Test_Ok(2)
#         file_Object.write(content + cont)
#         print("write ok: ", content)


def write_into_follow(path, content):
    with uio.open(path, 'a') as file_Object:
        file_Object.write(content)
        #print("write ok: ", content)


def create_new_document(path):
    content = "time,"
    for sesname in SensorList:
        content = content + "mm." + sesname + ","
    content = content + "\n"
    with uio.open(path, 'w') as file_Object:
        file_Object.write(content)


def new_folder(dir_name):
    if dir_name not in uos.listdir():
        uos.mkdir(dir_name)

