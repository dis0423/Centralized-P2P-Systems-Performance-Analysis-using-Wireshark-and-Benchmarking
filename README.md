# Centralized-P2P-Systems-Performance-Analysis-using-Wireshak-and-Benchmarking
### About
This is a Python implementation of a simple peer-to-peer file sharing system. The system consists of a server and multiple clients, where clients can connect to the server and register their available files. Other clients can then search for files on the server and download them directly from the clients that have them. The system is implemented using sockets, threading, and a simple protocol for communicating between the server and clients.

### Technologies/Libraries Used

#### The server, peer client and benchmark code will use following libraries:
1. socket: for networking operations.
2. threading: for implementing multi-threading in the server.
3. os: for platform-independent operations like handling system processes.
4. sys: for accessing some system-specific parameters and functions.
5. collections.defaultdict: for creating a dictionary with default value for non-existing keys.
6. pathlib.Path: for performing operations on file paths.
7. mimetypes: for mapping file extensions to MIME types.
8. time: provides various time-related functions.
9. hashlib: provides hashing algorithms for creating message digests.
#### Software
1. Wireshark - For evaluation and measurement

### Files

 1. Server.py
 2. Client.py
 3. benchmark.py

###
