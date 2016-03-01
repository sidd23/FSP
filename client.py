#!usr/local/bin/python

import socket                   # Import socket module
import sys
import time
import os
import select
import hashlib
import datetime

def fileDownload_tcp(filename):

    s = socket.socket()#socket.AF_INET, socket.SOCK_DGRAM)             # Create a socket object
    host = socket.gethostname()     # Get local machine name
    global filePort # Reserve a port for your service.

    s.connect((host, filePort))

    with open(filename, 'wb') as f:
        print 'file opened'
        while True:
            print('receiving data...')
            data = s.recv(1024)
            #print('data=%s', (data))
            if not data:
                break
            # write data to a file
            f.write(data)

    f.close()
    print('Successfully get the file')
    s.close()
    print('connection closed')
    print filename, os.stat(filename).st_size, datetime.datetime.fromtimestamp(os.stat(filename).st_mtime).strftime('%c'), md5(filename)




def fileDownload_udp(filename):
    #s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #host = socket.gethostname()
    #global filePort
    ##filePort = 60000
    #print filePort
    #s_udp.bind((host, filePort))

    global s_udp
    #global udp_port

    data, addr = s_udp.recvfrom(1024)
    print "Received File:",data.strip()
    f = open(data.strip(),'wb')

    data, addr = s_udp.recvfrom(1024)
    try:
        while(data):
            f.write(data)
            s_udp.settimeout(2)
            data,addr = s_udp.recvfrom(1024)
    except socket.timeout:
        f.close()
        #s_udp.close()
        print "File Downloaded"
        print filename, os.stat(filename).st_size, datetime.datetime.fromtimestamp(os.stat(filename).st_mtime).strftime('%c'), md5(filename)



def md5(filename):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()


def FileHash(command):
    s_fileHash = socket.socket()
    host = socket.gethostname()
    global filePort

    s_fileHash.connect((host, filePort))

    #s_fileHash.send(flag + " " + filename)
    s_fileHash.send(command)

    if command.split()[1].upper() == "VERIFY":
        data = s_fileHash.recv(1024)
        checksum_server = data.split()[0]
        mtime_server = data.split()[1]

        """if(checksum_server == md5(command.split()[-1]) and float(mtime_server) == os.stat(filename).st_mtime):
            print data + " YES"
        else:
            print data + " NO"
            """
        print data

    elif command.split()[1].upper() == "CHECKALL":

        """with open('fhash', 'wb') as f:
            print 'file opened'
            while True:
                print('receiving data...')
                data = s_fileHash.recv(1024)
                #print('data=%s', (data))
                if not data:
                    break
                # write data to a file
                f.write(data)
        f.close()"""

        #os.system('cat fhash')

        count = s_fileHash.recv(1024)
        '''while True:
            data = s_fileHash.recv(1024)
            print data
            if not data:
                break
                '''

        print count

        #for i in range(int(count)):
         #   data = s_fileHash.recv(1024)
         #   sys.stdout.write(data + "\n")


    s_fileHash.close()





def flagcommand(flag):

    global stack
    global i
#    port=60000
    global filePort
    print filePort
    s_flag=socket.socket()
    host=socket.gethostname()

    s_flag.connect((host, filePort))
    #s_flag.send("Hello server!")
    stack.append(flag)
    #print stack[i]
    i=i+1
    #s_flag.send(flag)


    print('receiving data...')

    while True:
      data = s_flag.recv(1024)
      if not data:
          break
      print(data)

    #info = s_flag.recv(1024)
    #print(info)
    s_flag.close()






def parse(command):

    global filePort

    if command.split()[0].upper() == "FILEDOWNLOAD":
        filename = command.split()[-1]
        if command.split()[1].upper() == "UDP":
            #pass
            time.sleep(3)
            fileDownload_udp(filename)
        else:
            time.sleep(3)
            fileDownload_tcp(filename)
    elif command.split()[0].upper() == "INDEXGET":
        time.sleep(1)
        flagcommand(command)
    elif command.split()[0].upper() == "FILEHASH":
        FileHash(command)
    elif command.upper() == "EXIT":
        sys.exit(0)

    filePort = filePort - 1



def run():
    port = 49152
    s_run = socket.socket()
    host = socket.gethostname()

    command = raw_input("$ -> ")

    s_run.connect((host, port))

    while True:

        time.sleep(0.1)
        s_run.send(command)

        time.sleep(0.5)
        parse(command)

        time.sleep(0.3)
        command = raw_input("$ -> ")

        if command.upper() == "EXIT":
            s_udp.close()
            s_run.send(command)
            s_run.close()
            print 'Exiting ... Connection Closed'
            sys.exit(0)



if __name__ == "__main__":
    i = 0
    stack= []
    filePort =  65535

    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = socket.gethostname()
    udp_port = 49151
    s_udp.bind((host, udp_port))

    run()
