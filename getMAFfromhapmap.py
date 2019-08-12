#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
File name: getMAFfromhapmap.py
Author: CrazyHsu @ crazyhsu9527@gmail.com 
Created on: 2019-05-05 20:51:59
Last modified: 2019-05-05 20:51:59
'''
import sys
import pandas as pd
from collections import Counter

HETERDICT={"AC": 1, "AG": 1, "AT": 1, "CA": 1, "CG": 1, "CT": 1,
           "TA": 1, "TC": 1, "TG": 1, "GA": 1, "GC": 1, "GT": 1}

def calMajorAndMinorAllele(x):
    name = x.name
    counter = Counter(x).most_common(3)
    majorGeno, minorGeno, majorCount, minorCount = judgeMajorAndMinor(counter, len(counter))
    majorPect = round(majorCount / float(len(x)), 4)
    minorPect = round(minorCount / float(len(x)), 4)
    # heterPect = round(1 - majorPect - minorPect, 4)
    return ",".join([majorGeno, minorGeno, str(majorPect), str(minorPect)])

def judgeMajorAndMinor(counter, counterLen):
    returnList = []
    if counterLen == 3:
        if counter[0][0] in HETERDICT:
            returnList = [counter[1][0], counter[2][0], counter[1][1], counter[2][1]]
        elif counter[1][0] in HETERDICT:
            returnList = [counter[0][0], counter[2][0], counter[0][1], counter[2][1]]
        elif counter[2][0] in HETERDICT:
            returnList = [counter[0][0], counter[1][0], counter[0][1], counter[1][1]]
    elif counterLen == 2:
        if counter[0][0] in HETERDICT:
            minorAllele = ''
            for i in counter[0][0]:
                if i not in counter[1][0]:
                    minorAllele = i
            returnList = [counter[1][0], minorAllele * 2, counter[1][1], 0]
        elif counter[1][0] in HETERDICT:
            minorAllele = ''
            for i in counter[1][0]:
                if i not in counter[0][0]:
                    minorAllele = i
            returnList = [counter[0][0], minorAllele * 2, counter[0][1], 0]
        else:
            returnList = [counter[0][0], counter[1][0], counter[0][1], counter[1][1]]
    elif counterLen == 1:
        returnList = [counter[0][0], "NN", counter[0][1], 0]
    return returnList

def processHapmap(hpFile):
    data = pd.read_table(hpFile, index_col=0)
    chrId = data.iloc[:, 1]
    pos = data.iloc[:, 2]
    # headerdf = data.iloc[:, 0:10]
    genoType = data.iloc[:, 10:]
    # probeId = data.index
    tmp = genoType.apply(lambda x: calMajorAndMinorAllele(x), axis=1)
    tmpdf = tmp.str.split(",", expand=True)
    tmpdf = tmpdf.rename({0: "majorGeno", 1: "minorGeno", 2: "majorPect", 3: "minorPect"},
                         axis="columns")
    tmpdf.insert(loc=0, column="chrId", value=chrId)
    tmpdf.insert(loc=1, column=pos.name, value=pos)
    tmpdf.to_csv("hapmap2maf.txt", index=True, header=False, sep="\t")

def main():
    hpFile = sys.argv[1]
    processHapmap(hpFile)

if __name__ == '__main__':
    main()
