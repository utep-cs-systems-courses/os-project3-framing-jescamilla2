#! /usr/bin/env python3

# client program
import socket, sys, re, time, os
sys.path.append("../lib")       # for params
import params
import mytar.py

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "filetransferClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)
    
'''
delay = float(paramMap['delay']) # delay before reading (default = 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(int(delay))
    print("done sleeping")
'''

outMessage = "Hello world!".encode()
while len(outMessage):
    print("sending '%s'" % outMessage.decode())
    bytesSent = s.send(outMessage)
    outMessage = outMessage[bytesSent:]

data = s.recv(1024).decode()
print("Received '%s'" % data)

'''
outMessage = "Hello world!"
while len(outMessage):
    print("sending '%s'" % outMessage)
    bytesSent = s.send(outMessage.encode())
    outMessage = outMessage[bytesSent:]
'''

# s.shutdown(socket.SHUT_WR)      # no more output


while 1:

    
    # the original code from demo
    data = s.recv(1024).decode()
    print("Received '%s'" % data)
    if len(data) == 0:
        break
 

    '''
    # -----BEGIN-----
    data = framer.recv_file(s)

    if data is None:
        break

    print("Received '%s'" % data)
    # -----END-----
    '''
    
print("Zero length read.  Closing")
s.close()

