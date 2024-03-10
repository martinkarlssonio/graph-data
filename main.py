from arango import ArangoClient, AQLQueryKillError
import initArango, createMockedData
import time

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
    createMockedData.populateDatabase(arangoClient)
    time.sleep(1)
    createMockedData.mockedEdges(arangoClient)
    print("####################################### Done")