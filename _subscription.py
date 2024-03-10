import logging
logging.basicConfig(\
    format='%(asctime)s - %(message)s',\
    datefmt='%d-%b-%y %H:%M:%S',\
    level=logging.DEBUG
    )

def createSubscription(arangoClient, subscriptionName, price):
    try:
        import uuid
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        logging.info("Insert documents in to subscription collection")
        subscriptionDict = {
            '_key': subscriptionName, #str(uuid.uuid4()),
            'subscriptionName': subscriptionName,
            'price': price
        }
        db.collection('subscription').insert(subscriptionDict)

    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))

def fetchSubscription(arangoClient,subscriptionName):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN subscription RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN subscription RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN subscription FILTER doc.subscriptionName == @subscriptionName RETURN doc',
        bind_vars={'subscriptionName': subscriptionName}
        )
        # Iterate through the result cursor
        subscription_keys = [doc['_key'] for doc in cursor]
        #logging.info("Response from Query : {}".format(subscription_keys))
        return {"status": "success", "message": "Subscription fetched successfully", "data": subscription_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching subscription"}

def fetchAll(arangoClient):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN subscription RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN subscription RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN subscription RETURN doc'
        )
        # Iterate through the result cursor
        subscription_keys = [doc['_key'] for doc in cursor]
        #logging.info("Response from Query : {}".format(subscription_keys))
        return {"status": "success", "message": "Subscriptions fetched successfully", "data": subscription_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching subscriptions"}