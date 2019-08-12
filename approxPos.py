#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
File name: approxPos.py
Author: CrazyHsu @ crazyhsu9527@gmail.com 
Created on: 2019-04-24 17:20:59
Last modified: 2019-04-24 17:21:00
'''
import re, sys, math

def process(fileIn):
    with open(fileIn) as f:
        for i in f:
            infoList = re.split("\t", i.strip())
            start = float(infoList[1])
            end = float(infoList[2])
            newStart = math.floor(start)
            newEnd = math.floor(end)
            print "\t".join([str(int(j)) for j in [infoList[0], newStart, newEnd, infoList[3]]])

def main():
    fileIn = sys.argv[1]
    process(fileIn)

if __name__ == '__main__':
    main()
