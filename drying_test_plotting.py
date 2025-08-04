import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import numpy as np
from datetime import datetime, time
from scipy.signal import find_peaks
import matplotlib.patheffects as path_effects

def find_next_ambient(ambient_temp, value_dataset,time_dataset, index, next_index):
    following_time_data=time_dataset[index:next_index]
    following_value_data=value_dataset[index:next_index]
    start_time=time_dataset[index]
    #track if the threshold is hit
    no_end=False
    end_time=0
    for i,value in enumerate(following_value_data):
        if value>ambient_temp:
            end_time=following_time_data[i]
            end_val=following_value_data[i]
            break
    if end_time==0:
        no_end=True
    #dealing with type and plot incompatibility
    if not no_end:
        original_start_time=start_time
        original_end_time=end_time
        print(start_time)
        if isinstance(start_time, str):
            #lots of pain converting, different for different files for some reason
            try:
                start_time= pd.to_datetime(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
            except:
                start_time = pd.to_datetime(datetime.strptime(start_time, '%m/%d/%Y %H:%M'))
        if isinstance(end_time, str):
            try:
                end_time= pd.to_datetime(datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
            except:
                end_time = pd.to_datetime(datetime.strptime(end_time, "%m/%d/%Y %H:%M"))

        time_diff_hours=((end_time-start_time)/ np.timedelta64(1, 's'))/(3600)
        print(start_time)
        print(time_diff_hours)
        return time_diff_hours, original_start_time, original_end_time, end_val
    else:
        return None, None, None, None

def drying(path, threshold, title, start_index=0, end_offset=0, minima_maximum=65):
    #takes a csv
    df = pd.read_csv(path)
    end_index=len(df)-end_offset
    time_stamps=df['Time'][start_index:end_index][::10]
    l_array=np.array(df['Fahrenheit'][start_index:end_index])[::10]
    time_stamps_array=np.array(time_stamps)
    local_minima=argrelextrema(l_array, np.less)
    local_minima, _ = find_peaks(-l_array, distance=30)
    trimmed_local_minima_indexs=[]
    for value in local_minima:
        if l_array[value]<minima_maximum:
            trimmed_local_minima_indexs.append(value)
    #trimming first two (don't want)
    #trimmed_local_minima_indexs=trimmed_local_minima_indexs[2:]
    print('num peaks: ',len(trimmed_local_minima_indexs))
    local_minima=l_array[trimmed_local_minima_indexs]
    minima_time_stamps=time_stamps_array[trimmed_local_minima_indexs]
    next_ambient_times=[]
    next_ambient_values=[]
    time_differences=[]
    for i,index in enumerate(trimmed_local_minima_indexs):
        if i<len(trimmed_local_minima_indexs)-1:
            next_ambient=find_next_ambient(threshold-0.1, l_array,time_stamps_array, index, trimmed_local_minima_indexs[i+1])
        else:
            next_ambient = find_next_ambient(threshold - 0.1, l_array, time_stamps_array, index,
                                             len(time_stamps))
        if next_ambient[0] is not None:
            next_ambient_times.append(next_ambient[2])
            next_ambient_values.append(next_ambient[3])
            time_differences.append(round(next_ambient[0],1))
    # df = pd.DataFrame({"time": next_ambient_times, "value": next_ambient_values})
    # ax =df.plot(x="time", y="value", marker='o')
    plt.plot(time_stamps_array,l_array, label=title+ ' '+str(threshold)+' Threshold')
    plt.plot(minima_time_stamps, local_minima, '*')

    plt.plot(next_ambient_times, next_ambient_values, 'o')
    for i in range(len(next_ambient_times)):
        if i % 2 == 0:  # For even indices, offset labels above the point
            y_offset = 0.3  # Offset above
        else:  # For odd indices, offset labels below the point
            y_offset = -0.8  # Offset below
        #get rid of valley that failed to come back up (skips 4th valley)
        #if i!=3:
        text=plt.text(next_ambient_times[i], next_ambient_values[i]+y_offset, f'{time_differences[i]}')
        text.set_path_effects([path_effects.withStroke(linewidth=3, foreground="white")])  # Add white outline
    plt.legend()
    plt.show()

path=r"C:\Users\PSankari\PycharmProjects\pythonProject1\General\Datalog17.txt"
drying(path, 67, '2680 Lip', 0, 0)