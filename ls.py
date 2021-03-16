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

import os
import socket
import threading
import time
import sys



TOP_LEVEL_SERVER = "TopLevelServer"
MAX_REQUEST_SIZE = 200
RS_BIND_ADDRESS = ''


def processDNSQuery(queriedHostname):
    r"""
       @TODO : Update to carry out the tasks required for project 2

       Requirements: 
        Needs to be able to connect to two top level servers simultaneously. When processing a single hostname
        will have to give each of those top level servers 5 secs to respond, when no response received for the 5
        seconds the connection has to be closed. If a response is received then it needs to be returned to the 
        client.

       Ideas:
        - Threads which are closed after 5 seconds. Can do a sleep function after calling the thread and then immediately
        check for results and if none then close.
            - Will need to figure out how to check if there are results or not after the 5 seconds are up.
                - Can do interrupt if a result is returned. Will need to look up interrupts for python.
    """
    pass



def server(rsPort):
    r"""
        Method to set up server and keep it running. Based on project zero code.

        ---------------------

        @param:
            rsPort : int - the port to bind the root server ; obtained originally from the command line
        
        ---------------------

        Will receive requests from the client and check the dns dictionary 
        (which will be set up at the start of this method) to see if the hostname
        exists. If it does then its corresponding details will be returned, if not then
        the top level server details will be returned.

        ----------------------

        ...
    """
    
    # set the host address or port based on project requirements here
    hostAddress = RS_BIND_ADDRESS
    hostPort = rsPort


    #create the server socket and initiate it:
    try:
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except:
        exit()
    
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
            toBeSentBackToClient = processDNSQuery(clientDataReceived)

            #   return the results to the client:
            clientSocketId.send(toBeSentBackToClient.encode('utf-8'))
        except:
            break
    

    serverSocket.close()
    exit()



if __name__ == "__main__":

    #get the port from command line arg:
    rsPort = int(sys.argv[1])

    serverThread = threading.Thread(name='serverThread',target=server,args=[rsPort])
    serverThread.start()
    print("Server Thread Started")