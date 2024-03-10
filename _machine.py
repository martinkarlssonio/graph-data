import logging
logging.basicConfig(\
    format='%(asctime)s - %(message)s',\
    datefmt='%d-%b-%y %H:%M:%S',\
    level=logging.DEBUG
    )

def createMachine(arangoClient, machineName, IP, MAC, settings):
    try:
        import uuid
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        logging.info("Insert documents in to machine collection")
        # Insert some test documents into "students" collection.
        machineDict = {
            '_key': str(uuid.uuid4()),
            'machineName': machineName,
            'IP': IP,
            'MAC': MAC,
            'settings': settings
        }
        db.collection('machine').insert(machineDict)

    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))

def fetchMachines(arangoClient,machineName):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN machine RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN machine RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN machine FILTER doc.machineType == @machineName RETURN doc',
        bind_vars={'machineName': machineName}
        )
        # Iterate through the result cursor
        machine_keys = [doc['_key'] for doc in cursor]
        logging.info("Response from Query : {}".format(machine_keys))
        return {"status": "success", "message": "Machines fetched successfully", "data": machine_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching machines"}
    
def fetchAll(arangoClient):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN machine RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN machine RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN machine RETURN doc'
        )
        # Iterate through the result cursor
        machine_keys = [doc['_key'] for doc in cursor]
        logging.info("Response from Query : {}".format(machine_keys))
        return {"status": "success", "message": "Machines fetched successfully", "data": machine_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching machines"}
    
