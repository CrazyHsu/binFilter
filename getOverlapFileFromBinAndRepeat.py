#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
File name: getOverlapFileFromBinAndRepeat.py
Author: CrazyHsu @ crazyhsu9527@gmail.com 
Created on: 2019-04-24 19:42:44
Last modified: 2019-04-24 19:42:45
'''

import re, sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

def getAttribute(key, default, **args):
    return default if key not in args else args[key]

class Bed4(object):
    def __init__(self, record):
        (self.chrId, self.start, self.end, self.name) = record[0], float(record[1]), float(record[2]), record[3]

class Bed4Line(Bed4):
    def __init__(self, line):
        self.record = re.split("\t", line.strip())
        if len(self.record) == 4:
            Bed4.__init__(self, self.record)

class Bed4Ext(Bed4):
    def __init__(self, record):
        Bed4.__init__(self, record)
        self.len = abs(self.end - self.start)

class BedFile(object):
    def __init__(self, fileName):
        self.fileName = fileName
        self.allChr = {}
        self.names = {}
        self.loadBedFile(self.fileName)
        self.sortByPos()

    def loadBedFile(self, fileName):
        with open(fileName) as f:
            for line in f:
                infoList = re.split("\t", line.strip())
                if len(infoList) == 4:
                    BedObj = Bed4Line(line)
                    if BedObj.chrId not in self.allChr:
                        self.allChr[BedObj.chrId] = [BedObj]
                    else:
                        self.allChr[BedObj.chrId].append(BedObj)
                    if BedObj.name not in self.names:
                        self.names[BedObj.name] = [BedObj]
                    else:
                        self.names[BedObj.name].append(BedObj)

    def sortByPos(self):
        for chrId in self.allChr:
            self.allChr[chrId] = sorted(self.allChr[chrId], key=lambda x: x.start)

def dict2bed(binDict, fileOut, binLenDict):
    for chrId in binDict:
        sortedKeys = sorted(binDict[chrId].keys())
        for binId in sortedKeys:
            myL = binDict[chrId][binId]
            print >>fileOut, "\t".join([str(i) for i in [chrId, myL[0], myL[1], binId, binLenDict[chrId][binId]]])

def getOverlap(binBed, repeatBed):
    newBinDict = {}
    for chrId in binBed.allChr:
        binObjs = binBed.allChr[chrId]
        repeatObjs = repeatBed.allChr[chrId]
        repeatIndex = 0
        newDict = {}
        newCount = 0
        for bin in binObjs:

            # if repeatIndex == len(repeatObjs) - 1:
            if repeatIndex == len(repeatObjs):
                break
            while repeatIndex <= len(repeatObjs) - 1:
            # while repeatIndex < len(repeatObjs) - 1:
                repeat = repeatObjs[repeatIndex]
                if bin.start >= repeat.start and bin.end <= repeat.end:
                    break
                elif bin.start <= repeat.end and bin.end >= repeat.end and bin.start >= repeat.start:
                    newDict[newCount] = [repeat.end, bin.end]
                    repeatIndex += 1
                elif bin.start >= repeat.end:
                    repeatIndex += 1
                elif bin.end >= repeat.start and bin.start <= repeat.start and bin.end <= repeat.end:
                    if newCount not in newDict:
                        newDict[newCount] = [bin.start, repeat.start]
                    else:
                        newDict[newCount][1] = repeat.start
                    newCount += 1
                    break
                elif bin.start <= repeat.start and bin.end >= repeat.end:
                    if newCount not in newDict:
                        newDict[newCount] = [bin.start, repeat.start]
                    else:
                        newDict[newCount][1] = repeat.start
                    newCount += 1
                    newDict[newCount] = [repeat.end, bin.end]
                    repeatIndex += 1
                elif bin.end <= repeat.start:
                    newCount += 1
                    break

        # for x in newDict:
        #     print x, newDict[x]
        newBinDict[chrId] = newDict
    return newBinDict

def filterBin(binDict):
    newDict = {}
    binLenDict = {}
    for chrId in binDict:
        for l in binDict[chrId]:
            start = binDict[chrId][l][0]
            end = binDict[chrId][l][1]
            length = end - start
            if length >= 200:
                if chrId not in newDict:
                    newDict[chrId] = {l: [start, end]}
                    binLenDict[chrId] = {l: length}
                else:
                    newDict[chrId].update({l: [start, end]})
                    binLenDict[chrId].update({l: length})
    return newDict, binLenDict

def plotBinLenDist(binLenDict):
    binLenDF = pd.DataFrame.from_dict(binLenDict)
    pp = PdfPages("Bins length distribution(200bp).pdf")
    for col in binLenDF.columns:
        fig = plt.figure()
        bdna = binLenDF[col].dropna()
        plt.hist(bdna, 20, range=(int(min(bdna)), int(max(bdna))))
        plt.title("The chromosome " + col)
        plt.xlabel("The distribution of bin length")
        plt.ylabel("The frequency of the bin length")
        pp.savefig(fig)
    pp.close()

def main():
    binFile, repeatFile = sys.argv[1:]
    binBed = BedFile(binFile)
    repeatBed = BedFile(repeatFile)
    newBinDict = getOverlap(binBed, repeatBed)
    filterNewBinDict, newBinLenDict = filterBin(newBinDict)

    bedOut = open("newBin_200bp.bed", "w")
    dict2bed(filterNewBinDict, bedOut, newBinLenDict)
    bedOut.close()
    plotBinLenDist(newBinLenDict)

if __name__ == '__main__':
    main()
