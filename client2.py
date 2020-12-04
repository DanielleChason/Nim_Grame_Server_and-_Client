!/usr/bin/python3


import errno
import struct
import sys
from socket import *
import binascii

def sendall(socket, heap, num):
    data=(socket, heap, num)
    packed_data=pack.pack(*data)
    return socket.send(packed_data)

port=6444
hostname='localhost'

if (len(sys.argv)>=2):
    hostname=int(sys.argv[1])

if (len(sys.argv>=3)):
    try:
        if (int(sys.argv[2])>=0 and int(sys.argv)<=65535):
            host=int(sys.argv[2])
        else:
            print ("Invalid input for port, using default 6444")
    except ValueError:
        print ("Invalid input for port, using default 6444 ")

unpack=struct.Struct('HH')
pack=struct.Struct('HHHHH')

try:
    soc=socket.Socket(socket.AF_INET, socket.SOCK_STREAM)
    address=(hostname, port)
    soc.connect(address)
except OSError as err:
    if (err.errno==errno.ECONNREFUSED):
        print ("Connection refused by the server")
        exit()
    else:
        print (err.strerror)

try:
    play=True
    while (play):
        data_server=soc.recv()
        unpack_data=unpack.unpack(data_server)
        a=int(unpack_data[0])
        b=int(unpack_data[1])
        c=int(unpack_data[2])
        win=int(unpack_data[3])
        legal_move=int(unpack_data[4])

        if (legal_move==0):
            print ("Illegal move")
        elif (legal_move==1):
            print ("Move accepted")
        print ("Heap A: ", a)
        print ("Heap B: ", b)
        print ("Heap C: ", c)

        if (win==1):
            print ("You win!")
            play=False
        if (win==2):
            print ("You lose!")
            play=False

        if (play):
            print ("Your turn!")
            arg=input().split()
            heap=0
            num=0
            if (len(arg)==2):
                if (arg[0]=="A"):
                    heap=0
                elif (arg[0]=="B"):
                    heap=1
                elif (arg[0]=="C"):
                    heap=2
                else:
                    print ("Invalid character for heap")

                if (arg[1]>0 and arg[1]<1001):
                    num=arg[1]
                else:
                    print ("Invalid number")

            sendall(soc, heap, num)

except OSError as err:
    if (err.errno==errno.ECONNREFUSED):
        print (err.strerror)
        soc.close()
finally:
        soc.close()


