import logging
logging.basicConfig(\
    format='%(asctime)s - %(message)s',\
    datefmt='%d-%b-%y %H:%M:%S',\
    level=logging.DEBUG
    )

def createMachineType(arangoClient, machineType,machineTypeDescription):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        logging.info("Insert documents in to machineType collection")
        # Insert some test documents into "students" collection.
        machineTypeDict = {
            '_key': machineType,
            'machineType': machineType,
            'machineTypeDescription': machineTypeDescription
        }
        db.collection('machineType').insert(machineTypeDict)

    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))

def fetchMachineType(arangoClient,machineType):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN machineType RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN machineType RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN machineType FILTER doc.machineType == @machineType RETURN doc',
        bind_vars={'machineType': machineType}
        )
        # Iterate through the result cursor
        machineType_keys = [doc['_key'] for doc in cursor]
        #logging.info("Response from Query : {}".format(machineType_keys))
        return {"status": "success", "message": "MachineType fetched successfully", "data": machineType_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching machineType"}

def fetchAll(arangoClient):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN machineType RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN machineType RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN machineType RETURN doc'
        )
        # Iterate through the result cursor
        machineType_keys = [doc['_key'] for doc in cursor]
        #logging.info("Response from Query : {}".format(machineType_keys))
        return {"status": "success", "message": "MachineTypes fetched successfully", "data": machineType_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching machineTypes"}