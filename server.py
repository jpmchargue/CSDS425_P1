import socket
import threading

PORT = 50000
nextPort = PORT + 1

# Set up a welcome socket.
connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection.bind(('', PORT))
connection.listen(1)
print("The server is ready!")

# The main map used to store keys and values
map = {}

# Take a command string, perform the appropriate actions, and return the appropriate message.
def parse(command):
    args = [s for s in command.split(' ') if len(s) > 0]
    if len(args) > 0:
        if args[0] == "get":
            if len(args) < 2:
                return "Invalid usage of get: must provide key"
            key = ' '.join(args[1:])
            if key not in map:
                return f"Cannot find {key} in data store"
            else:
                return map[key]

        elif args[0] == "put":
            if len(args) < 3:
                return "Invalid usage of put: must provide key and value"
            if not args[-1].isnumeric():
                return f"Value {args[-1]} is not valid"
            key = ' '.join(args[1:-1])
            map[key] = args[-1]
            return "Success"

        elif args[0] == "mappings":
            if len(map.keys()) == 0:
                return "no mappings assigned"
            acc = ""
            for key in map:
                acc += key + ' ' + map[key] + '\n'
            return acc[:-1]

        elif args[0] == "keyset":
            if len(map.keys()) == 0:
                return "no keys assigned"
            acc = ""
            for key in map:
                acc += key + '\n'
            return acc[:-1]

        elif args[0] == "values":
            if len(map.keys()) == 0:
                return "no values assigned"
            acc = ""
            for key in map:
                acc += map[key] + '\n'
            return acc[:-1]

# Manage a connection through a new client-specific socket.
def runService(local, port):
    client, addr = local.accept()
    while True:
        try:
            data = client.recv(1024) # Receive data
            if data:
                command = data.decode()
                if command == "bye":
                    print(f"Closing connection on port {port}")
                    return
                response = parse(command)
                client.send(response.encode())
        except ConnectionResetError:
            print(f"Connection lost with client on port {port}...")
            return

while True:
    # Constantly listen for connecting clients
    client, addr = connection.accept()
    print(f"Received connection from {addr}, assigning to port {nextPort}")
    if addr:
        # We've received a connection!
        # Create a new listen socket for it, then send the port of that socket
        # back to the client.
        local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        local.bind(('', nextPort))
        local.listen(1)
        client.send(str(nextPort).encode())

        # Spawn a new thread to manage this connection.
        threading.Thread(target=runService, args=(local, nextPort)).start()
        nextPort += 1
