# Centralized-P2P-Systems-Performance-Analysis-using-Wireshak-and-Benchmarking
### About
This is a Python implementation of a simple peer-to-peer file sharing system. The system consists of a server and multiple clients, where clients can connect to the server and register their available files. Other clients can then search for files on the server and download them directly from the clients that have them. The system is implemented using sockets, threading, and a simple protocol for communicating between the server and clients.

### Technologies/Libraries Used

##### The server, peer client and benchmark code will use following libraries:
1. **socket**: for networking operations.
2. **threading**: for implementing multi-threading in the server.
3. **os**: for platform-independent operations like handling system processes.
4. **sys**: for accessing some system-specific parameters and functions.
5. **collections.defaultdict**: for creating a dictionary with default value for non-existing keys.
6. **pathlib.Path:** for performing operations on file paths.
7. **mimetypes**: for mapping file extensions to MIME types.
8. **time**: provides various time-related functions.
9. **hashlib**: provides hashing algorithms for creating message digests.
#####  Software
1. Wireshark - For evaluation and measurement

### Files

 1. Server.py : This has all the functionalities for the server to act as the central indexing node
 2. Client.py: You can create multiples copies of this and put it in a respective client folder
 3. benchmark.py : This is to automate client creation


###  How to reproduce?
1. For each client you create, it should be in the following directory structure: 
```markdown
├── server.py
├── benchmark.py
│   ├── Client1
│   │   ├── client.py
│   │   ├── files
|	│   │   ├── all the files that client1 has access to
│   ├── Client2
│   │   ├── client.py
│   │   ├── files
|	│   │   ├── all the files that client2 has access to
│   ├── Client3
│   │   ├── client.py
│   │   ├── files
|	│   │   ├── all the files that client3 has access to
│   ├── Client4
│   │   ├── client.py
│   │   ├── files
|	│   │   ├── all the files that client4 has access to
│   ├── Clientn
│   │   ├── client.py
│   │   ├── files
|	│   │   ├── all the files that clientn has access to
```
2. Run the server.py, it will start on port 7734 by default
3. Now you can start any of all the clients that you want to be connected to the p2p server
4. For each of the client program, you can perform the following functionalities - add, lookup, download files. You can choose that with the appropriate menu option
5. Finally a client can also be shutdown using the menu option


###  Benchmark
1. For each client you create, it should be in the following directory structure: 
```markdown
├── server.py
├── benchmark.py
│   ├── Client1
│   │   ├── client.py
│   │   ├── files
|	│   │   ├── all the files that client1 has access to
│   ├── Client2
│   │   ├── client.py
│   │   ├── files
|	│   │   ├── all the files that client2 has access to
│   ├── Client3
│   │   ├── client.py
│   │   ├── files
|	│   │   ├── all the files that client3 has access to
│   ├── Client4
│   │   ├── client.py
│   │   ├── files
|	│   │   ├── all the files that client4 has access to
│   ├── Clientn
│   │   ├── client.py
│   │   ├── files
|	│   │   ├── all the files that clientn has access to
```
2. Run the server.py, it will start on port 7734 by default
3. Now you can start any of all the clients that you want to be connected to the p2p server
4. For each of the client program, you can perform the following functionalities - add, lookup, download files. You can choose that with the appropriate menu option
5. Finally a client can also be shutdown using the menu option


###  Program Flow
1.  The client is initialized with the server host, version, and file directory.
2.  The client connects to the server using a socket connection.
3.  The client starts a separate thread for handling file uploads and listens on a specific port for incoming upload requests.
4.  The client presents a command-line interface to the user, where the user can enter commands to add, look up, list all, and download files.
5.  Upon receiving a command from the user, the client sends a request to the server over the socket connection.
6.  The server receives the request, processes it, and sends back a response to the client.
7.  The client receives the response and presents it to the user.
8.  The user can continue entering commands until they decide to shut down the client.
9.  Upon shutting down the client, the client terminates the socket connection with the server and stops listening on the upload port.

