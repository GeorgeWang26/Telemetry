#!/usr/bin/python3

import socket
import hatControl

def socketInit():
    ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip.connect(("8.8.8.8", 80)) #Connects to itself to find it's IP
    host = ip.getsockname()[0]  #Gets it's own IP (for display)
    port = 8080                #The port that will be used for the socket

    print("Server IP: %s"%(host))
    print("Server PORT: %d"%(port))

    s = socket.socket()  # Create a socket
    s.bind(('0.0.0.0', port))  # Bind the socket object to that socket as the server

    s.listen(1)  # Waits for 1 connection
    c, addr = s.accept()  # Accept the connection and mark down it's IP (addr)
    print("Connection from: " + str(addr))

    return c


def read_values(connection):
    # send the message back to client a after all data is executed
    data = connection.recv(30).decode('utf-8')
    splitData = data.split(" ")
    print(splitData)
    return splitData


def run():
#    print('start')
#    stay = socket.socket()
#    stay.bind(('0.0.0.0', 8000))
#    stay.listen()
#    print('finish')

    preX = 0 
    preY = 0
    connection = socketInit()
    
    while True:
        values = read_values(connection)
        if values is not None:
            x_angle = float(values[0])
            y_angle = float(values[1])
            if abs(preX - x_angle) > 3.6:
                preX = x_angle
                hatControl.xChange(x_angle)
            if abs(preY - y_angle) > 3.6:
                preY = y_angle
                hatControl.yChange(y_angle)
            # send message back to client to recieve the new data
            MessageToClient = "t"
            connection.send(MessageToClient.encode('utf-8'))


if __name__ == "__main__":
    try: 
        run()
    except Exception as e:
        # socket will be closed when python ends 
        print(e)
        print("end")
