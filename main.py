from flask import Flask

app = Flask(__name__)

def write_to_txt(entering_chat: str):
    txt_dir : str = "./chat.txt"
    with open(txt_dir, "a") as f:
        f.write(entering_chat + "\n")
        f.close()

@app.route("/")
def hello_world():
    return "<p> Vamos los pibes</p>"

@app.post("/chat/<string:chat>")
def receive_chat(chat):
    write_to_txt(chat)
    return f"{chat}"

@app.get("/chat")
def give_chat():
    return {"jeje": "jojo"}

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000,debug=True)