from socketIO_client import SocketIO

import logging

'''A basic script that show you 
all basic functions for Skynet.im 
and the response that is sent back    

'''
logging.basicConfig(level=logging.DEBUG)
socketId="" #the id from the socket, needed by Skynet for some operations
socketIO="" #the socket itself

def on_message(*args): 
    # this function prints out the return that Skynet sended
    response= args[0]
    print ('we receveided following message:', response)
    
def on_connecting(*args):
    # this function catches the id from the socket when we are connecting
    global socketId
    response= args[0]
    socketId=response['socketid']
    print ('we receveided following socketId:', socketId)
    


with SocketIO('http://skynet.im', 80) as socketIO:
    #device=register({"type":"test","owner":"tomdemoor"})
    print ('connecting')
        # returns {"name":"identify","args":[{"socketid":"d-1IfjXMygTGHQBy_ZYe"}]}
    socketIO.on('identify',on_connecting) # save the socketid to the variable socketId
    socketIO.wait(2) # we wait for the response to identify to the socketId we received
    
    
    socketIO.emit('identity',{'uuid':'30ebecc1-b2cb-11e3-a36b-61e66c96102e','token':'xdcsa7d5vzwa5rk9yb3ea7bix7axlxr','socketid':socketId}, on_message)
    socketIO.wait_for_callbacks(seconds=6) # let the socket listen 6 seconds for a response, if you don't do specify this it ignores the response
        # returns a ready event when successfull
    
    
    print ('Doing a whoami')
    socketIO.emit("whoami", {"uuid":'0c132b91-bcf1-11e3-a3c6-0b41aaf824e3'},on_message)
    socketIO.wait_for_callbacks(seconds=6) 
        # returns {u'protocol': u'websocket', u'secure': False, u'type': u'test', u'socketId': u'dHtgar_1Slknj1uc_ZYi', u'uuid': u'30ebecc1-b2cb-11e3-a36b-61e66c96102e', u'online': True, u'owner': u'tomdemoor', u'ipAddress': u'XXX.XXX.XXX.XXX', u'channel': u'main'
    
    socketIO.emit('register',{'type':'pythonExample'}, on_message) #register a new device 
    socketIO.wait_for_callbacks(seconds=6)
        # returns {u'uuid': u'fi132b91-bcf1-11e3-a3c6-0b41aaf824e3', u'timestamp': u'2014-04-05T18:35:22.697Z', u'token': u'aaatfb92effmvdyrpb91svusl3ngsyvi', u'online': False, u'type': u'pythonExample', u'ipAddress': u'', u'channel': u'main'})
    
    
    print ('add data to your device')
    socketIO.emit('data', {'uuid':'30ebecc1-b2cb-11e3-a36b-61e66c96102e','token':'xdcsa7d5vzwa5rk9yb3ea7bix7axlxr', "temperature": 55}, on_message);
    socketIO.wait_for_callbacks(seconds=6)
        #returns {u'uuid': u'30ebecc1-b2cb-11e3-a36b-61e66c96102e', u'eventCode': 700, u'timestamp': u'2014-04-04T20:02:16.720Z', u'api': u'data', u'_id': u'533f0fc841abbe647b0bb8d3', u'temperature': u'55'})
     
    
    print ('Doing a whoami to check if the update was successfull')
    socketIO.emit("whoami", {"uuid":'30ebecc1-b2cb-11e3-a36b-61e66c96102e'},on_message)
    socketIO.wait_for_callbacks(seconds=6)
        # returns ('we receveided following message:', {u'protocol': u'websocket', u'secure': False, u'type': u'test', u'socketId': u'94xJCQmpj4LAsc86_ZYn', u'uuid': u'30ebecc1-b2cb-11e3-a36b-61e66c96102e', u'online': True, u'owner': u'tomdemoor', u'ipAddress': u'XXX.XXX.XXX.XXX', u'channel': u'main', u'temperature': 80})
    
    print ('Search all drones that are online now')
    socketIO.emit('devices', {"type":'drone',"online":"true"},on_message)
    socketIO.wait_for_callbacks(seconds=6)
        # returns a list with all uuids {u'devices': [u'lexon', u'864e2561-af11-11e3-b10a-39009a767d0f', u'new_test1', 999, u'test1212']}) 
        # you can do a whoami to get more info on the device
    
    
    print ('Subscribe to all events and messages from/to a device')
    socketIO.emit('subscribe', {'uuid':'42cfea10-b9b8-11e3-a3c6-0b41aaf824e3','token':'0n2l94z2o5ok1emit06s53415rduc8fr'},on_message)
    socketIO.wait_for_callbacks(seconds=5)
        # returns {u'fromUuid': u'30ebecc1-b2cb-11e3-a36b-61e66c96102e', u'api': u'subscribe', u'socketid': u'QQ-JTtdxiF2zm3Od_ZYt', u'toUuid': u'30ebecc1-b2cb-11e3-a36b-61e66c96102e'})
    
    print('send a message to a device')    
    socketIO.emit('messages',{"devices": "30ebecc1-b2cb-11e3-a36b-61e66c96102e","payload": {"light":"red"}},on_message)
    socketIO.wait_for_callbacks(seconds=5)
        # returns {u'fromUuid': u'30ebecc1-b2cb-11e3-a36b-61e66c96102e', u'payload': {u'light': u'red'}, u'devices': u'30ebecc1-b2cb-11e3-a36b-61e66c96102e'}
         
    print('retrieve the 10 last events from a device')
    socketIO.emit('events', {'uuid':'42cfea10-b9b8-11e3-a3c6-0b41aaf824e3','token':'0n2l94z2o5ok1emit06s53415rduc8fr'},on_message)
    socketIO.wait_for_callbacks(seconds=5)
        # returns {u'events': [{u'eventCode': 300, u'fromUuid': u'150c7461-bda8-11e3-a3c6-0b41aaf824e3', u'devices': u'*', u'id': u'5341814241abbe647b1a3625', u'api': u'message', u'timestamp': u'2014-04-06T16:30:58.525Z', u'payload': {u'y': 4647, u'x': 1073}}, {u'eventCode': 300, u'fromUuid': u'150c7461-bda8-11e3-a3c6-0b41aaf824e3', u'devices': u'*', u'id': u'534180e941abbe647b1a3622', u'api': u'message', u'timestamp': u'2014-04-06T16:29:29.312Z', u'payload': {u'y': 4639, u'x': 1282}}, {u'eventCode': 300, u'fromUuid': u'150c7461-bda8-11e3-a3c6-0b41aaf824e3', u'devices': u'*', u'id': u'534180e941abbe647b1a3621', u'api': u'message', u'timestamp': u'2014-04-06T16:29:29.018Z', u'payload': {u'y': 4783, u'x': 1161}}, {u'eventCode': 300, u'fromUuid': u'150c7461-bda8-11e3-a3c6-0b41aaf824e3', u'devices': u'*', u'id': u'534180e041abbe647b1a3620', u'api': u'message', u'timestamp': u'2014-04-06T16:29:20.762Z', u'payload': {u'y': 6010, u'x': 1112}}, {u'eventCode': 300, u'fromUuid': u'150c7461-bda8-11e3-a3c6-0b41aaf824e3', u'devices': u'*', u'id': u'534180e041abbe647b1a361f', u'api': u'message', u'timestamp': u'2014-04-06T16:29:20.461Z', u'payload': {u'y': 5998, u'x': 1123}}, {u'eventCode': 300, u'fromUuid': u'150c7461-bda8-11e3-a3c6-0b41aaf824e3', u'devices': u'*', u'id': u'534180d041abbe647b1a361c', u'api': u'message', u'timestamp': u'2014-04-06T16:29:04.121Z', u'payload': {u'y': 5736, u'x': 1405}}, {u'eventCode': 300, u'fromUuid': u'150c7461-bda8-11e3-a3c6-0b41aaf824e3', u'devices': u'*', u'id': u'534180cf41abbe647b1a361b', u'api': u'message', u'timestamp': u'2014-04-06T16:29:03.827Z', u'payload': {u'y': 5766, u'x': 1321}}, {u'eventCode': 300, u'fromUuid': u'150c7461-bda8-11e3-a3c6-0b41aaf824e3', u'devices': u'*', u'id': u'534180cd41abbe647b1a361a', u'api': u'message', u'timestamp': u'2014-04-06T16:29:01.110Z', u'payload': {u'y': 5850, u'x': 1296}}, {u'eventCode': 300, u'fromUuid': u'150c7461-bda8-11e3-a3c6-0b41aaf824e3', u'devices': u'*', u'id': u'534180cc41abbe647b1a3619', u'api': u'message', u'timestamp': u'2014-04-06T16:29:00.803Z', u'payload': {u'y': 5827, u'x': 1230}}, {u'eventCode': 300, u'fromUuid': u'150c7461-bda8-11e3-a3c6-0b41aaf824e3', u'devices': u'*', u'id': u'534180cc41abbe647b1a3618', u'api': u'message', u'timestamp': u'2014-04-06T16:29:00.511Z', u'payload': {u'y': 5880, u'x': 1172}}]})  
    
    print ('Unsubscribing...')    
    socketIO.emit('unsubscribe', {'uuid':'42cfea10-b9b8-11e3-a3c6-0b41aaf824e3','token':'0n2l94z2o5ok1emit06s53415rduc8fr'},on_message)
    socketIO.wait_for_callbacks(seconds=5)
        # returns  {u'api': u'unsubscribe', u'socketid': u'AuGuLWWzf1gnp3wG_ZYv', u'uuid': u'30ebecc1-b2cb-11e3-a36b-61e66c96102e'})
    
     
    socketIO.emit('authenticate',{'uuid':'30ebecc1-b2cb-11e3-a36b-61e66c96102e','token':'xdcsa7d5vzwa5rk9yb3ea7bix7axlxr'}, on_message)
    socketIO.wait_for_callbacks(seconds=6)
        # returns {u'authentication': True, u'uuid': u'30ebecc1-b2cb-11e3-a36b-61e66c96102e'})
        
    socketIO.emit('authenticate',{'uuid':'30ebecc1-b2cb-11e3-a36b-61e66c96102e','token':'a7d5vzwa5rk9yb3ea7bix7a'}, on_message) #wrong token 
    socketIO.wait_for_callbacks(seconds=6)
    #  returns {u'authentication': False, u'uuid': u'30ebecc1-b2cb-11e3-a36b-61e66c96102e'})
  
  
