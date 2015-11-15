#!/usr/bin/python3
'''
Introduction to Computer Networking -- CPTS 455 
------------------------------------------------
PROJECT 2: Distance-Vector Router
// Structure:
    router.py : main program file
    models.py : functions and class definitions
                Router Class has implementation of 
                Bellman-Ford.


'''
import sys
from argparser import ArgumentParser as cliparser
from readrouters import readlinks, readroutes

'''
argparser is in python3 standard library
command line parsing. format: router [-p] testdir routername
we extract, testdir, routername
NOTE: using readroutes, readlinks from skeleton
'''


parser = cliparser(description='router')
parser.add_argument('-p', action='store_true')
parser.add_argument('testdir')
parser.add_argument('routername')

args = parser.parse_args()
testdir     = args.testdir
poisoned    = args.p
routername  = args.routername


links       = readlinks(testdir, routername)
routers     = readroutes(testdir)

for 

## init routing table
## connect to neighbours
## start an async server
## LOOP 
##  on update/link change
##      change routing table
##      forward/inform neighnours
##      continue forever;


## 1. init routing table

#vars
routing_table={}

