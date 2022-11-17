import socket
import sys
import signal
import random
import json
import pickle
import struct
import array

###################################
def printArray(myArray):
    for row in myArray:
        print(row)

def initStructLike():
    rows, cols = (3, 3) #define size of myArray
    arr = [[0 for i in range(cols)] for j in range(rows)]
    msg = ""
    rowNum = 0
    colNum = 0
    myStruct = {'msg': msg, 'myArray': arr, 'rowInput': rowNum, 'columnInput': colNum}
    return myStruct

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        print("[CONTRL-C]: Server is terminating")
        sock.close()
        exit(1)

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

signal.signal(signal.SIGINT, handler)  #this gently takes care of ctl-c

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('', 10000)
sock.bind(server_address)
sock.listen(1)
random.seed(None, 2)
print('[INFO]: Server Started, waiting for a connection')
###################################

while True:
    connection, client_address = sock.accept()
    my_item = initStructLike()
    print ('[INFO]: client connected:', client_address)
    while True:
        #Choice made by the server(Random)
        oddNumbers = [1,3,5,7,9]
        choice = random.randint(0,len(oddNumbers))
        mysteryNumber = oddNumbers[choice]
        oddNumbers.remove(mysteryNumber)

        print("data to send to client")
        r = random.randint(0, 2)
        c = random.randint(0, 2)
        my_item['myArray'][r][c] = mysteryNumber
        printArray(my_item['myArray'])

        data = receive_data(connection)
        if data:
            if "quit" == data['msg']:
                print("[INFO]: client is leaving, time to wait for another connection")
                break
            print("data received from client")
            print(data['msg'])
            clientRow = data['rowInput']
            clientColumn = data['columnInput']     #Shows our change to the board
            my_item['myArray'][clientRow][clientColumn] = data['msg']
            printArray(data['myArray'])

            # These are the win conditions #
            # if my_item[0][0] + my_item[0][1] + my_item[0][2] == 15:
            # elif my_item[1][0] + my_item[1][1] + my_item[1][2] == 15:
            # elif my_item[2][0] + my_item[2][1] + my_item[2][2] == 15:
            # elif my_item[0][0] + my_item[0][1] + my_item[0][2] == 15:
            # elif my_item[1][0] + my_item[1][1] + my_item[1][2] == 15:
            # elif my_item[2][0] + my_item[2][1] + my_item[2][2] == 15:
            # elif my_item[0][0] + my_item[1][1] + my_item[2][2] == 15:
            # elif my_item[2][0] + my_item[1][1] + my_item[0][2] == 15:

            # update values
            # print("data to send to client")
            # my_item['msg'] = data['msg'].upper()
            # r = random.randint(0, 2)
            # c = random.randint(0, 2)
            # my_item['myArray'][r][c] = mysteryNumber

            printArray(my_item['myArray'])
            send_data(connection, my_item) #send 2d array and message in all caps
            print("[INFO]: done sending")
        else:
            print("[ERROR]: there was an error")
            break
    connection.close()

# make server go first
# get rid of used evens number on client sude
# make sure that server does not override space on board