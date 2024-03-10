import logging
logging.basicConfig(\
    format='%(asctime)s - %(message)s',\
    datefmt='%d-%b-%y %H:%M:%S',\
    level=logging.DEBUG
    )

def createRegion(arangoClient, regionName):
    try:
        import uuid
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        logging.info("Insert documents in to region collection")
        # Insert some test documents into "students" collection.
        regionDict = {
            '_key': regionName,
            'regionName': regionName
        }
        db.collection('region').insert(regionDict)

    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))

def fetchRegions(arangoClient,regionName):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN region RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN region RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN region FILTER doc.regionName == @regionName RETURN doc',
        bind_vars={'regionName': regionName}
        )
        # Iterate through the result cursor
        region_keys = [doc['_key'] for doc in cursor]
        #logging.info("Response from Query : {}".format(region_keys))
        return {"status": "success", "message": "Regions fetched successfully", "data": region_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching regions"}

def fetchAll(arangoClient):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN region RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN region RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN region RETURN doc'
        )
        # Iterate through the result cursor
        region_keys = [doc['_key'] for doc in cursor]
        #logging.info("Response from Query : {}".format(region_keys))
        return {"status": "success", "message": "Regions fetched successfully", "data": region_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching regions"}