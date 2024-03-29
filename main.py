from flask import Flask, request
import db
import json

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p> Vamos los pibes</p>"

@app.post("/users")
def check_user():
    texto = request.get_data(True, True, False)

    return look_for_user(texto)

@app.get("/turn")
def get_turn():
    return str(read_turn())

@app.get("/passturn")
def post_turn():
    actual_turn = read_turn()
    process_turn_actions(actual_turn)
    update_turn(actual_turn + 1)
    return str(read_turn())

@app.get("/ocupants/<ocu_id>")
def get_ocu(ocu_id :str):
    doc = db.get_ocupant_document(ocu_id)
    return doc

@app.post("/ocupants")
def post_ocu():
    body = request.get_json()
    model = get_ocupant_model(body['model_id'])
    _id = str(db.count_ocupants())

    db.create_ocupant_document(_id, model, body['owner_id'])
    write_in_cell(body['cell_id'], _id)
    return "Ok"


@app.get("/cells") 
def get_cells():
    dicct = db.get_all_cell_ocupants()
    return dicct

@app.get("/cell/<cell_id>")
def get_cell_ocupants(cell_id : str):
    cell = look_for_cell_ocupants(cell_id)
    if  cell == None:
        return 'Generic Error'
    else:
        return cell

@app.post("/cell/<cell_id>")
def post_to_cell(cell_id:str):
    body = request.get_data(True, True, False)
    result = write_in_cell(cell_id, body)
    return result

@app.post("/cell/<cell_id>/remove")
def remove_from_cell(cell_id : str):
    body = request.get_data(True, True, False)
    res = delete_from_cell(cell_id, body)
    return res 

@app.post("/actions")
def notice_action():
    body = request.get_json()
    body['turn'] = read_turn()
    db.create_action_doc(body)
    return "Ok"

# AUXs----------------------------------------------
def look_for_user(username : str) -> bool:
    json_dir : str = "./data/users.json"
    
    with open(json_dir) as f:
        data = json.load(f)
        if username in data:
            return data[username]
        else:
            return "no-user"
    
def get_ocupant_model(model_id):
    json_dir : str = "./data/ocupant_models.json"

    with open(json_dir) as f:
        data = json.load(f)
        if model_id in data:
            return data[model_id]
        else:
            return data["0"]

def look_for_cell_ocupants(cell_id):
        if db.check_cell_existance(cell_id):
            return db.view_cell_ocupant(cell_id)
        else:
            db.create_cell_document(cell_id)
            return db.view_cell_ocupant(cell_id)
        
def write_in_cell(cell_id, data_to_write):
        if db.check_cell_existance(cell_id):
           db.add_ocupant_to_cell_doc(cell_id, data_to_write)
        else:
            db.create_cell_document(cell_id)
            db.add_ocupant_to_cell_doc(cell_id, data_to_write)
        return 'Ok'

def delete_from_cell(cell_id : str, data_to_delete : str):
        if db.check_cell_existance(cell_id):
           db.delete_ocupant_from_cell_doc(cell_id, data_to_delete)
           return 'Ok'
        else:
            return 'Cell doesnt exist'
        
def process_turn_actions(turn: int):
    db.delete_old_empty_cells()
    actions = db.get_turn_actions(turn)
    print(actions)
    for action in actions:
        execute_movement(action)
    #hay q pasar el turno de alguna forma?

def execute_movement(action):
    depart_origin = action['origin']
    destiny = action['destiny']
    actor_ocupant = action['ocupant']
    delete_from_cell(depart_origin, actor_ocupant)
    write_in_cell(destiny, actor_ocupant)
    
def write_to_txt(entering_chat: str):
    txt_dir : str = "./data/chat.txt"
    with open(txt_dir, "a") as f:
        f.write(entering_chat + "\n")
        f.close()

def read_turn() -> int:
    txt_dir : str = "./data/turn.txt"
    with open(txt_dir, "r") as f:
        turno : str = f.read()
        f.close()
    return int(turno)

def update_turn(new_turn : int):
   txt_dir : str = "./data/turn.txt" 
   with open(txt_dir, "w") as f:
       f.write(str(new_turn))
       f.close()

# LAUNCH-------------------------------------------
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000,debug=True)