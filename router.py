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
from utils import setupserver, setupsock, broadcastcost, sendUmessage
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

args            = parser.parse_args()
testdir         = args.testdir
poisoned        = args.p
routername      = args.routername

links           = readlinks(testdir, routername)
routerlist      = readrouters(testdir)

neighbor = []

for link,linkinfo in links.items():
    neighbor.append([link,linkinfo.cost])

routerx     = Router(routername, neighbor, poisoned)

neighborset = []
broadcaster = setupserver(routerlist[routername].host,routerlist[routername].baseport)
socketmap   = [ routername ]

for host,info in routerlist.items():
    if host in links:
        neighborset.append(setupsock(routerlist[routername].host,routerlist[host].host,\
                                     routerlist[routername].baseport+links[host].locallink,\
                                     routerlist[host].baseport+links[host].remotelink))
        socketmap.append(host)

inputset    = [ broadcaster ]
inputset.extend(neighborset)

#outputset   = inputset[:]

'''
test block
'''

'''
This is the infinite select loop.
We aim to catch messages from neighbors,and other nodes
on appropriate sockets.
inputset: serversocket + neighbor sockets
TIMEOUT = 30sec
if we timeout, we send the 'U' message to all neighbors.

'''
while (True):
    timeout     = 2
    try:
        reader,writer,error = select.select(inputset,[],[],timeout)
    except Exception as e:
        print(e)
        break
    for s in reader:
        data = s.recv(1024)
        if data:
            print('data ' + data.decode())
            changes = False
            if s is broadcaster:
                '''
                    server socket on baseport of current router
                    we can expect to receive P and L messages
                '''
                # we got a message
                if (data[0]=='L'):
                    changes = routerx.linkcostupdate(data)
                elif (data[0]=='P'):
                    routerx.printhandle(data)
                else:
                    print('invalid message type')
            else:
                '''
                    this must be a neighbor socket
                    only U messages expected.
                '''
                base = ''
                for i in range(len(neighborset)):
                    if (neighborset[i]==s):
                        base = socketmap[i+1]
                if (data[0]=='U'):
                    #update message
                    changes = routerx.routerupdate(base,data)
            if changes:
                sendUmessage(neighborset,routerx)
    if not (reader or writer or error):
        '''
        30 sec timeout.
        Send 'U' messages to all neighbors
        '''
        print('sending message')
        routerx.runbellmanford()
        sendUmessage(neighborset,routerx)

#print(outputset,inputset)
