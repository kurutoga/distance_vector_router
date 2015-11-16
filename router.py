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
    utils.py  : DGRAM socket setup
                DGRAM connected socket setup
                broadcast cost to given server


'''
import sys
from argparse import ArgumentParser as cliparser
from readrouter import readlinks, readroutes
from utils import setupserver, setupsock, broadcastcost

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
routelist   = readroutes(testdir)

for routers in routelist:
    print(routers)

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

