import socket,sys,time
from select import select

def broadcastlink(sock,cost):
    message = 'L '+str(cost)
    sock.send(message)

def broadcastcost(sock, nodes):
    message = 'U '
    for node,cost in nodes:
        message+=node+' '+str(cost)
    sock.send(message)

def setupserver(host,baseport):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('',baseport))
    return sock

def setupsock(host,remotehost,localport,remoteport):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((host,localport))
        sock.connect((remotehost,remoteport))
        return sock
    except:
        print('ERROR')
        sys.exit(1)
        
