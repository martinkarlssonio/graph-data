import logging
logging.basicConfig(\
    format='%(asctime)s - %(message)s',\
    datefmt='%d-%b-%y %H:%M:%S',\
    level=logging.DEBUG
    )

def startArangoContainer():
    import docker
    containerImage = 'arangodb:3.11.8'
    dockerClient = docker.from_env()
    ## Check if container is already rnning
    containerRunning = False
    containers = dockerClient.containers.list(all=False)
    for container in containers:
        if str(container.attrs['Config']['Image']) == containerImage:
            if "true" in str(container.attrs['State']['Running']).lower():
                print("Container is running")
                containerRunning = True
    ## Start container if not running
    if not containerRunning:
        print("Starting container...")
        env_vars = {"ARANGO_NO_AUTH": 1}  # No auth for this example, should be changed in production
        container = dockerClient.containers.run(containerImage, detach=True, environment=env_vars, ports={'8529/tcp': ('127.0.0.1',8529)})
        print(container)

def setupArango(arangoClient):
    import os
    import _initData
    try:
        # Connect to "_system" database as root user.
        # This returns an API wrapper for "_system" database.
        try:
            username = os.environ['ARANGO_ROOT_USER']
            password = os.environ['ARANGO_ROOT_PASSWORD']
        except:
            username = 'test'
            password = 'test'

        ## Connect to _system andn then create a new database named "main" if it does not already exist.
        sys_db = arangoClient.db('_system')
        if not sys_db.has_database('main'):
            sys_db.create_database(
                name='main',
                users=[
                    {'username': username, 'password': password, 'active': True},
                ],
            )
        db = arangoClient.db('main', username=username, password=password)

        ## Create graph
        graphs = ['main']
        for graph in graphs:
            if db.has_graph('main'):
                pass
            else:
                db.create_graph('main')
        main = db.graph('main')

        ## Create set of Collections
        collections, edges = _initData.fetchInitData()

        for collection in collections:
            if main.has_vertex_collection(collection):
                pass
            else:
                main.create_vertex_collection(collection)

        ## Create set of Edges (relationship types between collections)
        edges = [
            {"edgeName":"HAS_SUBSCRIPTION","fromCollection":["customer"],"toCollection":["subscription"]},
            {"edgeName":"OF_TYPE","fromCollection":["machine"],"toCollection":["machineType"]},
            {"edgeName":"RUNS_SOFTWARE","fromCollection":["machine"],"toCollection":["software"]},
            {"edgeName":"EMPLOYED_AT","fromCollection":["user"],"toCollection":["customer"]},
            {"edgeName":"IN_REGION","fromCollection":["customer"],"toCollection":["region"]},
            {"edgeName":"OPERATES_IN","fromCollection":["machine"],"toCollection":["region"]},
            {"edgeName":"HAS_ROLE","fromCollection":["user"],"toCollection":["userRole"]}
            ]
        
        for edge in edges:
            edgeName = edge['edgeName']
            fromCollection = edge['fromCollection']
            toCollection = edge['toCollection']
            if main.has_edge_definition(edge):
                pass
            else:
                graphFromEdge = main.create_edge_definition(
                    edge_collection=edgeName,
                    from_vertex_collections=fromCollection,
                    to_vertex_collections=toCollection
                )
        return {"status": "success", "message": "ArangoDB initialized successfully"}
    except Exception as e:
        logging.info(e, exc_info=True)
        return {"status": "error", "message": "Error initializing ArangoDB"}

