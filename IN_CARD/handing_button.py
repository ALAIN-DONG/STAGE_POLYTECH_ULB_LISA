import pyb
import utime
import lighting


def button_control(press_delay):
    # commonly, the delay is in millisecond
    ms_time_before = 0
    ms_time_after = 0
    sw_button = pyb.Switch()
    if sw_button.value():
        ms_time_before = utime.ticks_ms()
        while True:
            if (utime.ticks_ms() - ms_time_before) > press_delay:
                lighting.turnon_light(2)
            if sw_button.value() is False:
                ms_time_after = utime.ticks_ms()
                break
    if (ms_time_after - ms_time_before) > press_delay:
        lighting.Light_Feedback_Button_Long()
        return "L"
    else:
        lighting.Light_Feedback_Button_Short()
        return "S"
