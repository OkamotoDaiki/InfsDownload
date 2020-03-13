import pandas as pd
import pandas.tseries.offsets as offsets
import math
import numpy as np
import glob
import sys
#import matplotlib.pyplot as plt

class ConstFramerate():
    def __init__(self, timestamps, data):
        self.timestamps = timestamps
        self.data = data


    def basic_stat(self, array):
        """
        Use basic statistics for data distribusion in block.
        """
        try:
            return np.median(array)
        except TypeError:
            print("I have not investigated the cause.")
            return 0

    def TimeIntervalBlocks(self, samplingrate=2):
        """
        separate with time interval for ignoring outlier value.
        """
        time_interval = 1 / samplingrate
        #initial objects
        raw_data_count = 0
        block = []
        blocks = []
        block_time = []
        blocks_time = []
        try:
            first_timestamp = self.timestamps[0]
            end_timestamp = self.timestamps[-1]
        except IndexError:
            print("Error! including no data csvfile.")
            return blocks, blocks_time
        time_sep = first_timestamp

        while time_sep < end_timestamp:
            #make block
            time_sep += time_interval
            try:
                while self.timestamps[raw_data_count] <= time_sep:
                    #block content
                    block.append(self.data[raw_data_count])
                    block_time.append(self.timestamps[raw_data_count])
                    raw_data_count += 1
            except IndexError:
                print("through end data")

            if len(block) == 0:
                blocks.append('nan')
                blocks_time.append('nan')
            else:
                one_data = round(self.basic_stat(block),4)
                one_data_time = round(self.basic_stat(block_time),3)
                blocks.append(one_data)
                blocks_time.append(one_data_time)
            block = []
            block_time = []
        return blocks, blocks_time

    def ConstFramerate(self):
        blocks, blocks_time = self.TimeIntervalBlocks()
        return blocks, blocks_time


def graph(data):
    fname = "test_constfname.png"
    time_data = range(len(data))
    plt.plot(time_data, data)
    plt.savefig(fname)
    return 0

def main():
    raw_data_fpath = "../raw_data/infs*.csv"
    fpaths = glob.glob(raw_data_fpath)
    for fpath in fpaths:
        
        df = pd.read_csv(fpath)
        timestamps = df['SensorTimeStamp'].tolist()
        Infs_AC = df['InfAC'].tolist()

        ConstFramerate_obj = ConstFramerate(timestamps, Infs_AC)
        new_data, new_data_time = ConstFramerate_obj.ConstFramerate()
        if len(new_data) != len(new_data_time):
            print("error: differet array length.")
            print(len(new_data))
            print(len(new_data_time))
        else:
            in_dataframe = [[new_data_time[number], new_data[number]] for number in range(len(new_data))]
            header = ['SensorTimeStamp', 'InfAC']
            fname = fpath.split("/")[2]
            fname_write = "../const_framerate_data/" + fname
            df_write = pd.DataFrame(in_dataframe, columns=header)
            df_write.to_csv(fname_write)
            print("data length = {}".format(len(new_data)))
            print("raw data length = {}".format(len(Infs_AC)))
            print("Write {}".format(fname_write))
            #graph(new_data)
    return 0

if __name__=="__main__":
    main()
