from flask import Flask, request
import db
import json

app = Flask(__name__)


@app.route("/")
def hello_world():
    db.test_db()
    return "<p> Vamos los pibes</p>"

@app.post("/users")
def check_user():
    texto = request.get_data(True, True, False)
    if look_for_user(texto):
        return texto
    else:
        return 'Generic Error'

@app.get("/cell/<cell_id>")
def get_cell(cell_id : str):
    cell = look_for_cell(cell_id)
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
    return result

# AUXs----------------------------------------------
def look_for_user(username : str) -> bool:
    json_dir : str = "./data/users.json"
    
    with open(json_dir) as f:
        data = json.load(f)
        if username in data['users']:
            return True
        else:
            return False
        
def look_for_cell(cell_id):
    json_dir : str = "./data/cells.json"
    
    with open(json_dir) as f:
        data = json.load(f)
        if cell_id in data:
            return data[cell_id]
        else:
            return None
        
def write_in_cell(cell_id, data_to_write):
    try:
        json_dir : str = "./data/cells.json"
    
        with open(json_dir, 'r') as f:
            data = json.load(f)
            if cell_id in data:
                modif = data
                modif[cell_id].append(data_to_write)
                newJson = json.dumps(modif, ensure_ascii=False)
            else:
                json.dumps([data_to_write], f ,ensure_ascii=False)

        with open(json_dir, 'w') as f:
            f.write(newJson)

        return 'Ok'
    except Exception as exp:
        return f'Generic Error {exp}'
        
def write_to_txt(entering_chat: str):
    txt_dir : str = "./data/chat.txt"
    with open(txt_dir, "a") as f:
        f.write(entering_chat + "\n")
        f.close()

# LAUNCH-------------------------------------------
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000,debug=True)