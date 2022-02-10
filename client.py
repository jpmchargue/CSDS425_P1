import os
import socket
import sys

# Check if a given hostname/IP is value by pinging it.
def isValidIP(str):
    check = os.system(f'ping -c 1 {str} > /dev/null')
    return True if check == 0 else False

# Print welcome messages,
# then request an IP or hostname until a valid one is entered.
print("Welcome to the KeyValue Service client!")
ip = ""
while True:
    ip = input("Please enter the IP or hostname of the server: ")
    if isValidIP(ip):
        break
    print(f"'{ip}' is not a valid IP or hostname")
print(f"Connecting to {ip}...")

PORT = 50000

# Open a TCP connection
hello = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hello.connect((ip, PORT))

# The server will assign the client a new dedicated port;
# save this port number and switch to a new connection through it
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

# Send a command to the server and return the response.
def send(string):
    data = string
    connection.send(data.encode())
    response = connection.recv(1024)
    return response.decode()

# Pre-filtering of commands:
# don't send commands to the server that are obviously invalid
# or don't need to check with the server, like 'help'.
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

# Keep prompting the user for commands, then processing them
# until the process is closed.
while True:
    command = input("KeyValue Service> ")
    process(command)
