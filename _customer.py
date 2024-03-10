import logging
logging.basicConfig(\
    format='%(asctime)s - %(message)s',\
    datefmt='%d-%b-%y %H:%M:%S',\
    level=logging.DEBUG
    )
        
def createCustomer(arangoClient, customerName, VAT, address, city, country, postalCode, contactPerson, contactEmail, contactPhone):
    try:
        import uuid
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        customerDict = {
            '_key': str(uuid.uuid4()),
            'customerName': customerName,
            'VAT': VAT,
            'address': address,
            'city': city,
            'country': country,
            'postalCode': postalCode,
            'contactPerson': contactPerson,
            'contactEmail': contactEmail,
            'contactPhone': contactPhone
        }
        db.collection('customer').insert(customerDict)

    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))

def fetchCustomers(arangoClient,customerName):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN customer RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN customer RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN customer FILTER doc.customerName == @customerName RETURN doc',
        bind_vars={'customerName': customerName}
        )
        # Iterate through the result cursor
        customer_keys = [doc['_key'] for doc in cursor]
        #logging.info("Response from Query : {}".format(customer_keys))
        return {"status": "success", "message": "Customers fetched successfully", "data": customer_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching customers"}
    
def fetchAll(arangoClient):
    try:
        logging.info("Connect to test database")
        db = arangoClient.db('main')
        # Get the AQL API wrapper.
        aql = db.aql
        logging.info("AQL explain")
        # Retrieve the execution plan without running the query.
        aql.explain('FOR doc IN customer RETURN doc')
        logging.info("AQL validate")
        # Validate the query without executing it.
        aql.validate('FOR doc IN customer RETURN doc')
        logging.info("AQL execute")
        # Execute the query
        cursor = db.aql.execute(
        'FOR doc IN customer RETURN doc'
        )
        # Iterate through the result cursor
        customer_keys = [doc['_key'] for doc in cursor]
        #logging.info("Response from Query : {}".format(customer_keys))
        return {"status": "success", "message": "Customers fetched successfully", "data": customer_keys}
    except Exception as e:
        logging.info("EXCEPTION! {}".format(e))
        return {"status": "error", "message": "Error fetching customers"}
    
