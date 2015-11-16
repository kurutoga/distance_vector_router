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
from readrouters import readlinks, readrouters
from utils import setupserver, setupsock, broadcastcost
from models import Router

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


links           = readlinks(testdir, routername)
routerlist      = readrouters(testdir)

neighbor = []

for link,linkinfo in links.items():
    neighbor.append([link,linkinfo.cost])


routerx     = Router(routername, neighbor, poisoned)
#print(routerx)
#print(routerx.node)
#print(routerx.name)
#print(routerx.neighbors)
#print(routerx.table)
#routerx.printhandle('P')

neighborset = []
nodeset     = []

for host,info in routerlist.items():
    if host in links:
        neighborset.append(setupsock(routerlist[host].host,routerlist[routername].baseport+links[host].locallink,routerlist[host].baseport+links[host].remotelink))
print(neighborset)



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

