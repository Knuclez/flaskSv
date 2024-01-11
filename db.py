from pymongo import MongoClient
from bson.json_util import dumps

CONN_STRING = "mongodb://localhost:27017"

def check_cell_existance(cell : str):
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    cells = db['cells']
    cursor = cells.find({'position' : cell})
    results = list(cursor)
    if len(results) == 0:
        print("No existe")
        client.close()
        return False
    else:
        print("existe")
        client.close()
        return True

def create_cell_document(cell : str):
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    cells = db['cells']
    cells.insert_one({
        'position' : cell,
        'ocupants' : []
    })
    client.close()

def create_ocupant_document(ocupant_id : str, ocupant_type: str):
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    ocupants_collect = db['ocupants']
    ocupants_collect.insert_one({
        '_id' : ocupant_id,
        'type' : ocupant_type
    }) 
    client.close()

def get_ocupant_document(id : str):
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    ocu_collect = db['ocupants']
    doc = ocu_collect.find_one({'_id':id})
    client.close()
    return doc
    
def get_all_cell_ocupants():
    result = {}
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    cells = db['cells']
    cursor = cells.find()
    lista = list(cursor)
    client.close()
    result_jsn = dumps(lista, indent = 2)
    return result_jsn

def view_cell_ocupant(cell :str):
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    cells = db['cells']
    doc = cells.find_one({'position' : cell})
    client.close()
    return doc['ocupants']

def add_ocupant_to_cell_doc(cell : str, ocupant : str):
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    cells = db['cells']
    #the $operator operators belong to mongo, so for documentation consult there
    cells.update_one({'position' : cell}, {'$addToSet': {'ocupants' : ocupant}})
    client.close()

def delete_ocupant_from_cell_doc(cell : str, ocupant: str ):
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    cells = db['cells']
    cells.update_one({'position':cell}, {'$pull' : {'ocupants' : ocupant}})
    doc = cells.find_one({'position':cell})
    if len(doc['ocupants']) <= 0:
        cells.delete_one({'position':cell})
    client.close()


def create_action_doc(action:dict):
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    actions = db['actions']
    status = actions.insert_one(action)
    client.close()
    print(status.acknowledged)

def get_turn_actions(turn: str):
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    actions_coll = db['actions']
    turn_actions = actions_coll.find({'turn':turn})
    list_format = list(turn_actions)
    return list_format 

#NOT FOR USE
def create_db():
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    users = db['users']
    result = users.insert_one({
        'name' : 'marianeitor'
    })
    print(result)

#NOT FOR USE
def test_db():
    client = MongoClient(CONN_STRING)
    db = client['brutal']
    users = db['users']
    cursor = users.find()
    for doc in cursor:
        print(doc)