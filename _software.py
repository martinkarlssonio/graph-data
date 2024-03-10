import logging
logging.basicConfig(\
    format='%(asctime)s - %(message)s',\
    datefmt='%d-%b-%y %H:%M:%S',\
    level=logging.DEBUG
    )
        
def createSoftware(arangoClient, softwareName, softwareVersion, settings):
    try:
        import uuid
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        logging.info("Insert documents in to software collection")
        softwareDict = {
            '_key': str(uuid.uuid4()),
            'softwareName': softwareName,
            'softwareVersion': softwareVersion,
            'softwareLocation': settings
        }
        db.collection('software').insert(softwareDict)

    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))

def fetchSoftware(arangoClient,softwareName):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN software RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN software RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN software FILTER doc.softwareName == @softwareName RETURN doc',
        bind_vars={'softwareName': softwareName}
        )
        # Iterate through the result cursor
        software_keys = [doc['_key'] for doc in cursor]
        logging.info("Response from Query : {}".format(software_keys))
        return {"status": "success", "message": "Software fetched successfully", "data": software_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching software"}

def fetchAll(arangoClient):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN software RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN software RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN software RETURN doc'
        )
        # Iterate through the result cursor
        software_keys = [doc['_key'] for doc in cursor]
        logging.info("Response from Query : {}".format(software_keys))
        return {"status": "success", "message": "Software fetched successfully", "data": software_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching software"}