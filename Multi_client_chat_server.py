#Apart from typed text messages, this is a multi-client program in which clients can exchange speech-to-text messages via a server, in a local network
#by taking voice input and converting the audio message into text.

# -*- coding: utf-8 -*-
'''By Ajay'''

#SERVER SIDE SCRIPT

#Importing required libraries
import socket
import threading
import os 

#Initializing server socket object 
soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Getting the IP address of the server
h=socket.gethostname()
host=socket.gethostbyname(h)

#Setting up a port on which chat server will listen
port=5005

#Printing ip address of the chat server device
print(host)

#Binding the chat server socket to the IP address and port
soc.bind((host,port))

#Making the server listen for the incoming client requests
soc.listen(10)          #Listening for 10 clients

#Making an empty list in which we'll add the connected client
client_list=[]
client_address=[]

#Making a function to receive messages from a client and sending to all other clients
def clients(con,ad,client_id):
    var=1
    print(f'connection with {ad} established!')
    con.send(bytes('welcome to the Server.','utf-8'))           #Sending welcome message to the client
    try:
        while var:
            message=con.recv(1024).decode('utf-8')              #Receiving message from the client and decoding it
            print(message)
            message2=client_id+ ' said: '+message
            for c in client_list:                        
                if c!=con:
                    c.send(bytes(message2,'utf-8'))             #Sending message in bytes to every client except the one who sent it
                    if message=='bye' or message=='see ya':     #Condition to disconnect the client
                        con.close()
                        client_list.remove(con)                 #Removing disconnected client from client list
                        var=0
                elif len(client_list)==1:                       #Condition for closing the server
                    con.close()
                    print('Server is closed!')
                    os._exit(1)                                 #Closing the server
                    var=0
                else:
                    pass
    except:
        pass
    
#Creating a server thread for every client that connects
i=1 
while 1:
    con,ad=soc.accept() 
    client_id='client '+str(i)                                #Giving id to every client
    i+=1
    client_list.append(con)                                   #Appending connected clients to the list
    client_address.append(ad[0])                              #Appending clients' address to the list
    thread=threading.Thread(target=clients,args=(con,ad,client_id))   #converting above function into a thread
    thread.start()                                                    #Starting thread
    n_of_threads=threading.activeCount()-1                    #No. of threads generated would be equal to no. of clients connected
    print('active clients are ',n_of_threads)
    print('the client list : ', client_address)
    

#CLIENT SIDE SCRIPT

#CLIENT 1
# -*- coding: utf-8 -*-
'''By Ajay'''

#Importing required libraries
import socket
import threading
import keyboard as kb
import speech_recognition as sr
import os

#Initializing client socket object
coc= socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Getting the IP address of the client (not necessarily required)
host=socket.gethostname()
host=socket.gethostbyname(host)
print(host)

#Specifying the port on which chat server is listening
c_port=5005

#Entering server IP address and connecting at the specified port
server_ip=input('Enter server IP address: ')
coc.connect((server_ip,c_port))

#Receiving welcome message from the server
print(coc.recv(1024).decode('utf-8'))

#Making a function to send speech-to-text message
r=sr.Recognizer()
def speak():
    try:
        while True:
            with sr.Microphone() as s:                             #Initializing microphone to listen
                kb.wait('alt')
                if kb.is_pressed('alt'):                           #Mic will listen only when 'alt' key is pressed
                    print('listening.....')
                    aud=r.listen(s)                                #Getting speech from user
                    c_m=r.recognize_google(aud,language='en-IN')    #Converting speech to text
                    print(c_m)
                    coc.send(bytes(c_m,'utf-8'))                    #sending text to the server in bytes
                    if c_m=='bye' or c_m== 'disconnect':             #Condition to disconnect
                        coc.close()                                #Closing the connection
                        os._exit(1)
                        break
    except:
        pass
    
#Making a function to receive messages of other clients from the server
def receive():
    while 1:
        mess=coc.recv(1024).decode('utf-8')
        print(mess)

#Making a function to send typed text to the server
def send():  
    while 1: 
        c_s= input('')                                              #taking message from the user
        coc.send(bytes(c_s,'utf-8'))                                #Sending message to the server in bytes
        if c_s=='bye' or c_s== 'disconnect':                         
            coc.close()
            os._exit(1)
            break  
        
#Creating threads for above functions so that client can send and receive text concurretly
t1= threading.Thread(target=receive)
t2=threading.Thread(target=send)
t3=threading.Thread(target=speak)

