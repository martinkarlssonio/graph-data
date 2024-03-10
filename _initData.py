
def fetchInitData():
    collections = [
        "customer",
        "user",
        "machine",
        "machineType",
        "region",
        "userRole",
        "subscription"
        "software"
    ]

    edges = [
        {"edgeName":"HAS_SUBSCRIPTION","fromCollection":["customer"],"toCollection":["subscription"]},
        {"edgeName":"OF_TYPE","fromCollection":["machine"],"toCollection":["machineType"]},
        {"edgeName":"RUNS_SOFTWARE","fromCollection":["machine"],"toCollection":["software"]},
        {"edgeName":"OWNED_BY","fromCollection":["machine"],"toCollection":["customer"]},
        {"edgeName":"EMPLOYED_AT","fromCollection":["user"],"toCollection":["customer"]},
        {"edgeName":"IN_REGION","fromCollection":["customer"],"toCollection":["region"]},
        {"edgeName":"OPERATES_IN","fromCollection":["machine"],"toCollection":["region"]},
        {"edgeName":"HAS_ROLE","fromCollection":["user"],"toCollection":["userRole"]}
        ]

    return collections,edges