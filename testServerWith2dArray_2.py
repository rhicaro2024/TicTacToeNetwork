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
    gameInfo = 0
    myStruct = {'msg': msg, 'myArray': arr, 'rowInput': rowNum, 'columnInput': colNum, 'gameStatus': gameInfo}
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

firstPick = 0
oddNumbers = [1,3,5,7,9]
while True:
    connection, client_address = sock.accept()
    my_item = initStructLike()
    print ('[INFO]: client connected:', client_address)
    while True:
        while firstPick == 0:
            print("data to send to client")
            choice = random.randint(0, len(oddNumbers) - 1)
            mysteryNumber = oddNumbers[choice]
            oddNumbers.remove(mysteryNumber)
            r = random.randint(0, 2)
            c = random.randint(0, 2)
            my_item['myArray'][r][c] = mysteryNumber
            print(oddNumbers)
            printArray(my_item['myArray'])
            send_data(connection, my_item) #send 2d array and message in all caps
            print("[INFO]: done sending")
            firstPick += 1

        print("[INFO]: begin receiving")
        data = receive_data(connection)
        if data:
            if "quit" == data['msg']:
                print("[INFO]: client is leaving, time to wait for another connection")
                break
            print("data received from client")
            print(data['msg'])
            printArray(data['myArray'])
            clientRow = data['rowInput']
            clientColumn = data['columnInput']
            my_item['myArray'][clientRow][clientColumn] = data['msg']
            print(oddNumbers)
            print(my_item['myArray'])

            ###################################

            # if my_item[0][0] + my_item[0][1] + my_item[0][2] == 15:
            # elif my_item[1][0] + my_item[1][1] + my_item[1][2] == 15:
            # elif my_item[2][0] + my_item[2][1] + my_item[2][2] == 15:
            # elif my_item[0][0] + my_item[0][1] + my_item[0][2] == 15:
            # elif my_item[1][0] + my_item[1][1] + my_item[1][2] == 15:
            # elif my_item[2][0] + my_item[2][1] + my_item[2][2] == 15:
            # elif my_item[0][0] + my_item[1][1] + my_item[2][2] == 15:
            # elif my_item[2][0] + my_item[1][1] + my_item[0][2] == 15:

            # update values
            print("data to send to client")
            my_item['msg'] = data['msg'].upper()
            choice1 = random.randint(0, len(oddNumbers) - 1)
            mysteryNumber1 = oddNumbers[choice1]
            oddNumbers.remove(mysteryNumber1)
            
            while my_item['myArray'][r][c] != 0:
                r = random.randint(0, 2)
                c = random.randint(0, 2)
                if my_item['myArray'][r][c] == 0:
                    break
                
            my_item['myArray'][r][c] = mysteryNumber1
            print(oddNumbers)
            printArray(my_item['myArray'])
            send_data(connection, my_item)
            print("[INFO]: done sending")

            if (int(my_item['myArray'][0][0]) + int(my_item['myArray'][0][1]) + int(my_item['myArray'][0][2])) == 15 or \
            (int(my_item['myArray'][1][0]) + int(my_item['myArray'][1][1]) + int(my_item['myArray'][1][2])) == 15 or \
            (int(my_item['myArray'][2][0]) + int(my_item['myArray'][2][1]) + int(my_item['myArray'][2][2])) == 15 or \
            (int(my_item['myArray'][0][0]) + int(my_item['myArray'][1][0]) + int(my_item['myArray'][2][0])) == 15 or \
            (int(my_item['myArray'][0][1]) + int(my_item['myArray'][1][1]) + int(my_item['myArray'][2][1])) == 15 or \
            (int(my_item['myArray'][0][2]) + int(my_item['myArray'][1][2]) + int(my_item['myArray'][2][2])) == 15 or \
            (int(my_item['myArray'][0][0]) + int(my_item['myArray'][1][1]) + int(my_item['myArray'][2][2])) == 15 or \
            (int(my_item['myArray'][2][0]) + int(my_item['myArray'][1][1]) + int(my_item['myArray'][0][2])) == 15:

                print(int(my_item['myArray'][0][0]) + int(my_item['myArray'][0][1]) + int(my_item['myArray'][0][2]))
                print(int(my_item['myArray'][1][0]) + int(my_item['myArray'][1][1]) + int(my_item['myArray'][1][2]))
                print(int(my_item['myArray'][2][0]) + int(my_item['myArray'][2][1]) + int(my_item['myArray'][2][2]))
                print(int(my_item['myArray'][0][0]) + int(my_item['myArray'][1][0]) + int(my_item['myArray'][2][0]))
                print(int(my_item['myArray'][0][1]) + int(my_item['myArray'][1][1]) + int(my_item['myArray'][2][1]))
                print(int(my_item['myArray'][0][2]) + int(my_item['myArray'][1][2]) + int(my_item['myArray'][2][2]))
                print(int(my_item['myArray'][0][0]) + int(my_item['myArray'][1][1]) + int(my_item['myArray'][2][2]))
                print(int(my_item['myArray'][2][0]) + int(my_item['myArray'][1][1]) + int(my_item['myArray'][0][2]))

                my_item['gameStatus'] = 2
                send_data(connection, my_item['gameStatus'])
                connection.close()
            else:
                my_item['gameStatus'] = 0

            if len(oddNumbers) == 0:
                my_item['gameStatus'] = 1
                print(my_item['gameStatus'])
                send_data(connection, my_item['gameStatus'])
                print("[INFO]: connection closed")
                connection.close()
        else:
            print("[ERROR]: there was an error")
            break
    connection.close()