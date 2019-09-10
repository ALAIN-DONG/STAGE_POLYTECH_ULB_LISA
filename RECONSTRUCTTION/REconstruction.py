from typing import List, Any
import pandas as pd
from pyntcloud import PyntCloud
import numpy as np
from filtrage_donnee import filtre_SOR, filtre_ROR

#  global variable
first_value = True
time_last: int = 0
theta_accumu: float = 0
Z_accumu = 0

# global constant
fieldname = ["time", "TOF0", "TOF2"]


def open_csv_file(path_file):
    return pd.read_csv(path_file, sep=',')


def read_csv_ij(data, i, j):
    return data.iloc[i, j]


def get_rows_quantity(data):
    return len(data)


def dispose_data(SW_TOF0 = False, SW_TOF1 = False, SW_TOF2 = False, internal = True, distance = 0, start_circle = 0, stop_circle = None, seuil = 200, speed_sample = 48, path = "None", T=76187.43, ):

    global time_last
    global first_value
    global theta_accumu
    global Z_accumu

    data_location: List[Any] = []

    x: float = 0
    y: float = 0
    z: float = 0

    compensation_for_sensor_0 = -20
    compensation_angular_for_sensor_0 =0.11
    compensation_for_sensor_1 = 12
    compensation_for_sensor_2 = 12
    taux_tof0 = 1.2

    data = open_csv_file(path)
    length = get_rows_quantity(data)

    n_one_circle = int(T/speed_sample)
    begin_num = n_one_circle * start_circle
    fin_num = length

    if begin_num > length:
        print("not enough points for the start line")
        begin_num = 0
        fin_num = length
    else:
        if stop_circle is None:
            fin_num = length
        elif stop_circle <= 0:
            fin_num = length + n_one_circle * stop_circle
            if fin_num < begin_num:
                fin_num = length
                print("length error")
        else:
            fin_num = n_one_circle * stop_circle
            if fin_num > length:
                print("not enough points for the end line")
                fin_num = length

    begin_num = int(begin_num)
    fin_num = int(fin_num)

    time_last = read_csv_ij(data, begin_num-1, 0)
    level = 0
    for k in range(begin_num, fin_num):
        x = 0
        y = 0
        z = 0
        sw_sensor = -1
        value = 0

        if first_value is True:
            if theta_accumu >= (2 * np.pi):
                theta_accumu = theta_accumu - 2 * np.pi
            first_value = False
            level = level + 1

        time_now = read_csv_ij(data, k, 0)

        sensor_tof0 = read_csv_ij(data, k, 1)
        sensor_tof1 = read_csv_ij(data, k, 2)
        sensor_tof2 = read_csv_ij(data, k, 3)

        if pd.isna(sensor_tof1) and pd.isna(sensor_tof2) and not(pd.isna(sensor_tof0)):
            # case tof1
            if SW_TOF0:
                value = sensor_tof0
                sw_sensor = 0

        if pd.isna(sensor_tof2) and pd.isna(sensor_tof0) and not(pd.isna(sensor_tof1)):
            # case tof1
            if SW_TOF1:
                if sensor_tof1 < seuil:
                    if internal is True:
                        value = sensor_tof1 + compensation_for_sensor_1
                    else:
                        value = sensor_tof1
                sw_sensor = 1 # shutdown this sensor

        if pd.isna(sensor_tof0) and pd.isna(sensor_tof1) and not(pd.isna(sensor_tof2)):
            # case tof2
            if SW_TOF2:
                if sensor_tof2 < seuil:
                    if internal is True:
                        value = sensor_tof2 + compensation_for_sensor_2
                    else:
                        value = sensor_tof2
                sw_sensor = 2

        theta_accumu = theta_accumu + 2 * np.pi * (time_now - time_last) / T
        Z_accumu = Z_accumu + 0.05 * (time_now - time_last) * 0.001

        if sw_sensor is 2:
            if internal:
                x = value * np.cos(theta_accumu)
                y = value * np.sin(theta_accumu)
            else:
                x = (distance - value) * np.cos(theta_accumu)
                y = (distance - value) * np.sin(theta_accumu)
            z = Z_accumu

        if sw_sensor is 1:
            x = value * np.cos(theta_accumu + np.pi)
            y = value * np.sin(theta_accumu + np.pi)
            z = Z_accumu

        if sw_sensor is 0:
            value = value * taux_tof0
            theta = theta_accumu + compensation_angular_for_sensor_0
            x = value * np.cos(theta + np.pi * 0.5) * np.sin(np.pi / 6)
            y = value * np.sin(theta + np.pi * 0.5) * np.sin(np.pi / 6)
            z = Z_accumu - value * np.cos(np.pi / 6) + compensation_for_sensor_0

        time_last = time_now

        if theta_accumu >= (2 * np.pi):
            first_value = True
            # point = pd.DataFrame(data_location, columns=['x', 'y', 'z', ])
            # cloud = PyntCloud(point)
            # cloud.plot(return_scene=True)

        if value is not 0:
            result = (x, y, z)
            data_location.append(result)

    print("Total level constructed:", level)
    return data_location





