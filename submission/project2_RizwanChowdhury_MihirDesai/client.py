"""
    Client code. Will read the input file and send each hostname as request to the root &/or top level servers.
    
    ------------------------

    Organized with the following methods:
        - readInputFile
        - setupClientSocket
        - sendRequest
        - clientFunctionalities
"""



#imports
import socket
import sys
import os

# constants (will use constants to define the address and port for rs and ts until clarification is obtained); these will be changed
RS_HOSTADDRESS_LOCAL = socket.gethostbyname(socket.gethostname())
HOST_QUERY_FILE = './PROJ2-HNS.txt'
NS_FLAG = "NS"
TS_RESPONSE_MARKER = 'NS'
OUTPUT_FILE_PATH = './RESOLVED.txt' #this needs to be changed to just RESOLVED.txt
BUFFER_SIZE = 200
RESULT_STRING_DELIMITER = '\n'


def readInputFile(filePath=HOST_QUERY_FILE):
    r"""
        Read the input file line by line. Lines will be stored in a list and returned.

        -----------------
        
        @param
            filePath : path to the input file; the name given will be used

        ----------------

        @return : list - list of addresses to be requested from rs and ts
    """
    
    with open(filePath,'r') as inputfile:
        hostNameList = inputfile.readlines()
    
    return hostNameList



def sendRequest(hostName,clientSocket):
    r"""
        Sends a request to either the root server or the top level server based on the destination parameter.

        ---------------

        @param
            hostName : str - the hostname being requested of the servers
            destination : tuple - the (address,port) of the server that is being sent the request
        
        --------------

        @returns : str - the response from the server
                   None - if the hostname is blank
    """

    #print('hostnamesent:',hostName.encode('utf-8'))

    #send server the hostname:
    if hostName != '':
        clientSocket.send(hostName.encode('utf-8'))
    else :
        return None

    #wait for response from server:
    dataFromServer = clientSocket.recv(BUFFER_SIZE).decode('utf-8')

    return dataFromServer


def clientFunctionalities(rsHostName,rsPort):
    r"""
        First gets list of inputs (by calling readInputFile()). Then opens connection to root and if necessary top level
        server to request the addresses corresponding to hostnames from input files. Requests are made for each input.
        Finally writes to the output file the responses from the requests.
    """

    # get host address from provided hostname
    #rsHostName = '' if rsHostName == 'localhost' else rsHostName
    rsHostAddress = socket.gethostbyname(rsHostName)
    
    #setup the client socket:
    clientSocket_rs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #   set destination details and create socket connections:
    rs_destination = (rsHostAddress,rsPort)
    clientSocket_rs.connect(rs_destination)
    
    hostNames = readInputFile() # get inputs
    aggResString = ''

    # make requests for each hostName in the inputfile
    for hostName in hostNames:
        #make request to the root server:
        hostName = hostName.lower().strip('\n')
        hostName = hostName.strip()
        rsResponse = sendRequest(hostName,clientSocket_rs)

        if rsResponse is None:
            continue
        else:
            rsResponse = rsResponse.strip()

        resultString = hostName + ' ' + rsResponse
        aggResString += resultString + RESULT_STRING_DELIMITER
            
    
    
    clientSocket_rs.close()
    
    #write output to the RESOLVED.TXT
    with open(OUTPUT_FILE_PATH,'a') as outputFile:
        outputFile.write(aggResString)
        
    


if __name__ == "__main__":
    # parse the command line arguments; the positions of the args are based on instructions:
    listOfArguments = sys.argv
    rsHostAddress = str(listOfArguments[1])
    rsPort = int(listOfArguments[2])

    rsHostAddress = socket.gethostbyname(socket.gethostname()) if rsHostAddress == 'localhost' else rsHostAddress

    clientFunctionalities(rsHostAddress,rsPort)