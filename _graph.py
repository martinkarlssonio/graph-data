import logging
logging.basicConfig(\
    format='%(asctime)s - %(message)s',\
    datefmt='%d-%b-%y %H:%M:%S',\
    level=logging.DEBUG
    )

def fetchGraph(arangoClient,collection,vertexId,followType="OUTBOUND"):
    mockedData = {
        "graph" : {
        "nodes" : [], 
        "edges" : [],
        "combos" : [] 
        }
        }
    graph = mockedData
    try:
        logging.info("models.fetchGraph - nodeType/nodeId : {}/{}".format(collection,vertexId))
        ##QUERY ARANGODB
        # Execute the query
        db = arangoClient.db('main')
        queryString = f"FOR v, e, p IN 1..5 {followType} '{collection}/{vertexId}' GRAPH 'main' RETURN" + " { " + "verticesIds: p.vertices[*]._id, edges: p.edges[*].label}"
        cursor = db.aql.execute(queryString)
        # Iterate through the result cursor
        graph = [doc for doc in cursor]
        return graph
    except Exception as e:
        logging.info(e, exc_info=True)
        return {}