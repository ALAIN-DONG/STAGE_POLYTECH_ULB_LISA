## author:    Lihao DONG
## date:      2019-06-24
## function:  note the input and return them when a 'ENTER' reconized


import pyb

usb1 = pyb.USB_VCP()

data1 = "dfef"
while True:
    data = usb1.recv(1,timeout=10)
    
    data1 = str(data1)
    if data == b'':
        pass
    elif data == b'\r':
        print(data1)
        data1 = ""
    else:
        data1 = data1 + (data.decode('utf-8'))


