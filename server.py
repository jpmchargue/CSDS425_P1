import socket

PORT = 50000

connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection.bind(('', PORT))
connection.listen(1)
print("The server is ready!")

map = {}

def parse(command):
    args = [s for s in command.split(' ') if len(s) > 0]
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
        if not isnumeric(args[-1]):
            return f"Value {args[-1]} is not valid"
        key = ' '.join(args[1:-1])
        map[key] = args[-1]

    elif args[0] == "mappings":
        acc = ""
        for key in map:
            acc += key + ' ' + map + '\n'
        return acc

    elif args[0] == "keyset":
        acc = ""
        for key in map:
            acc += key + '\n'
        return acc

    elif args[0] == "values":
        acc = ""
        for key in map:
            acc += map[key] + '\n'
        return acc


while True:
    # Constantly listen for connecting clients
    arrivingSocket, addr = connection.accept()
    data = arrivingSocket.recv(1024)

    # Pass the client's message to parse(), then send back what parse() returns
    arrivingSocket.send(parse(data.decode()).encode())

    # Close the connection to the client
    #arrivingSocket.close()