#Starting the threads
t1.start()
t2.start()
t3.start()

 #CLIENT 2
 # -*- coding: utf-8 -*-
'''By Ajay'''

#Importing required libraries
import socket
import threading
import keyboard as kb
import speech_recognition as sr
import os

#Initializing client socket object
coc= socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Getting the IP address of the client (not necessarily required)
h=socket.gethostname()
host=socket.gethostbyname(h)
print(host)

#Specifying the port on which chat server is listening
c_port=5005

#Entering server IP address and connecting at the specified port
server_ip=input('Enter server IP address: ')
coc.connect((server_ip,c_port))

#Receiving welcome message from the server
print(coc.recv(1024).decode('utf-8'))

#Making a function to send speech-to-text message
r=sr.Recognizer()
def speak():
    try:
        while True:
            with sr.Microphone() as s:                                  #Initializing microphone to listen
                kb.wait('ctrl')
                if kb.is_pressed('ctrl'):                               #Mic will listen only when 'ctrl' key is pressed
                    print('listening.....')
                    aud=r.listen(s)                                     #Getting speech from user
                    c_m=r.recognize_google(aud,language='en-IN')         #Converting speech to text
                    print(c_m)
                    coc.send(bytes(c_m,'utf-8'))                         #sending text to the server in bytes
                    if c_m=='bye' or c_m== 'disconnect':                  #Condition to disconnect
                        coc.close()                                     #Closing the connection
                        os._exit(1)
                        break
    except:
        pass

#Making a function to receive messages of other clients from the server
def receive():
    while 1:
        mess=coc.recv(1024).decode('utf-8')
        print(mess)

#Making a function to send typed text to the server
def send():  
    while 1: 
        c_s= input('')                                                   #taking message from the user
        coc.send(bytes(c_s,'utf-8'))                                     #Sending message to the server in bytes
        if c_s=='bye' or c_s== 'disconnect':
            coc.close()
            os._exit(1)
            break  
        
#Creating threads for above functions so that client can send and receive text concurretly
t1=threading.Thread(target=receive)
t2=threading.Thread(target=send)
t3=threading.Thread(target=speak)

#Starting the threads
t1.start()
t2.start()
t3.start()

#CLIENT 3
# -*- coding: utf-8 -*-
'''By Ajay'''

#Importing required libraries
import socket
import threading
import keyboard as kb
import speech_recognition as sr
import os

#Initializing client socket object
coc= socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Getting the IP address of the client (not necessarily required)
host=socket.gethostname()
host=socket.gethostbyname(host)
print(host)

#Specifying the port on which chat server is listening
c_port=5005

#Entering server IP address and connecting at the specified port
server_ip=input('Enter server IP address: ')
coc.connect((server_ip,c_port))

#Receiving welcome message from the server
print(coc.recv(1024).decode('utf-8'))

#Making a function to send speech-to-text message  
r=sr.Recognizer()
def speak():
    try:
        while 1:
            with sr.Microphone() as s:                                  #Initializing microphone to listen
                kb.wait('esc')
                if kb.is_pressed('esc'):                                #Mic will listen only when 'ctrl' key is pressed
                    print('listening.....')
                    aud=r.listen(s)                                     #Getting speech from user
                    c_m=r.recognize_google(aud,language='en-IN')         #Converting speech to text
                    print(c_m)
                    coc.send(bytes(c_m,'utf-8'))                         #sending text to the server in bytes
                    if c_m=='bye' or c_m== 'disconnect':                  #Condition to disconnect
                        coc.close()                                     #Closing the connection
                        os._exit(1)
                        break
    except:
        pass

#Making a function to receive messages of other clients from the server
def receive():
    while 1:
        mess=coc.recv(1024).decode('utf-8')
        print(mess)
        
#Making a function to send typed text to the server
def send():  
    while 1: 
        c_s= input('')                                                   #taking message from the user       
        coc.send(bytes(c_s,'utf-8'))                                     #Sending message to the server in bytes
        if c_s=='bye' or c_s== 'disconnect':
            coc.close()
            os._exit(1)
            break 

#Creating threads for above functions so that client can send and receive text concurretly
t1=threading.Thread(target=receive)
t2=threading.Thread(target=send)
t3=threading.Thread(target=speak)

#Starting the threads
t1.start()
t2.start()
t3.start()


   

    
