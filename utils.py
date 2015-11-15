import socket,sys,time
from select import select

def broadcastcost(sock, nodes):
    message = 'U '
    for node,cost in nodes:
        message+=node+' '+str(cost)
    sock.send(message)

def setupserver(baseport):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind('',baseport)
    return sock

def setupsock(host,localport,remoteport):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind('',port)
        sock.connect(host,remoteport)
        return sock
    except Exception,e:
        print("Error: ",Exception,e)
        return



