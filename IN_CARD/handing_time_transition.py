def formal_number(num):
    num_str = str(num)
    if len(num_str) == 1:
        return '0' + num_str
    return num_str


def calc_time(start_time, current_time):
    if current_time < start_time:
        raise RuntimeError("time not good!")

    delta = str(current_time - start_time)
    length = len(delta)

    calc_ms = 0
    calc_s = 0
    calc_min = 0
    calc_hour = 0

    if 0 < length <= 3:
        calc_ms = delta[0:length-1]
    elif length > 3:
        calc_ms = delta[length-3:length]
        calc_s = delta[0:length-3]

    calc_s = int(calc_s)
    if calc_s >= 60:
        calc_min = calc_s // 60
        calc_s = calc_s % 60
        if calc_min >= 60:
            calc_hour = calc_min // 60
            calc_min = calc_min % 60

    time_str = formal_number(calc_hour) + "-" + formal_number(calc_min) + "-" + formal_number(calc_s) + "-" + calc_ms
    return time_str
