#The code to send and receive multiple messages between a client and a server concurrently, in a local network.
#SERVER SIDE SCRIPT

# -*- coding: utf-8 -*-
'''By Ajay'''

#Importing required libraries
import socket
from threading import Thread

#Initiating socket element
s_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Getting server IP address
host=socket.gethostname()
host=socket.gethostbyname(host)
print(host)

#Binding server to IP address and port 
s_socket.bind((host,2525))

#Making the server listen for a connection
s_socket.listen(1)

#Accepting client and storing client's IP address
c_con,c_adr=s_socket.accept()

#Printing a message to make sure that client is connected
print(f'connection with {c_adr} established')

#Sending confirmation message to client
c_con.send(bytes('You are connected!','utf-8')) 

#Making a function to send messages     
def s_send():
    try:
        while 1:
            s_message=input('')                              #message to be sent
            c_con.send(bytes(s_message,'utf-8'))             #sending message in bytes
            if s_message== 'Bye' or s_message== 'See ya':    #Condition to disconnect
                c_con.close()
                break
            else:
                continue
    except:
        pass         
  
#Making a function to receive messages     
def s_receive():
    try:
        while 1:
            r_message=c_con.recv(1024)                       #receving message in bytes
            r_message=r_message.decode('utf-8')              #decoding message 
            print('Client said: ',r_message)
            if r_message=='Bye' or r_message=='See ya':      #condition to disconnect
                c_con.close()
                break
            else:
                continue
    except:
        pass
 
#Putting functions in thread  so that server can receive and send message concurrently
st1=Thread(target=s_send)
st2=Thread(target=s_receive)

#Starting threads
st1.start()
st2.start()
   


#CLIENT SIDE SCRIPT

# -*- coding: utf-8 -*-
'''By Ajay'''

#Importing required libraries
import socket
from threading import Thread

#Initiating socket element
c_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Getting client IP address (although it's not necessarily needed to connect with server)
c_ip=socket.gethostname()
c_ip=socket.gethostbyname(c_ip)
print(c_ip)

#Entering server IP address and connecting at the specified port
server_ip=input('Enter server IP address: ')
c_socket.connect((server_ip,2525))

#Printing confirmation message received from server
print(c_socket.recv(1024).decode('utf-8'))

#Making a function to send messages     
def c_send():
    try:
     while 1:
        c_message=input('')                               #message to be sent
        c_socket.send(bytes(c_message,'utf-8'))           #sending message in bytes
        if c_message== 'Bye' or c_message== 'See ya':     #Condition to disconnect
            c_socket.close()
            break
        else:
            continue
    except:
        pass
                
#Making a function to receive messages     
def c_receive():
    try:
        while 1:
            cr_message=c_socket.recv(1024)                       #receving message in bytes
            cr_message1=cr_message.decode('utf-8')               #decoding message 
            print('Server said: ',cr_message1)
            if cr_message1=='Bye' or cr_message1=='See ya':      #condition to disconnect
                c_socket.close()
                break
            else:
                continue
    except:
        pass
            
#Putting functions in thread  so that client can receive and send message concurrently
ct1=Thread(target=c_send)
ct2=Thread(target=c_receive)

#Starting threads
ct1.start()
ct2.start()
    
