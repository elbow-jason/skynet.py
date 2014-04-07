from socketIO_client import SocketIO
import socket
import logging

''' This script runs on my Rapsberry Pi
    It connect to Skynet and starts listening to messages
    It can send an sms to any Belgian mobile number +324[789]
    You can test and send a message to my personal number +32485063730'''
logging.basicConfig(level=logging.DEBUG)
outputOn=""
outputEmit=""
socketId=""
socketIO=""
uuid="0c132b91-bcf1-11e3-a3c6-0b41aaf824e3"
token="000tfb92effmvdyrpb91svusl3ngsyvi"

def on_message(*args):
    print('Incomming message')
    response= args[0]
    global socketIO
    global outputOn
    ##{u'fromUuid': u'30ebecc1-b2cb-11e3-a36b-61e66c96102e', 
    message=response['payload']['message']
    number=response['payload']['number']
    


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = '127.0.0.1'
    PORT = 5038
    s.connect((HOST,PORT))
    s.send("Action: login\r\n")
    s.send("Username: username\r\n")
    s.send("Secret: secret\r\n\r\n")
    s.send("Action: DongleSendSMS\r\n")
    s.send("Device: dongle0\r\n")
    s.send("Number:"+ number+"\r\n")
    s.send("Message:" +message +"\r\n\r\n")
    s.send('Action: Logoff\r\n')
    
def on_identify(*args):
    global socketId
    global outputOn
    response= args[0]
    socketId=response['socketid']
    print ('socketId is',socketId)

def on_ready(*args):
    print('we are ready')
    global socketIO
    global socketId
    global uuid
    global token
    socketIO.on('message',on_message)
    response= args[0]
    if response['status']==201:
        print('we are ready')
        while (1==1):
            socketIO.wait(1)
            print ('listening to incoming messages...',)
    
    if response['status']!=201:
        print('Sorry we are not ready')
         

        
def connect():
    
    global socketIO
    global token
    global uuid
    with SocketIO('http://skynet.im', 80) as socketIO:
        print ('Connecting')
        socketIO.on('identify',on_identify)
        socketIO.wait(4) #wait 4 seconds to be sure you get an identify back
        
        socketIO.emit('identity',{'uuid':uuid,'token':token,'socketid':socketId})
        
        socketIO.on('ready',on_ready)
        socketIO.wait(4) #wait 4 seconds to be sure you get an identify back
        
         



connect()


