import logging
logging.basicConfig(\
    format='%(asctime)s - %(message)s',\
    datefmt='%d-%b-%y %H:%M:%S',\
    level=logging.DEBUG
    )
        
def createUser(arangoClient, firstName, lastName, email, password, settings):
    try:
        import uuid
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        logging.info("Insert documents in to user collection")
        # Insert some test documents into "students" collection.
        userDict = {
            '_key': str(uuid.uuid4()),
            'firstName': firstName,
            'lastName': lastName,
            'email': email,
            'password': password,
            'settings': settings
        }
        #db.collection('user').insert_many(userDict)
        #db.collection('user').InsertOne(userDict)
        db.collection('user').insert(userDict)

    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))

def fetchUser(arangoClient,firstName):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN user RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN user RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN user FILTER doc.firstName == @firstName RETURN doc',
        bind_vars={'firstName': firstName}
        )
        # Iterate through the result cursor
        user_keys = [doc['_key'] for doc in cursor]
        logging.info("Response from Query : {}".format(user_keys))
        return {"status": "success", "message": "Users fetched successfully", "data": user_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching users"}

def fetchAll(arangoClient):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN user RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN user RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN user RETURN doc'
        )
        # Iterate through the result cursor
        user_keys = [doc['_key'] for doc in cursor]
        logging.info("Response from Query : {}".format(user_keys))
        return {"status": "success", "message": "Users fetched successfully", "data": user_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching users"}
