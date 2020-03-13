import glob
import pandas as pd
import shutil

def MoveNoData(fname):
    """
    Move no raw data to ../rawdata_unabledata folder.
    """
    df = pd.read_csv(fname, header=None)
    df_len = len(df.values.tolist())
    if df_len == 1:
        print("No data. Mo unable usedata folder")
        shutil.move(fname, './raw_data/unable_usedata')
        return 1
    else:
        return 0


def main():
    fpath = "../raw_data/infs*.csv"
    fpaths = glob.glob(fpath)

    count = 0
    for fname in fpaths:
        count = MoveNoData(fname) + count
    print("number of {} was moved ../raw_data/unable_usedata.".format(count))

    return 0

if __name__=="__main__":
    main()