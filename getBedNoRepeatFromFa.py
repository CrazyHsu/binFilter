#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
File name: getBedNoRepeatFromFa.py
Author: CrazyHsu @ crazyhsu9527@gmail.com 
Created on: 2019-04-23 14:59:07
Last modified: 2019-04-23 14:59:08
'''

import re, sys, gzip, os
from collections import Counter

repeatMask = "N"

def getNoRepeat(repeatDict, chrLenDict):
    noRepeatDict = {}
    for chrId in repeatDict:
        indexList = repeatDict[chrId].keys()
        prev = [0, 0]
        noRepeatDict[chrId] = {}
        for index in xrange(len(indexList)):
            cur = repeatDict[chrId][indexList[index]]
            if index == 0:
                if cur[0] != 0:
                    noRepeatDict[chrId].update({index: [prev[1], cur[0] - 1]})
            else:
                noRepeatDict[chrId].update({index: [prev[1] + 1, cur[0] - 1]})
            prev = cur
        if not repeatDict[chrId]:
            noRepeatDict[chrId].update({0: [0, chrLenDict[chrId] - 1]})
            continue
        if prev[1] < chrLenDict[chrId] - 1:
            noRepeatDict[chrId].update({index + 1: [prev[1] + 1, chrLenDict[chrId] - 1]})
    return noRepeatDict

def printBed(repeatDict, fileOut):
    for chrId in repeatDict:
        for index in repeatDict[chrId]:
            start = repeatDict[chrId][index][0]
            end = repeatDict[chrId][index][1]
            print >>fileOut, "\t".join([str(i) for i in [chrId, start, end, index]])

def processFa(f):
    repeatDict = {}
    chrLenDict = {}
    repeatCount = 0
    currentLen = 0
    chrId = ""
    for i in f:
        if i.startswith(">"):
            chrId = re.split(">|\s+", i.strip())[1]
            currentLen = 0
            # repeatDict[chrId] = {0: [0, -1]}
            repeatDict[chrId] = {}
            chrLenDict[chrId] = 0
            repeatCount = 0
        else:
            if repeatMask in i:
                start = i.index(repeatMask)
                end = i.rindex(repeatMask)
                innerSeq = i[start: end + 1]
                if len(Counter(innerSeq)) == 1:
                    if start != 0:
                        curStart = start + currentLen
                        curEnd = end + currentLen
                        # if repeatDict[chrId][0][1] != -1:
                        #     repeatCount += 1
                        repeatCount += 1
                        repeatDict[chrId].update({repeatCount: [curStart, curEnd]})
                    else:
                        curStart = currentLen
                        curEnd = end + currentLen
                        # print chrId, repeatCount

                        if (repeatCount not in repeatDict[chrId]) or curStart != repeatDict[chrId][repeatCount][1] + 1:
                            repeatCount += 1
                            curStart = start + currentLen
                            curEnd = end + currentLen
                            repeatDict[chrId].update({repeatCount: [curStart, curEnd]})
                        else:
                            repeatDict[chrId][repeatCount][1] = curEnd
                        # if curStart == repeatDict[chrId][repeatCount][1] + 1:
                        #     repeatDict[chrId][repeatCount][1] = curEnd
                        # else:
                        #     repeatCount += 1
                        #     curStart = start + currentLen
                        #     curEnd = end + currentLen
                        #     repeatDict[chrId].update({repeatCount: [curStart, curEnd]})
                else:
                    repeatList = re.findall(repeatMask + "+", i.strip())
                    repeatIndex = 0
                    for j in range(len(repeatList)):
                        repeat = repeatList[j]
                        repeatIndex = i.strip().index(repeat, repeatIndex)
                        newStart = repeatIndex + currentLen
                        newEnd = repeatIndex + currentLen + len(repeat) - 1
                        if start != 0:
                            repeatCount += 1
                            repeatDict[chrId].update({repeatCount: [newStart, newEnd]})
                        else:
                            if j == 0:
                                if repeatCount not in repeatDict[chrId]:
                                    repeatCount += 1
                                    repeatDict[chrId].update({repeatCount: [newStart, newEnd]})
                                else:
                                    repeatDict[chrId][repeatCount][1] = newEnd
                            else:
                                repeatCount += 1
                                repeatDict[chrId].update({repeatCount: [newStart, newEnd]})
                        repeatIndex += len(repeat)
            currentLen += len(i.strip())
            chrLenDict[chrId] = currentLen
    return repeatDict, chrLenDict

def main():
    faFileIn = sys.argv[1]
    basename = os.path.basename(faFileIn)
    name = re.split("\.", basename)[0]
    if faFileIn.endswith(".gz"):
        f = gzip.open(faFileIn, "rb")
    else:
        f = open(faFileIn, "rb")
    repeatDict, chrLenDict = processFa(f)
    # print repeatDict
    noRepeatDict = getNoRepeat(repeatDict, chrLenDict)
    fileOut1 = open(name + ".repeat.bed", "w")
    fileOut2 = open(name + ".norepeat.bed", "w")
    printBed(repeatDict, fileOut1)
    printBed(noRepeatDict, fileOut2)
    fileOut1.close()
    fileOut2.close()

if __name__ == '__main__':
    main()
