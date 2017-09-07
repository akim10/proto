import socket
from _thread import *
from queue import Queue
import pickle
from prototyperObjects import *

HOST = ''
PORT = 6887
BACKLOG = 4

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

def handleClient(client, serverChannel, cID):
  client.setblocking(1)
  msg = ""
  while True:
    msg = pickle.loads(client.recv(16384))
    serverChannel.put(msg)

def serverThread(clientele, serverChannel):
  while True:
    msg = serverChannel.get(True, None)
    print("msg recv: ", msg, type(msg))
    if (msg):
      for cID in clientele:
        sendMsg = pickle.dumps(msg)
        clientele[cID].send(sendMsg)
    serverChannel.task_done()

clientele = {}
currID = 0

serverChannel = Queue(100)
start_new_thread(serverThread, (clientele, serverChannel))

while True:
  client, address = server.accept()
  print(currID)
  for cID in clientele:
    clientele[cID].send(bytes("newUser " + str(cID), "UTF-8"))
    client.send(bytes("newUser " + str(cID), "UTF-8"))
  clientele[currID] = client
  print("connection recieved")
  start_new_thread(handleClient, (client,serverChannel, currID))
  currID += 1

