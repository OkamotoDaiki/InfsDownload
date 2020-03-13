# coding: utf-8

import urllib.request
import csv
import pandas

#find a character string in header
def my_index(l, x, default=-1):
    if x in l:
        headernumber = l.index(x) #Index number of header 
        print("can find " + x)
        return headernumber
    
    #cannot find character string 
    else:
        print("cannot find " + x)
        return default

#read csv
def readcsv(filename):
    #want to read a character from header
    readheader = "URL"

    with open(filename, 'r') as f:
        reader = csv.reader(f) #read csv
        
        #read header in .csv
        header = next(reader)

        print(header)
        csvlist = []
        Indexnumber = my_index(header, readheader)

        if Indexnumber != False :
            for row in reader:
                csvlist.append(row[Indexnumber]) #append all cells of 1 row
        else:
            print("cannot find URL")

    return csvlist #

#data from header Info
def headerdata(filename, name):
    with open(filename, 'r') as f:
        reader = csv.reader(f) #read csv
        
        #read header in .csv
        header = next(reader)
        Indexnumber = my_index(header, name) #インデックス番号
        csvlist = []

        if Indexnumber != -1 :
            for row in reader:
                csvlist.append(row[Indexnumber]) #append all cells of 1 row
            return csvlist
        else:
            print("cannot find")  
            return -1


def FindLocationName(row_num):
    return 0


def download(URLlist, Locationlist):
    """
    Download infrasound csv data from KUT Infrasound Observation Network page.
    """
    #init
    count = 0
    download_count = 0

    #Location to decide filenames
    for url in URLlist:
        print("Location: {}".format(Locationlist[count]))
        print("downloading {}".format(count+1))

        #download csvfile from the Infrasound Institute
        try:
            urllib.request.urlretrieve(url, './raw_data/infs_{}.csv'.format(Locationlist[count]))
            download_count += 1
        except ValueError:
            print("This is unable to download URL.")
        count += 1
    
    print("Finish {} download.".format(download_count))
    return 0

if __name__ == "__main__":
    filename = "sample.csv" #読み込みたいcsvファイルを入力
    
    Locationlist = headerdata(filename, "Location")
    print(Locationlist)
    URLlist = headerdata(filename, "URL")

    print("downloading now...")
    download(URLlist, Locationlist)
    print("finish downloading")


    #urlと保存パスを指定
#    url = "http://infrasound.mydns.jp/infrasound/lib/getAllData.php?fn=15&sy=2018&sm=10&sd=19&sh=9&sn=39&ss=0&ey=2018&em=10&ed=19&eh=10&en=39&es=0&mt=1&gc=2"

#    urllib.request.urlretrieve(url, 'infrasound.csv')
#    print("finish downloading")
