#!/usr/local/bin/python


import socket                   # Import socket module
import sys
import os
import hashlib
import datetime
import commands

def fileSend_tcp(command):
    #port = 60000                    # Reserve a port for your service.
    global filePort
    s = socket.socket()#socket.AF_INET, socket.SOCK_DGRAM)             # Create a socket object
    host = socket.gethostname()     # Get local machine name
    s.bind((host, filePort))            # Bind to the port
    s.listen(5)                     # Now wait for client connection.
    
    print 'Server listening....'
    
    conn, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    
    filename = command.split()[-1]
    f = open(filename,'rb')
    
    l = f.read(os.stat(filename).st_size)
    while (l):
        conn.send(l)
        #print('Sent ',repr(l))
        l = f.read(1024)
    f.close()

    print('Done sending')
    
    s.close()
    conn.close()
    print filename, os.stat(filename).st_size, datetime.datetime.fromtimestamp(os.stat(filename).st_mtime).strftime('%c'), md5(filename)

  
  
  
def fileSend_udp(filename):

    #s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #host = socket.gethostname()
    #global filePort
    #print filePort
    
    global udp_port
    
    f = open(filename, "rb")
    data = f.read(1024)
    
    s_udp.sendto(filename, (host, udp_port))
    
    while(data):
        if(s_udp.sendto(data, (host, udp_port))):
            print "Sending file ..."
            data = f.read(1024)
    
    #s_udp.close()
    f.close()
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
    
    s_fileHash.bind((host, filePort))
   
    s_fileHash.listen(5)                     # Now wait for client connection.
    
    print 'Server listening....'
    
    conn, addr = s_fileHash.accept()     # Establish connection with client.
    print 'Got connection from', addr
    
    if command.split()[1].upper() == "VERIFY":
        conn.send(md5(command.split()[-1]) + " " + str(os.stat(command.split()[-1]).st_mtime))
    
    if command.split()[1].upper() == "CHECKALL":
        files = commands.getoutput('ls').split('\n')
        #print files
        os.system('rm -f fhash 2> /dev/null')

        with open("fhash", "wb") as f:
            for i in files:
                data = i + " " + md5(i) + " " + str(os.stat(i).st_size)
                f.write(data + '\n')
        f.close()
        
        """
        f = open('fhash','rb')
    
        l = f.read(os.stat('fhash').st_size)
        while (l):
            conn.send(l)
            #print('Sent ',repr(l))
            #l = f.read(1024)
            l = f.readline()
        f.close()
        """
        with open('fhash', "rb") as f:
            content = f.readlines()
        f.close()
        
        """count = 0
        
        for data in content:
            count += 1
            
        conn.send(str(count))"""
        
        for data in content:
            #print data
            conn.send(data)
        
        os.system('rm fhash 2> /dev/null')       
    
    s_fileHash.close()
    conn.close()    
     
     
     
def flagcommand(data):
#    port = 60000
    global filePort
    print filePort
    s_flag=socket.socket()
    host = socket.gethostname()     # Get local machine name
    s_flag.bind((host, filePort))            # Bind to the port
    s_flag.listen(5)                     # Now wait for client connection.
    conn, addr = s_flag.accept()     # Establish connection with client.
    #data = conn.recv(1024)
    # print('Server received', repr(data))
#    data = conn.recv(1024)
    #print('Server received', repr(data))

    if data.split()[1] == "longlist":
       '''os.system("rm out.txt 2> /dev/null")
       os.system("ls -l >out.txt")

       filename='out.txt'
       f = open(filename,'rb')
       l = f.read(1024)


       conn.send(l)
       print('Sent ',repr(l))
       #l = f.read(1024)
       f.close()  '''
       file_ls = commands.getoutput('ls').split('\n')
       #length = len(file_ls)
       #j = 0
       #while j in range(0,length) :
       for x in file_ls:
         #x = file_ls[j]
         value = commands.getoutput("ls -l %s | awk '{print $1,$5,$6,$7,$8,$9}'" %x)
         print value
         conn.send(value)
         #j = j+1
       conn.close()
       s_flag.close()
    elif data.split()[1] == "shortlist":
       a = data.split()[2]  #start year
       b = data.split()[3]  #start month  
       c = data.split()[4]  #start day
       d = data.split()[5]  #start time
       e = data.split()[6]  #end year
       f = data.split()[7]  #end month 
       g = data.split()[8]  #end day
       h = data.split()[9]  #end time
       
       print a, b, c, d, e, f, g, h

       '''os.system("rm filetext.txt 2> /dev/null")
       os.system('find . -type f -newermt "%s-%s-%s %s" ! -newermt "%s-%s-%s %s" > filetext.txt'%(a,b,c,d,e,f,g,h) )

       filename = 'filetext.txt'
       f= open(filename, 'rb')
       l = f.read(1024)

       conn.send(l)
       print('Sent',repr(l))
       f.close()'''

       file_shortlist = commands.getoutput('find . -type f -newermt "%s-%s-%s %s" ! -newermt "%s-%s-%s %s"' %(a,b,c,d,e,f,g,h)).split('\n')
       print file_shortlist

       #length = len(file_ls)
       #j = 0
       #while j in range(0,length):
        #x =  file_ls[j]
        #value = commands.getoutput("ls -l %s | awk '{print $1,$5,$6,$7,$8,$9}'" %x)
        #conn.send(value)
        #j=j+1
       
       if file_shortlist == ['']:
           conn.send('')
       else: 
           for target in file_shortlist:
               val = commands.getoutput("ls -l %s | awk '{print $1,$5,$6,$7,$8,$9}'" %target)
               print val
               conn.send(val)


       print('Done sending')
    #conn.send('Thank you for connecting')
       conn.close()
       s_flag.close()

 
    
        

def parse(command):

    global filePort
    
    if command.split()[0].upper() == "FILEDOWNLOAD":
        if command.split()[1].upper() == "UDP":
            #pass
            fileSend_udp(command.split()[-1])
        else:
            fileSend_tcp(command.split()[-1])
    elif command.split()[0].upper() == "INDEXGET":
        flagcommand(command)
    elif command.split()[0].upper() == "FILEHASH":
        FileHash(command)            
            
    filePort = filePort - 1   
        


def run():
    port = 49152
    s_run = socket.socket()
    host = socket.gethostname()
    s_run.bind((host, port))
    
    s_run.listen(5)
    
    print 'Server listening....'
    
        
    while True:
        
        
        conn, addr = s_run.accept()     # Establish connection with client.
        print 'Got connection from', addr
                
        while True:
            command = conn.recv(1024)
        
            if command.upper() == "EXIT":
                conn.close()
                s_run.close()
                s_udp.close()
                print 'Exiting ... Connection Closed'
                sys.exit(0)
            else:
                parse(command)              
               
        
    conn.close()
            
        

if __name__ == "__main__":
    filePort = 65535
    
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = socket.gethostname()
    udp_port = 49151
    
    run()