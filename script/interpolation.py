import pandas as pd
import numpy as np
import glob
import os

time_Significant_digits = 3
data_Significant_digits = 4

def FindNAN(datalist):
    """
    Find nan string type in const samplingrate data.
    """
    nan_numbers = []
    count = 0
    for data in datalist:
        data_str = str(data)
        if data_str == 'nan':
            nan_numbers.append(count)
        count += 1
    return nan_numbers


def SegmentNAN_test(nan_numbers):
    """
    Separate continuous number from nan_numbers.
    """
    #init values
    segment_num = {}
    block = []
    key_segment_num = 0
    for nan_number in nan_numbers:
        if len(block) == 0:
            #init
            block.append(nan_number)
        else:
            if block[-1] + 1 != nan_number:
                #forward segment
                segment_num[key_segment_num] = block
                block = []
                key_segment_num += 1
            block.append(nan_number)
    return segment_num

def SegmentNAN(nan_numbers):
    """
    Separate continuous number from nan_numbers.
    """
    #init values
    segment_num = {}
    block = []
    key_segment_num = 0
    count = 0
    nan_numbers_len = len(nan_numbers)
    for nan_number in nan_numbers:
        count += 1
        if len(block) != 0 and block[-1] + 1 != nan_number:
            segment_num[key_segment_num] = block
            block = []
            key_segment_num += 1
        
        block.append(nan_number)

        if count == nan_numbers_len:
            #end array
            segment_num[key_segment_num] = block
    return segment_num


def GetBothEnds(times, data, Segments, start_data_len, end_data_len):
    segments_bothends = {}
    for dic in Segments.items():
        segment = dic[0]
        block = dic[1]
        lower = block[0] - 1
        upper = block[-1] + 1
        #delete both ends. if both ends is nan.
        if lower < start_data_len:
            times.pop(0)
            data.pop(0)
        elif upper > end_data_len:
            times.pop(-1)
            data.pop(-1)
        else:
            values = [lower, upper]
            segments_bothends[segment] = values
    return segments_bothends, times, data


def InterpolationCoordinates(segments_bothends, times, data):
    def Interpolation(x, param):
        """
        Math:calculate interpolation.
        """
        x1, x2, y1, y2 = param[0], param[1], param[2], param[3]
        k = (y2 - y1) / (x2 - x1)
        y = y1 + k * (x - x1)
        return (x, y)

    def ObtainDecimal(x, integer):
        return x - integer


    Interpolation_list = []
    dic_Interpolation_nan = {}
    try:
        time_interval = round((times[-1] - times[0]) / len(times), time_Significant_digits)
        print("time_interval = {}".format(time_interval))

        count_try = 0
        for bothends in segments_bothends.values():
            number_list = np.arange(bothends[0]+1, bothends[-1])
            number_list_len = len(number_list)
            confirm_nan = [data[i] for i in number_list]

            #print("number list = {}".format(number_list))
            y1 = data[bothends[0]]
            y2 = data[bothends[-1]]
            #calculate with decimal
            minx = times[bothends[0]]
            integer = int(minx)
            x1 = round(ObtainDecimal(minx, integer), time_Significant_digits)
            x2 = round(ObtainDecimal(times[bothends[-1]], integer), time_Significant_digits)
            #print("{} , number list = {}, x2 = {}".format(bothends, number_list_len, x2))
            #print("nan list = {}".format(confirm_nan))
            param = [x1, x2, y1, y2]
            x_numbers = np.arange(x1 + time_interval, x2, time_interval)
            if len(x_numbers) > number_list_len:
                x_numbers = list(x_numbers)
                x_numbers.pop(-1)
                x_numbers = np.array(x_numbers)
            #print(x_numbers)
            count = 0
            for x in x_numbers:
                Interpolation_coordinate = Interpolation(x, param)
                Interpolation_coordinate = (round(Interpolation_coordinate[0], time_Significant_digits) + integer, round(Interpolation_coordinate[1], data_Significant_digits))
                Interpolation_list.append(Interpolation_coordinate)
                try:
                    dic_Interpolation_nan[number_list[count]] = Interpolation_coordinate
                except IndexError:
                    print("IndexError, {} data".format(count_try))
                count += 1
            count_try += 1
    except IndexError:
        print("IndexError. Cause investigation now.")
    return Interpolation_list, dic_Interpolation_nan


def Replace_NAN_Number(times, data, nan_num_coordinates):
    """
    Replace nan string to interpolation number.
    """
    for dic in nan_num_coordinates.items():
        replace_number = dic[0]
        coordinate = dic[1]
        times[replace_number] = coordinate[0]
        data[replace_number] = coordinate[1]
    return times, data


def WriteCSV(fname, times, data):
    """
    Write including interpolation data to csv file.
    """
    new_fname = '../interpolation_data/' + fname + '.csv'
    header = ['SensorTimeStamp', 'InfAC']
    in_dataframe = [[times[i], data[i]] for i in range(len(data))]
    write_df = pd.DataFrame(in_dataframe, columns=header)
    write_df.to_csv(new_fname)
    print("Write {}".format(new_fname))
    return 0


def GetCSVfileName(*args):
    """
    folder name format : mount_volcano_obsname_date_time(_volcano scale)
    """
    GetFolderName = os.getcwd().split('/')[-1].split('_')

    folder_name = ""
    length_FolderName = len(GetFolderName)
    count = 0
    for name in GetFolderName:
        count += 1
        if length_FolderName - 1 > count:
            folder_name = folder_name + name + "_"
        elif length_FolderName - 1 >= count:
            folder_name = folder_name + name

    csvfile_name = folder_name
    for fname in args:
        csvfile_name += '_' + fname
    return csvfile_name


def main():
    print("Perform linear interpolation on lack of data from const framerate data")
    #read data
    fpath = '../const_framerate_data/infs_*.csv'
    fpaths = glob.glob(fpath)

    
    for fpath in fpaths:
        df = pd.read_csv(fpath)
        timestamps = df['SensorTimeStamp'].tolist()
        Infs_AC = df['InfAC'].tolist()
        #processing
        nan_numbers = FindNAN(Infs_AC)
        #print("found {} nan".format(len(nan_numbers)))
        Segments = SegmentNAN(nan_numbers)
        start_data_len = 0
        end_data_len = len(Infs_AC) - 1
        segments_bothends, times, data = GetBothEnds(timestamps, Infs_AC, Segments, start_data_len, end_data_len)
        coordinates, nan_num_coordinates = InterpolationCoordinates(segments_bothends, times, data)
        nan_numbers2 = FindNAN(data)
        times, data = Replace_NAN_Number(times, data, nan_num_coordinates)
        
        if len(data) != 0:
            lack_rate = round(len(nan_numbers) / len(data) * 100, 1)
            print("lack rate : {}%".format(lack_rate))
            #write data
            fname_infs = fpath.split('/')[2].split('.')[0]
            fname_csv = GetCSVfileName(fname_infs, str(lack_rate))
            WriteCSV(fname_csv, times, data)
    return 0

if __name__ == '__main__':
    main()