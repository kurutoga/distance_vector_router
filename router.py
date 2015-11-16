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
import sys, select
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

neighborset = []
broadcaster = setupserver(routerlist[routername].host,routerlist[routername].baseport)

for host,info in routerlist.items():
    if host in links:
        neighborset.append(setupsock(routerlist[routername].host,routerlist[host].host,\
                                     routerlist[routername].baseport+links[host].locallink,\
                                     routerlist[host].baseport+links[host].remotelink))

inputset    = [ broadcaster ]
inputset.extend(neighborset)

outputset   = inputset[:]

'''
This is the infinite select loop.
We aim to catch messages from neighbors,and other nodes
on appropriate sockets.
inputset: serversocket + neighbor sockets
outputset: serversocket (for 'L' messages) and
           neighborset  (for 'U' messages)

TIMEOUT = 30sec
if we timeout, we send the 'U' message to all neighbors.

'''
while (True):
    timeout     = 30
    try:
        reader,writer,error = select.select(inputset,outputset,[],timeout)
    except Exception as e:
        print(socket.error,e)
        break
    for s in reader:
        if s is broadcaster:
            '''
                server socket on baseport of current router
                we can expect to receive P and L messages
            '''
            pass

        else:
            '''
                this must be a neighbor socket
                only U messages expected.
            '''
            pass
    if not (reader or writer or error):
        '''
        30 sec timeout.
        Send 'U' messages to all neighbors
        '''
        distancevector = routerx.getdistancevector()
        for sock in neighborset:
            broadcastcost(sock, distancevector)
        


#print(outputset,inputset)