def reconstruction(from_path=None, to_path=None,filtre = None, k = None, z_max = None, r = None, SW_TOF0 = False, SW_TOF1 = False, SW_TOF2 = False, internal = True, distance = 0, start_circle = 0, stop_circle = None, seuil = 200, speed_sample = 48, path = "None", T=76187.43,):
    data_calculated = dispose_data(SW_TOF0=SW_TOF0, SW_TOF1=SW_TOF1, SW_TOF2=SW_TOF2, internal=internal, distance=distance,
                                   start_circle=start_circle, stop_circle=stop_circle,
                                   path=from_path,)
    point = pd.DataFrame(data_calculated, columns=['x', 'y', 'z', ])
    cloud = PyntCloud(point)

    if filtre is None:
        print("Do not use any filter")
        pass
    elif filtre is "SOR":
        cloud.apply_filter(filtre_SOR(point, k=k, z_max=z_max))
        print("Use filter SOR")
    elif filtre is "ROR":
        cloud.apply_filter(filtre_ROR(point, k=k, r=r))
        print("Use filter ROR")

    cloud.to_file(to_path)
    cloud.plot(return_scene=True)
    print("Generated successfully, the PLY file has been stored in: ", to_path)


## optional parameters ##
# from_path : the file CSV's  path (complete path)
# to_path : the 3D image file PLY's path (complete path)
#filtre : the type of the filter, three options to choose from: "SOR", "ROR", None
#k, r, z_max : the parameters for the filters
# Two filters avaliable:

    # filtre_ROR(point, k = int, r = float)
    # Radius Outlier Removal Filter,the filter will look for the required number of neighboors inside that sphere.
    # k is the number of neighbors that will be used to compute the filter
    # r is the radius of the sphere with center on each point.

    # filtre_SOR(point, k = int, z_max = float)
    # Statistical Outlier Removal Filter
    # k is the number of neighbors that will be used to compute the filter.
    # z_max is the maximum Z score which determines if the point is an outlier.
#SW_TOF0/SW_TOF1/SW_TOF2 : the switch for each sensor. True to activate the sensor
#internal : to distinguish the mode of the reconstruction: interior mode or exterior mode. Ture for the interior mode
#distance : the distance between the sensor and the center of the turning table, in millimetre, only usful in the exterior mode.
#start_circle : the number of started circle for the reconstruction
#stop_circle : the number of final circle for the reconstruction
#seuil : the seuil for limite the detected distance
#speed_sample : the speed of the sampling, or the time interval of each sample (in millisecond)
#T : the period of one turn of the turning table (in millisecond)
reconstruction(from_path="/home/alain/Desktop/all code/source_csv/data_for_reconstruction_FINAL.csv", to_path="/home/alain/Desktop/all code/head_with_SOR0.ply", filtre="SOR", k=5, z_max=1, SW_TOF0=True, SW_TOF2=True, SW_TOF1=False, internal=True, distance=200,
                                   start_circle=3, stop_circle=None)

