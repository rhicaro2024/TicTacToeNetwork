import socket
import sys
import signal
import random
import json
import pickle
import struct
import array

############################################
def printArray(myArray):
    for row in myArray:
        print(row)

def initStructLike():
    rows, cols = (3, 3) #define size of myArray
    arr = [[0]*cols]*rows #init myArray to 0
    msg = ""
    rowNumber = 0
    columnNumber = 0
    myStruct = {'msg': msg, 'myArray': arr, 
    'rowInput': rowNumber, 'columnInput': columnNumber}
    return myStruct

def send_data(conn, data):
        serialized_data = pickle.dumps(data)
        conn.sendall(struct.pack('>I', len(serialized_data)))
        conn.sendall(serialized_data)

def receive_data(conn):
    data_size = struct.unpack('>I', conn.recv(4))[0]
    received_payload = b""
    reamining_payload_size = data_size
    while reamining_payload_size != 0:
        received_payload += conn.recv(reamining_payload_size)
        reamining_payload_size = data_size - len(received_payload)
    data = pickle.loads(received_payload)
    return data

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server given by the caller
server_address = (sys.argv[1], 10000)
print ("connecting to ")
print(server_address)
sock.connect(server_address)
my_item = initStructLike()
############################################

rcNum = [0,1,2]
evenNumbers = [2,4,6,8]
messageCounter = 0

while True:
    if messageCounter == 0:
        startGame = input("Begin game, type anything to begin: ")
        messageCounter = messageCounter + 1

    if messageCounter == 1:
        message = input("Type an even number from " + str(evenNumbers) + "(type quit to end): ")
        messageInt = int(message)
        while messageInt % 2 == 1:
            message = input("Type an even number from " + str(evenNumbers) + "(type quit to end):")
            messageInt = int(message)
            if messageInt % 2 == 0:
                break
        evenNumbers.remove(messageInt) #removed player choice from int

        rowPlacement = input("Enter row number (0-2): ")
        rowNum = int(rowPlacement)
        while rowNum not in rcNum:
            rowPlacement = input("Type a number between 0-2 (row): ")
            rowNum = int(rowPlacement)
            if rowNum in rcNum:
                break

        columnPlacement = input("Enter column number (0-2): ")
        colNum = int(columnPlacement)
        while colNum not in rcNum:
            columnPlacement = input("Type a number between 0-2 (column): ")
            colNum = int(columnPlacement)
            if colNum in rcNum:
                break

    #my_item = initStructLike()
    my_item['msg'] = message
    my_item['rowInput'] = rowNum
    my_item['columnInput'] = colNum

    print("data to send")
    print(my_item['msg'])
    printArray(my_item['myArray']['rowInput']['columnInput'])
    send_data(sock, my_item) #send mesaage
    if "quit" == message:
        break
    my_item=receive_data(sock) #receive array
    print("data received")
    print(my_item['msg'])
    printArray(my_item['myArray'])
sock.close()