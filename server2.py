#!/usr/bin/python3


import errno
import struct
import sys
from socket import *
import binascii

def sendall(socket, a, b, c, win, legal_move):
    data=( a, b, c, win, legal_move)
    print(*data)
    packed_data=pack.pack(*data)
    return socket.send(packed_data)

while True:
    n_a=0
    n_b=0
    n_c=0
    port=6444

    if (len(sys.argv)<4):
        print ("Not enough arguments")
        sys.exit()

    try:

        if (2 <= len(sys.argv) <= 5):
            if ( 1 <= int(sys.argv[1]) <= 1000 and 1 <= int(sys.argv[2]) <= 1000 and 1 <= int(sys.argv[3]) <= 1000):
                n_a=int(sys.argv[1])
                n_b=int(sys.argv[2])
                n_c=int(sys.argv[3])

            else:
                print("size not an integer between 1 and 1000, Try again")
                sys.exit()

    except ValueError:
        print ("The input given is not valid integer. Try again")
        sys.exit()


    if (len(sys.argv)>4):
        try:
            if ( 0 <= int(sys.argv[4]) <= 65535):
                port=int(sys.argv[4])
            else:
                print("The input port value is  outside the range of 0 and 65535, using default port: 6444")
        except (ValueError):
            print("The input port is not valid integer, using default port: 6444")

    try:
         listeningSocket=socket(AF_INET, SOCK_STREAM)
         listeningSocket.bind (('', port))
         listeningSocket.listen(5)
    except OSError:
         print ("port already in use. Try another port")
         sys.exit()

    unpack=struct.Struct('HH')
    pack=struct.Struct('HHHHH')

    while (True):
        try:
            listeningSocket.listen(5)
            (soc, address)=listeningSocket.accept()
            a=n_a
            b=n_b
            c=n_c
            legal_move=1
            win=0
            sendall(soc,a, b, c, win, legal_move)
            play=True
            while (play):
                data_client=soc.recv(unpack.size)
                unpack_data=unpack.unpack(data_client)
                heap=unpack_data[0]
                num=unpack_data[1]
                legal_move = 1

                if (num>0):
                    if (heap==0): #heap A
                        a-=num
                    elif (heap==1): #heap B
                        b-=num
                    elif (heap==2): #heap C
                        c-=num
                    else:
                        legal_move=0

                else:
                    legal_move=0

                if (a==0 and b==0 and c==0):
                    win=1
                    play=False

                elif(legal_move != 0):
                    if (a>=b and a>=c):
                        a-=1
                    elif (b>=a and b>=c):
                        b-=1
                    else:
                        c-=1

                    if (a==0 and b==0 and c==0):
                        win=2
                        play=False

                sendall(soc, a, b, c, win, legal_move)
                    



        except KeyboardInterrupt:
            soc.shutdown(SHUT_WR)
            soc.close()

        finally:
            soc.shutdown(SHUT_WR)
            soc.close()






