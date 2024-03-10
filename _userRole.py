import logging
logging.basicConfig(\
    format='%(asctime)s - %(message)s',\
    datefmt='%d-%b-%y %H:%M:%S',\
    level=logging.DEBUG
    )

def createUserRole(arangoClient, roleName):
    try:
        import uuid
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        logging.info("Insert documents in to userRole collection")
        # Insert some test documents into "students" collection.
        userRoleDict = {
            '_key': str(uuid.uuid4()),
            'roleName': roleName
        }
        db.collection('userRole').insert(userRoleDict)

    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))

def fetchUserRole(arangoClient,roleName):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN userRole RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN userRole RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN userRole FILTER doc.roleName == @roleName RETURN doc',
        bind_vars={'roleName': roleName}
        )
        # Iterate through the result cursor
        userRole_keys = [doc['_key'] for doc in cursor]
        logging.info("Response from Query : {}".format(userRole_keys))
        return {"status": "success", "message": "UserRoles fetched successfully", "data": userRole_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching userRoles"}

def fetchAll(arangoClient):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN userRole RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN userRole RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN userRole RETURN doc'
        )
        # Iterate through the result cursor
        userRole_keys = [doc['_key'] for doc in cursor]
        logging.info("Response from Query : {}".format(userRole_keys))
        return {"status": "success", "message": "UserRoles fetched successfully", "data": userRole_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching userRoles"}