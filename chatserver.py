from twisted.protocols import basic
from twisted.web.websockets import WebSocketsResource, WebSocketsProtocol, lookupProtocolForFactory

import time, datetime, json, thread
from twisted.web.resource import Resource
from twisted.internet import task
from twisted.web.server import NOT_DONE_YET
import HTMLParser
import json
from sets import Set
write_lock = thread.allocate_lock() #forcing synchronized writes between the various kinds of clients

class WebsocketChat(basic.LineReceiver):

    def connectionMade(self):
        print "Got new client!"
        self.factory.num_connections+=1
        #WebsocketChat.dataReceived(self,'Asif: welcome')
	self.transport.write('connected ....\n')
	self.factory.clients.append(self)
    #print str(self.factory.clients)
    def connectionLost(self, reason):
        print "socket connection lost, Reason",reason
        self.factory.num_connections-=1
        for key,value in self.factory.client_name.items():
            if value==self:
                del self.factory.client_name[key]
	self.factory.clients.remove(self)
    

    def dataReceived(self, data):
        msg_list=[]
        f=''
        data=str(HTMLParser.HTMLParser().unescape(data))
        print "data_recieved"+data
        split=data.split(':')
        self.factory.sender=split[0]
        if(split[0]=='list'):
            if 'admin' not in self.factory.client_name.keys():
                self.factory.client_name.update({'admin':self.factory.clients[len(self.factory.clients)-1]})
            self.factory.list=json.loads(split[1])
            print self.factory.list
        elif(split[1]=='enable' and split[0]=='admin' ):
            self.factory.enable=True
            #question_id = request.POST.get('question_id')
            self.factory.question_id=split[2]
            if(self.factory.question_id):
                print "question_id",self.factory.question_id
                #file_path=('static_in_env/media_root/uploads/chats/'str(%s.txt')%(self.factory.question_id)
                #print file_path
                self.factory.file_desc=open('static_in_env/media_root/uploads/chats/'+str(self.factory.question_id)+'.txt','w')
            print "enable chat"
        elif(split[1]=='disable' and split[0]=='admin'):
            self.factory.enable=False
            print 'disable chat'
            if(self.factory.file_desc):
                self.factory.file_desc.close()
        else:
            print "number_of_connections",self.factory.num_connections
            if self.factory.sender not in self.factory.client_name.keys():
                self.factory.client_name.update({str(self.factory.sender):self.factory.clients[len(self.factory.clients)-1]})

        print self.factory.client_name
        write_lock.acquire()
        self.factory.messages[float(time.time())] = data
        write_lock.release()
        if(self.factory.enable):
            if(self.factory.file_desc):
                print "writing "+data+ "to file"
                self.factory.file_desc.write(data+"\n")
            if self.factory.sender=='admin':
                print 'admin_sender'
                msg_list=Set([])
                for list in self.factory.list:
                    for items in list:
                        msg_list.add(items)
                print "broadcast message",msg_list
                self.updateClients(data,msg_list)
            else:
                for list in self.factory.list:
                    if self.factory.sender in list:
                        msg_list=list
                        print list
                        break
                self.updateClients(data,msg_list)
        else:
            try:
                self.factory.client_name[self.factory.sender].message("chat not yet enable by admin")
            except KeyError:
                pass
            print "chat not enable yet"

    def updateClients(self, data,list1):
        print "updateClients"
        self.factory.client_name['admin'].message(data)
        for c in list1:
            print str(c)
            try:
                self.factory.client_name[str(c)].message(data)
                
            except KeyError:
                self.factory.client_name[self.factory.sender].message(str(c)+"  not connected yet")
                print str(c),"not connected yet."
                pass


    def message(self, message):
        self.transport.write(message + '\n')





from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import protocol
from twisted.application import service, internet

from twisted.internet.protocol import Factory
class ChatFactory(Factory):###################this one is global variables 
    protocol = WebsocketChat
    clients = []
    messages = {}
    client_name={}
    list=[]
    sender=''
    num_connections=0
    enable=False
    file_desc=''
    question_id=''
class HttpChat(Resource):
    #optimization 
    isLeaf = True
    def __init__(self):
        # throttle in seconds to check app for new data
        self.throttle = 1
        # define a list to store client requests
        self.delayed_requests = []
        self.messages = {}
 
        #instantiate a ChatFactory, for generating the websocket protocols
        self.wsFactory = ChatFactory()
 
        # setup a loop to process delayed requests
        # not strictly neccessary, but a useful optimization, 
        # since it can force dropped connections to close, etc...
        loopingCall = task.LoopingCall(self.processDelayedRequests)
        loopingCall.start(self.throttle, False)
 
        #share the list of messages between the factories of the two protocols
        write_lock.acquire()
        self.wsFactory.messages = self.messages
        write_lock.release()
        #print 'HTTPCHAT runs'
        # initialize parent
        Resource.__init__(self)
 
    def render_POST(self, request):
        request.setHeader('Content-Type', 'application/json')
        print "render_POST"
        args = request.args
        if 'new_message' in args:
            write_lock.acquire()
            self.messages[float(time.time())] = args['new_message'][0]
            write_lock.release()
            if len(self.wsFactory.clients) > 0:
                self.wsFactory.clients[0].updateClients(args['new_message'][0])
            self.processDelayedRequests()
        return ''
 
    def render_GET(self, request):
        request.setHeader('Content-Type', 'application/json')
        args = request.args
                
        if 'callback' in args:
            request.jsonpcallback =  args['callback'][0]
         
        if 'lastupdate' in args:
            request.lastupdate =  float(args['lastupdate'][0])
        else:
            request.lastupdate = 0.0
 
        if request.lastupdate < 0:             
            return self.__format_response(request, 1, "connected...", timestamp=0.0)         
 
        #get the next message for this user
        data = self.getData(request)         
        if data:             
            return self.__format_response(request, 1, data.message, timestamp=data.published_at)
 
        self.delayed_requests.append(request)         
        return NOT_DONE_YET             
 
    #returns the next sequential message, 
    #and the time it was received at
    def getData(self, request):         
        for published_at in sorted(self.messages):               
            if published_at > request.lastupdate:
                return type('obj', (object,), {'published_at' : published_at, "message": self.messages[published_at]})(); 
        return
       
    def processDelayedRequests(self):
        for request in self.delayed_requests:
            data = self.getData(request)
           
            if data:
                try:
                    request.write(self.__format_response(request, 1, data.message, data.published_at))
                    request.finish()
                except:
                    print 'connection lost before complete.'
                finally:
                    self.delayed_requests.remove(request)
 
    def __format_response(self, request, status, data, timestamp=float(time.time())):
        response = json.dumps({'status':status,'timestamp': timestamp, 'data':data})
       
        if hasattr(request, 'jsonpcallback'):
            return request.jsonpcallback+'('+response+')'
        else:
            return response

from twisted.web.resource import Resource
from twisted.web.server import Site
 
from twisted.internet import protocol
from twisted.application import service, internet
 
resource = HttpChat()
factory = Site(resource)
ws_resource = WebSocketsResource(lookupProtocolForFactory(resource.wsFactory))
root = Resource()
root.putChild("",resource) #the http protocol is up at /
root.putChild("ws",ws_resource) #the websocket protocol is at /ws
application = service.Application("chatserver")
#print 'before interface'
internet.TCPServer(9000, Site(root),interface='0.0.0.0').setServiceParent(application)
