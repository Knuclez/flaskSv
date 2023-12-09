from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p> Vamos los pibes</p>"

@app.post("/users")
def check_user():
    texto = request.get_data(True, True, False)
    if look_for_user(texto):
        return texto
    else:
        return '1'

@app.get("/chat")
def give_chat():
    return {"jeje": "jojo"}

@app.post("/chat")
def receive_chat():
    try:
        texto = request.get_data(True, True, False)
        write_to_txt(texto)
        return "Ok"
    except Exception as excp:
        print(type(excp))


# AUXs----------------------------------------------
def look_for_user(username : str) -> bool:
    json_dir : str = "./data/users.json"
    
    with open(json_dir) as f:
        data = json.load(f)
        if username in data['users']:
            return True
        else:
            return False
        
def write_to_txt(entering_chat: str):
    txt_dir : str = "./data/chat.txt"
    with open(txt_dir, "a") as f:
        f.write(entering_chat + "\n")
        f.close()

# LAUNCH-------------------------------------------
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000,debug=True)