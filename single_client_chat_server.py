#Apart from typed text messages, in this program, client and server can exchange speech-to-text messages, in a local network
#by taking voice input and converting the audio message into text.

#SERVER SIDE SCRIPT
# -*- coding: utf-8 -*-
'''By Ajay'''

#Importing required libraries
import socket
from threading import Thread
import speech_recognition as sr
import keyboard as kb
import os

#Initiating socket element
s_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Getting server IP address
host=socket.gethostname()
host=socket.gethostbyname(host)
print(host)

#Binding server to IP address and port 
s_socket.bind((host,2527))

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
            if s_message== 'bye' or s_message== 'see ya':    #Condition to disconnect
                c_con.close()
                print('connection closed!')
                os._exit(1)
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
            if r_message== 'bye' or r_message== 'see ya':    #Condition to disconnect
                c_con.close()
                print('connection closed!')
                os._exit(1)
                break
            else:
                continue
    except:
        pass
    
    
#Making a function to convert speech to text and sending it to the client
r=sr.Recognizer()
def s_speech_text():
    try:
      while 1:
        with sr.Microphone() as s:
            kb.wait('esc')
            if kb.is_pressed('esc'):
                print('listening.....')
                r.adjust_for_ambient_noise(s,0.5)
                aud=r.listen(s)
                text_message=r.recognize_google(aud,language='en-IN')
                print(text_message)
                c_con.send(bytes(text_message,'utf-8'))
                if text_message=='bye' or text_message== 'see ya':
                    c_con.close()
                    print('connection closed!')
                    os._exit(1)
                    break
    except Exception as er:
        print(er)
        pass
 
#Putting functions in thread  so that server can receive and send message concurrently
st1=Thread(target=s_send)
st2=Thread(target=s_receive)
st3=Thread(target=s_speech_text)

#Starting threads
st1.start()
st2.start()
st3.start()

#Joining threads
st1.join()
st2.join()
st3.join()

#CLIENT SIDE SCRIPT
# -*- coding: utf-8 -*-
'''By Ajay'''

#Importing required libraries
import socket
from threading import Thread
import speech_recognition as sr
import keyboard as kb
import os

#Initiating socket element
c_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Getting client IP address (although it's not necessarily needed to connect with server)
c_ip=socket.gethostname()
c_ip=socket.gethostbyname(c_ip)
print(c_ip)

#Entering server IP address and connecting at the specified port
server_ip=input('Enter server IP address: ')
c_socket.connect((server_ip,2527))

#Printing confirmation message received from server
print(c_socket.recv(1024).decode('utf-8'))

#Making a function to send messages     
def c_send():
    try:
     while 1:
        c_message=input('')                               #message to be sent
        c_socket.send(bytes(c_message,'utf-8'))           #sending message in bytes
        if c_message== 'bye' or c_message== 'see ya':     #Condition to disconnect
            c_socket.close()
            print('connection closed!')
            os._exit(1)
            break
        else:
            continue
    except:
        pass
                
#Making a function to receive messages     
def c_receive():
    try:
        while 1:
            cr_message=c_socket.recv(1024)                        #receving message in bytes
            cr_message1=cr_message.decode('utf-8')                #decoding message 
            print('Server said: ',cr_message1)
            if cr_message1== 'bye' or cr_message1== 'see ya':     #Condition to disconnect
                c_socket.close()
                print('connection closed!')
                os._exit(1)
                break
            else:
                continue
    except:
        pass
  
#Making a function to convert speech to text and sending it to the client
r=sr.Recognizer()
def c_speech_text():
    try:
      while 1:
        with sr.Microphone() as s:
            kb.wait('ctrl')
            if kb.is_pressed('ctrl'):
                print('listening.....')
                r.adjust_for_ambient_noise(s,0.5)
                aud=r.listen(s)
                text_message=r.recognize_google(aud,language='en-IN')
                print(text_message)
                c_socket.send(bytes(text_message,'utf-8'))
                if text_message=='bye' or text_message== 'see ya':
                    c_socket.close()
                    print('connection closed!')
                    os._exit(1)
                    break
    except Exception as er:
        print(er)
        pass
           
#Putting functions in thread  so that client can receive and send message concurrently
ct1=Thread(target=c_send)
ct2=Thread(target=c_receive)
ct3=Thread(target=c_speech_text)

#Starting threads
ct1.start()
ct2.start()
ct3.start()

#Joining threads
ct1.join()
ct2.join()
ct3.join()
