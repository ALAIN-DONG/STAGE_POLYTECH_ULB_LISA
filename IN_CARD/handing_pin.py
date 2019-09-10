import pyb

def InitXshutPin(TabPin):
    for nomPin in TabPin:
        myPin = pyb.Pin(nomPin, pyb.Pin.OUT)
        myPin.value(False)


def Pin_TurnOn(PinName):
    myPin = pyb.Pin(PinName, pyb.Pin.OUT)
    myPin.value(True)


def Pin_TurnOff(PinName):
    myPin = pyb.Pin(PinName, pyb.Pin.OUT)
    myPin.value(False)


def Pin_TurnOn_C(myPin):
    myPin.value(True)


def Pin_TurnOff_C(myPin):
    myPin.value(False)
