import lighting
from ReadMultipleSensorsWithDiffAddr import capture

lighting.Light_Main_Start()

# Optional parameter:
#   # SC_TOF0           : Turn on(True) or off(False) the sensor TOF0, defaut: False
    # SC_TOF1           : Turn on(True) or off(False) the sensor TOF1, defaut: False
    # SC_TOF2           : Turn on(True) or off(False) the sensor TOF2, defaut: False
    # TIMEOUT_CAPTURE   : constant for configure the timeout for whit the response of the sensor, defaut: (50)
    # TIMEOUT_BUTTON    : constant for distinguish the long press and short press, defaut: 500(ms)
    # DELAY             : constant for configure the interval of sampling, defaut: 48(ms)
capture(SC_TOF0 = True, SC_TOF1 = True, SC_TOF2 = True)


lighting.Light_EnRepos()

