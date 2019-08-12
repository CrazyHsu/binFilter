#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
File name: filterBlatByIdentity.py
Author: CrazyHsu @ crazyhsu9527@gmail.com 
Created on: 2019-05-15 10:46:03
Last modified: 2019-05-15 10:46:04
'''

import re, sys
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

def processBlatOut(fileIn):
    with open(fileIn) as f:
        snpInLevels = {}
        for i in f:
            infoList = re.split("\t", i.strip())
            blat = BlatOut(infoList)
            if float(blat.mismatch) + float(blat.identity) != float(blat.length):
                continue
            level = judgeIdentity(float(blat.identity))
            if level not in snpInLevels:
                snpInLevels[level] = [blat]
            else:
                snpInLevels[level].append(blat)
        return snpInLevels

def printOut(snpInLevels):
    for level in snpInLevels:
        snps = snpInLevels[level]
        uniqueSnps = set([i.query for i in snps])
        print "\t".join([str(i) for i in [level, levelDict[level], len(snps), len(uniqueSnps)]])

def printSnpsInLevels(snpInLevels, levelNum):
    for i in range(1, levelNum + 1):
        snps = snpInLevels[i]
        uniqueSnps = list(set([i.query for i in snps]))
        for snp in uniqueSnps:
            print >>sys.stderr, snp

def main():
    fileIn = sys.argv[1]
    snpInLevels = processBlatOut(fileIn)
    printOut(snpInLevels)
    levelNum = 6
    printSnpsInLevels(snpInLevels, levelNum)

if __name__ == '__main__':
    main()
