"""
    Root server code.

    ------------------

    Will use a dictionary to store the DNS data.
        - The dictionary will be formatted in the following way:
            - key : hostname (the url)
            - value: tuple -> (ip address, A/NS)
    
    ----------------

    The rs code will be organized several methods and the main section that calls the methods. The methods are:
        - getDNSEntries
        - processDNSQuery (check if hostname exists in the server dictionary)
        - server
"""

import socket
import threading
import sys
import select



TOP_LEVEL_SERVER = "TopLevelServer"
ERROR_MESSAGE = '- Error:HOST NOT FOUND'
TIME_OUT_CONSTANT = 5 # 5 seconds before timeout
MAX_REQUEST_SIZE = 200
BUFFER_SIZE = 200
RS_BIND_ADDRESS = ''
BREAK_STATEMENT = "BreakLoop"


def setupConnections(ts1ConnData,ts2ConnData):
    r"""
        Create the sockets that will be used to send the data to the two top level servers and then
        will be waited on to get the response. The parameters here will be obtained from the command line
        arguments.
    """
    try:
        ts1_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ts2_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ts1_socket.connect(ts1ConnData)
        ts2_socket.connect(ts2ConnData)
        ts1_socket.setblocking(False)
        ts2_socket.setblocking(False)
    except:
        print('Exception:',sys.exc_info()[0])
        exit()
    
    
    return ts1_socket,ts2_socket


def processDNSQuery(queriedHostname,ts1_socket,ts2_socket):
    r"""
       Get hostname queried by client then send it to ts1 and ts2. Then wait for a response from
       either for 5 seconds. After five seconds if there is no response then return an error message.
       
       ----------------------
       @params:
        queriedHostname : str - the hostname that the client is requesting
        ts1_socket : socket - socket to connect to ts1 with
        ts2_socket : same as ts1_socket
       
       ----------------------
       @return : str - Either the ip belonging to the hostname or the error message
    """
    
    #send each of the toplevel servers the queried hostname:
    encodedQueriedHostname = queriedHostname.encode('utf-8')
    ts1_socket.send(encodedQueriedHostname)
    ts2_socket.send(encodedQueriedHostname)
    #use select statement to wait for the top level server that returns data for 5 seconds:
    read_output,_,_ = select.select([ts1_socket,ts2_socket],[],[],TIME_OUT_CONSTANT)

    # we know only one server will send a response so will read the first and only element in read_output. if read_output empty then no response and entry doesn't exist:
    if len(read_output) > 0:
        toBeReturned = read_output[0].recv(BUFFER_SIZE).decode('utf-8')
    else:
        toBeReturned = ERROR_MESSAGE
    
    
    return toBeReturned




def server(lsListenPort,ts1ConnData,ts2ConnData):
    r"""
        Method to set up server and keep it running. Based on project zero code.

        ---------------------

        @param:
            lsListenPort : port for ls server to listen on
            ts1ConnData : tuple -> (ts1hostname,ts1port)
            ts2ConnData : same as ts1ConnData
        
        ---------------------

        Will receive requests from the client and check the dns dictionary 
        (which will be set up at the start of this method) to see if the hostname
        exists. If it does then its corresponding details will be returned, if not then
        the top level server details will be returned.
    """
    
    # set the host address or port based on project requirements here
    hostAddress = RS_BIND_ADDRESS
    hostPort = lsListenPort


    #create the server socket and initiate it:
    try:
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except:
        exit()
    
    #set up the sockets and connection that will be used to contact the top level servers:
    ts1_socket,ts2_socket = setupConnections(ts1ConnData,ts2ConnData)
    
    serverBindingDetails = (hostAddress,hostPort)
    serverSocket.bind(serverBindingDetails)
    serverSocket.listen(1)

    #wait for client request and process the request:
    clientSocketId, clientAddress = serverSocket.accept()

    # loop so that multiple requests can be received:
    while(1):
        try:

            #   extract data from client socket:
            clientDataReceived_bytes = clientSocketId.recv(MAX_REQUEST_SIZE)
            clientDataReceived = clientDataReceived_bytes.decode('utf-8').strip()

            #   check if hostname is in the root dns server:
            toBeSentBackToClient = processDNSQuery(clientDataReceived,ts1_socket,ts2_socket)

            #   return the results to the client:
            clientSocketId.send(toBeSentBackToClient.encode('utf-8'))
        except:
            break
    

    # close all connections; the send statements sending the break statement should break the loop within the other servers:
    ts1_socket.send(BREAK_STATEMENT.encode('utf-8'))
    ts2_socket.send(BREAK_STATEMENT.encode('utf-8'))
    serverSocket.close()
    exit()



if __name__ == "__main__":

    #get the port from command line arg:
    lsListenPort = int(sys.argv[1])
    ts1Hostname = sys.argv[2]
    ts1ListenPort = int(sys.argv[3])
    ts2Hostname = sys.argv[4]
    ts2ListenPort = int(sys.argv[5])

    # if being tested on same machine:
    ts1Hostname = socket.gethostbyname(socket.gethostname()) if ts1Hostname == 'localhost' else ts1Hostname
    ts2Hostname = socket.gethostbyname(socket.gethostname()) if ts2Hostname == 'localhost' else ts2Hostname

    #set up connection data tuples:
    ts1ConnData = (ts1Hostname,ts1ListenPort)
    ts2ConnData = (ts2Hostname,ts2ListenPort)

    serverThread = threading.Thread(name='serverThread',target=server,args=[lsListenPort,ts1ConnData,ts2ConnData])
    serverThread.start()
    print("Server Thread Started")