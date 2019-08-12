#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
File name: filterBlatByIdentity_batch.py
Author: CrazyHsu @ crazyhsu9527@gmail.com 
Created on: 2019-05-15 10:46:03
Last modified: 2019-05-15 10:46:04
'''

import re, sys, os, random
import pandas as pd

levelDict = {
    1: "100%",
    2: "99%-100%",
    3: "98%-99%",
    4: "97%-98%",
    5: "96%-97%",
    6: "95%-96%",
    7: "94%-95%",
    8: "93%-94%",
    9: "92%-93%",
    10: "91%-92%",
    11: "90%-91%",
    12: "<90%"
}

class BlatOut(object):
    def __init__(self, record):
        self.query = record[0]
        self.refChrId = record[1]
        self.identity = record[2]
        self.length = record[3]
        self.mismatch = record[4]
        self.infoList = record[5:]

def judgeIdentity(identity):
    if identity == 100:
        return 1
    if 99 <= identity < 100:
        return 2
    if 98 <= identity < 99:
        return 3
    if 97 <= identity < 98:
        return 4
    if 96 <= identity < 97:
        return 5
    if 95 <= identity < 96:
        return 6
    if 94 <= identity < 95:
        return 7
    if 93 <= identity < 94:
        return 8
    if 92 <= identity < 93:
        return 9
    if 91 <= identity < 92:
        return 10
    if 90 <= identity < 91:
        return 11
    if identity < 90:
        return 12

def processBlatOut(fileInList):
    snpInLevels = {}
    for fileIn in fileInList:
        with open(fileIn) as f:
            snpInLevels[fileIn] = {}
            for i in f:
                infoList = re.split("\t", i.strip())
                blat = BlatOut(infoList)
                if float(blat.mismatch) + float(blat.identity) != float(blat.length):
                    continue
                level = judgeIdentity(float(blat.identity))
                if level not in snpInLevels[fileIn]:
                    snpInLevels[fileIn][level] = [blat]
                else:
                    snpInLevels[fileIn][level].append(blat)
    return snpInLevels

def mergeLevelInFiles(snpInLevels):
    newDict = {}
    for fileIn in snpInLevels:
        newFileName = os.path.basename(fileIn)
        newDict[newFileName] = {}
        for level in snpInLevels[fileIn]:
            snps = snpInLevels[fileIn][level]
            uniqueSnps = set([i.query for i in snps])
            newDict[newFileName][level] = len(uniqueSnps)
            # print "\t".join([str(i) for i in [level, levelDict[level], len(snps), len(uniqueSnps)]])
    newdf = pd.DataFrame.from_dict(newDict)
    newdf.to_csv("mergedSNPinLevels.txt", sep="\t", header=True, index=True)
    # return newDict

def printSnpsInLevels(snpInLevels, levelNum, speciesNum=5):
    newDict = {}
    for fileIn in snpInLevels:
        newFileName = os.path.basename(fileIn)
        newDict[newFileName] = {}
        for i in range(1, levelNum + 1):
            newDict[newFileName][i] = snpInLevels[fileIn][i]
    newdf = pd.DataFrame.from_dict(newDict)
    queryDict = {}
    for index, row in newdf.iterrows():
        queryDict[index] = []
        for i in newdf.columns:
            queryDict[index].append([j.query for j in row[i]])
    querydf = pd.DataFrame.from_dict(queryDict)
    if speciesNum != 5:
        l = sorted(random.sample(querydf.index, speciesNum))
        querydf = querydf.loc[l, :]
    print "The overlap between %d genomes" % speciesNum
    for col in querydf.columns:
        myList = list(set.intersection(*map(set, querydf.loc[:, col])))
        print col, levelDict[col], len(myList)
    # return newDict

def main():
    fileInList = sys.argv[1:]
    snpInLevels = processBlatOut(fileInList)
    # mergeLevelInFiles(snpInLevels)
    levelNum = 6
    printSnpsInLevels(snpInLevels, levelNum, 3)

if __name__ == '__main__':
    main()
