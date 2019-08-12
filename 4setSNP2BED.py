#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
File name: 4setSNP2BED.py
Author: CrazyHsu @ crazyhsu9527@gmail.com 
Created on: 2019-04-28 21:29:17
Last modified: 2019-04-28 21:29:18
'''
import re, sys

def process(fileIn):
    with open(fileIn) as f:
        for i in f:
            infoList = re.split("chr|\.|_", i.strip())
            chrId = infoList[1]
            pos = infoList[-1]
            start = end = int(pos) - 1
            print "\t".join([str(j) for j in [chrId, start, end, i.strip()]])

def main():
    fileIn = sys.argv[1]
    process(fileIn)

if __name__ == '__main__':
    main()
