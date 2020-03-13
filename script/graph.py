import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os
import glob

def GetGraphPNG(fname, times, inf_AC):
    #元データのグラフ化
    plt.plot(times, inf_AC)
    plt.xlabel('Timestamp')
    plt.ylabel('pressure[mPa]')
    plt.savefig(fname + '.png')
    print("saving {}.png".format(fname))
    plt.clf()
    return 0

def main():
    fpath = '../interpolation_data/*.csv'
    fpaths = glob.glob(fpath)
    #fnames_noextension = [os.path.basename(fname).split('.')[0] for fname in fnames]
    print(fpaths)

    count = 0
    for fpath in fpaths:
        df = pd.read_csv(fpath)
        times = df['SensorTimeStamp'].tolist()
        inf_AC = df['InfAC'].tolist()
        if len(inf_AC) != len(times):
            print("error:diffent number of list length.")
            sys.exit()
        fname = "../graph/" + fpath.split('/')[2].split('.')[0]
        GetGraphPNG(fname, times, inf_AC)
        count += 1
    return 0

if __name__ == '__main__':
    main()