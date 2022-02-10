CSDS 425 PROJECT 1
James McHargue
jpm221

** HOW TO RUN **
To start the server, run the command 'python3 server.py' in the terminal.
To start a client, run the command 'python3 client.py'.
BE SURE TO USE PYTHON3, NOT JUST PYTHON. I make heavy use of Python3-exclusive formatting.


** IMPLEMENTATION **
The core functionality of the KeyValue Service can be achieved using a simple Python dictionary,
as it already can map arbitrary strings to arbitrary values. In this program, the main
dictionary that stores the keys and values is simply called 'map'.

The server script has three main features:
- parse(str), which analyzes a command string and returns the appropriate message
- runService(), which handles a connection with an individual client
- a 'while' loop that manages incoming connections
The 'while' loop constantly checks port 50000 for incoming connections from clients.
When it receives one, it first chooses an unused port (by counting up from 50001)
and sends that port number back to the client.
Using that port, it then creates a new listener socket for that connection,
spawns a new thread, and tells the thread to run 'runService()' using the new socket.
runService() then simply passes any incoming messages to 'parse()'
and sends the returned value back to the client.

The client script is straightforward: it spawns a connection with the server welcome socket,
checks the port number the server sends back, and then opens a new connection to the
server through the new port number.
It then repeatedly prompts the user for a command-- whenever the user enters one,
it verifies the validity of the command, sends it to the server,
and displays the message the server sends back.


** TESTING **
I tested this code by running both scripts on a new Ubuntu 20.04 VM in VM VirtualBox.
All commands were tested; removal of excess spaces from keys was tested;
support for multiple clients was tested.
