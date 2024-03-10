from arango import ArangoClient, AQLQueryKillError
import initArango, createMockedData
import time
import _graph, _machine

import logging
logging.basicConfig(\
    format='%(asctime)s - %(message)s',\
    datefmt='%d-%b-%y %H:%M:%S',\
    level=logging.DEBUG
    )
        
def hashPassword(passwordString):
    import hashlib
    passwordHashed = hashlib.md5(passwordString.encode('utf-8')).hexdigest()
    return passwordHashed

if __name__ == "__main__":
    initArango.startArangoContainer()
    ## Initialize the ArangoDB client.
    arangoClient = ArangoClient(hosts="http://127.0.0.1:8529")
    initArango.setupArango(arangoClient)
    time.sleep(1)
    ## Populate witih mocked data
    ## Ask if user want to popluate with mocked data
    userInput = input("Would you like to populate database with mocked data? (y/n) ")
    if userInput == "y":
        print("Populating database with mocked data")
        createMockedData.populateDatabase(arangoClient)
        time.sleep(1)
        createMockedData.mockedEdges(arangoClient)
        print("Database populated with mocked data!")
    else:
        print("Database will not be populated with mocked data")
    ## Fetch graph starting traversal from a specific vertexId for a machine
    print("Fetching a random machine and traversing graph...")
    machines = _machine.fetchAll(arangoClient)
    machineId = machines['data'][0]
    graph = _graph.fetchGraph(arangoClient,"machine",machineId,followType="OUTBOUND")
    print("Graph:")
    print(graph)