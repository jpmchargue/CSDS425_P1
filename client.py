import os
import socket
import sys

def isValidIP2(str):
    check = os.system(f'ping -c 1 {str} > /dev/null')
    return True if check == 0 else False

def isValidIP(str):
    if len(str) == 0:
        return False
    numbers = str.split('.')
    if len(numbers) != 4:
        return False
    for i in numbers:
        if len(i) > 3 or not i.isnumeric():
            return False
    return True

print("Welcome to the KeyValue Service client!")

ip = ""
while True:
    ip = input("Please enter the IP or hostname of the server: ")
    if isValidIP2(ip):
        break
    print(f"'{ip}' is not a valid IP or hostname")
print(f"Connecting to {ip}...")

PORT = 50000

# Open a TCP connection
hello = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hello.connect((ip, PORT))
assignedPort = int(hello.recv(1024).decode())
hello.close()

print(f"Assigned to Port {assignedPort}...")
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((ip, assignedPort))

print("Connected!")

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
        if args[0] == "help":
            print("help \n \
                get key \
                put key value \
                values \
                keyset \
                mappings \
                bye")
        elif args[0] == "bye":
            send(command)
            quit()
        elif args[0] in valid_commands:
            print(send(command))
        else:
            print(f"Invalid command '{command}'")

while True:
    command = input("KeyValue Service> ")
    process(command)
