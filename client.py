import socket
import sys

print("Welcome to the KeyValue Service client!")
ip = input("Please enter the IP or hostname of the server: ")
PORT = 50000

# Open a TCP connection
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((ip, PORT))

valid_commands = [
    'get',
    'put',
    'mappings',
    'keyset',
    'values'
]

def send(string):
    data = string
    connection.send(data.encode())
    response = connection.recv(1024)
    return response.decode()

def process(command):
    args = command.split(' ')
    if len(args) > 0:
        if args[0] in valid_commands:
            print(send(command))
        else:
            print(f"Invalid command '{command}'")



while True:
    command = input("KeyValue Service> ")
    process(command)
