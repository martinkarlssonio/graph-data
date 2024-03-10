import initArango, _user, _userRole, _customer, _software, _machine, _machineType, _region, _subscription
import random,string,os
from faker import Faker
fake = Faker()


import logging
logging.basicConfig(\
    format='%(asctime)s - %(message)s',\
    datefmt='%d-%b-%y %H:%M:%S',\
    level=logging.DEBUG
    )

def hashPassword(passwordString):
    print(passwordString)
    import hashlib
    passwordHashed = hashlib.md5(passwordString.encode('utf-8')).hexdigest()
    return passwordHashed

def populateDatabase(arangoClient):
    try:
        ## USER ROLES
        mockedUserRoleDicts = [
            {"roleName":"admin"},
            {"roleName":"user"},
            {"roleName":"viewer"}
        ]
        for userRoleDict in mockedUserRoleDicts:
            _userRole.createUserRole(arangoClient, userRoleDict["roleName"])

        ## USERS
        mockedUserDicts = []
        for n in range(0,100):
            mockedUserDicts.append(
                {"firstName":str(fake.name()).split(" ")[0],
                "lastName":str(fake.name()).split(" ")[1],
                "email":fake.company_email(),
                "password":hashPassword(fake.vin()),
                "settings":{"timezone":"utc+2","language":"english"}
                }
                )
        for user in mockedUserDicts:
            _user.createUser(arangoClient, 
                            user["firstName"], 
                            user["lastName"], 
                            user["email"], 
                            user["password"], 
                            user["settings"]
                            )
            
        ## CUSTOMERS
        mockedCustomerDicts = []
        for n in range(0,5):
            mockedCustomerDicts.append(
            {
                "customerName": fake.company(),
                "VAT": "XX123456789",
                "address": fake.street_name(),
                "city": fake.city(),
                "postalCode": "12345",
                "country": fake.country(),
                "contactPerson": "John Doe",
                "contactEmail": "john.doe@test.com",
                "contactPhone": "+46 123 456 789"
            }
            )
        for customerDict in mockedCustomerDicts:
            _customer.createCustomer(arangoClient, 
                                    customerDict["customerName"], 
                                    customerDict["VAT"], 
                                    customerDict["address"], 
                                    customerDict["city"], 
                                    customerDict["country"], 
                                    customerDict["postalCode"], 
                                    customerDict["contactPerson"], 
                                    customerDict["contactEmail"], 
                                    customerDict["contactPhone"]
                                    )

        ## MACHINE TYPES
        mockedMachineTypeDicts = [
            {
                "machineTypeName": "Driller",
                "machineTypeDescription": "Heavy driller for mining"
            },
            {
                "machineTypeName": "Large_Cutter",
                "machineTypeDescription": "Large cutter for stone blocks"
            },
            {
                "machineTypeName": "Truck_S9",
                "machineTypeDescription": "S9 trucks used for mining"
            },
            {
                "machineTypeName": "Manufacturing_Robot",
                "machineTypeDescription": "Assembly robot in production line"
            },
            {
                "machineTypeName": "Paint_Robot",
                "machineTypeDescription": "Painting robot in production line"
            }
        ]
        for machineTypeDict in mockedMachineTypeDicts:
            _machineType.createMachineType(arangoClient, 
                                    machineTypeDict["machineTypeName"], 
                                    machineTypeDict["machineTypeDescription"]
                                    )
        ## MACHINES
        mockedMachineDicts = []
        for n in range(0,100):
            mockedMachineDicts.append(
                {"machineName":str(fake.name()),
                "IP":fake.ipv4(),
                "MAC":fake.mac_address(),
                "settings":{"configuration":"config4","auto_update":random.choice(["true","false"])}
                }
                )
        for machineDict in mockedMachineDicts:
            _machine.createMachine(arangoClient, 
                                    machineDict["machineName"], 
                                    machineDict["IP"], 
                                    machineDict["MAC"], 
                                    machineDict["settings"]
                                    )
        ## REGIONS
        mockedRegionDicts = [
                {"regionName":"eu"},
                {"regionName":"emea"},
                {"regionName":"na"},
                {"regionName":"apac"},
                {"regionName":"latam"}
                ]
        for regionDict in mockedRegionDicts:
            _region.createRegion(arangoClient, regionDict["regionName"])
        
        ## SOFTWARE
        mockedSoftwareDicts = []
        for n in range(0,10):
            mockedSoftwareDicts.append(
                {"softwareName":"someSoftware",
                "softwareVersion":str(random.randint(0,9))+"."+str(random.randint(0,9))+"."+str(random.randint(0,9))+random.choice(["a","b","c","d","e","f","g","h","i","j"]),
                "softwareLocation":"s3://someBucket/someSoftware"
                }
                )
        for softwareDict in mockedSoftwareDicts:
            _software.createSoftware(arangoClient, 
                                    softwareDict["softwareName"], 
                                    softwareDict["softwareVersion"], 
                                    softwareDict["softwareLocation"]
                                    )

        ## SUBSCRIPTIONS
        mockedSubscriptionDicts = [
            {"subscriptionName":"basic","price":100},
            {"subscriptionName":"standard","price":200},
            {"subscriptionName":"premium","price":300}
        ]
        for subscriptionDict in mockedSubscriptionDicts:
            _subscription.createSubscription(arangoClient, subscriptionDict["subscriptionName"], subscriptionDict["price"])
    except Exception as e:
        logging.info(e, exc_info=True)

def mockedEdges(arangoClient):
    import  _initData
    try:
        # Connect to "_system" database as root user.
        # This returns an API wrapper for "_system" database.
        try:
            username = os.environ['ARANGO_ROOT_USER']
            password = os.environ['ARANGO_ROOT_PASSWORD']
        except:
            username = 'test'
            password = 'test'
        
        db = arangoClient.db('main', username=username, password=password)

        # Insert edges into the graph.
        main = db.graph('main')
        collections, edges = _initData.fetchInitData()
        ## Create edges randomly between the vertices
        for edge in edges:
            try:
                print(f"#################################### Creating mocked edges for {edge["edgeName"]}")
                import importlib
                fromCollection = edge["fromCollection"][0]
                toCollection = edge["toCollection"][0]
                fromPkg = importlib.import_module("_"+str(fromCollection))
                toPkg = importlib.import_module("_"+str(toCollection))
                #{"edgeName":"HAS_SUBSCRIPTION","fromCollection":["customer"],"toCollection":["subscription"]}

                #graph = main.edge_collection(edge["edgeName"])
                fromIds = fromPkg.fetchAll(arangoClient)
                toIds = toPkg.fetchAll(arangoClient)
                print(f"Total from vertices : {len(fromIds["data"])}")
                print(f"Total to vertices : {len(toIds["data"])}")
                for fromId in fromIds["data"]:
                    toId = random.choice(toIds["data"])
                    # The "_id" field is required instead of "_key" field.
                    idString = f"{edge["edgeName"]}/{fromId}-{toId}"
                    fromString = f"{fromCollection}/{fromId}"
                    toString = f"{toCollection}/{toId}"
                    logging.info("models.createRelationship - from : {} : {} : {}".format(idString,fromString,toString))
                    main.insert_edge(
                        collection=edge["edgeName"],
                        edge={
                            '_id': idString,
                            '_from': fromString,
                            '_to': toString,
                            'label': edge["edgeName"]
                        }
                    )
            except Exception as e:
                logging.info(e, exc_info=True)
    except Exception as e:
        logging.info(e, exc_info=True)