from pymongo import MongoClient

CONN_STRING = "mongodb://localhost:27017"


def create_cell_document(cell : str):
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    cells = db['cells']
    cells.insert_one({
        'position' : cell,
        'ocupants' : []
    })
    

def add_ocupant_to_cell_doc(cell : str, ocupant : str):
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    cells = db['cells']
    #the $operator operators belong to mongo, so for documentation consult there
    cells.update_one({'position' : cell}, {'$addToSet': {'ocupants' : ocupant}})

def delete_ocupant_from_cell_doc(cell : str, ocupant: str ):
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    cells = db['cells']
    cells.update_one({'position':cell}, {'$pull' : {'ocupants' : ocupant}})


#NOT FOR USE
def create_db():
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    users = db['users']
    result = users.insert_one({
        'name' : 'marianeitor'
    })
    print(result)

#NOT FOR USER
def test_db():
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    users = db['users']
    cursor = users.find()
    for doc in cursor:
        print(doc)