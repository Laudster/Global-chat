from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from post_endpoints import *
from get_endpoints import *


app = Flask(__name__)
#app.config["SECRET_KEY"] = "hemmelig"
socket = SocketIO(app)

@app.route("/")
def globall():
    messages : str
    display_name = request.args.get("display_name")\

    with open(f"{boards}/Global.json", "r") as file:
        data = json.load(file)
        messages = data["messages"]

    return render_template("chat.html", messages=messages, displayer=display_name, title="Global")

@app.route("/<room>")
def room(room):
    if os.path.exists(f"{boards}/{room}.json"):
        messages : str
        display_name = request.args.get("display_name")

        with open(f"{boards}/{room}.json", "r") as file:
            data = json.load(file)
            messages = data["messages"]

        return render_template("chat.html", messages=messages, displayer=display_name, title=room)
    
    return redirect(url_for("globall"))

@app.route("/get-situation")
def situation_report():
    return situation_report_endpoint()

@app.route("/get-messages", methods=["GET"])
def get_messages():
    return get_messages_endpoint()

@app.route("/get-image", methods=["GET"])
def get_image():
    return get_image_endpoint()

@app.route("/get-rooms", methods=["GET"])
def get_rooms():
    return get_rooms_endpoint()

@socket.on("new-message")
def post(data):
    message = data.get("message")
    display_name = data.get("display_name", "Anon")

    room = data.get("room")

    print(f"original: {data} new: {message} {display_name} {room}")

    content = '<h2 style="margin-bottom: 20px;" class="message">' + display_name + ": "

    splits = message.split(" ");
                
    for v in splits:
        cut = v
        cut_text = cut;

        domener = [".com", ".no", ".net", ".org", ".co", ".us", ".io", ".gg", ".ai", ".gov", ".info", ".se", ".de", ".edu", ".mil", ".eu"];
        domenet = ""

        for v2 in domener:
            if v2 in cut:
                domenet = v2;
                break;

        if domenet != "":
            cut_text = cut.split(domenet)[0];

            if "//" in cut:
                if "www." in cut:
                    content += '<a title="' + cut + '" target="_blank" href="' + cut + '" >' + cut_text.split("//")[1].split("www.")[1] + ' </a>';
                else:
                    content += '<a title="' + cut + '" target="_blank" href="' + cut + '" >' + cut_text.split("//")[1] + ' </a>';
                
            else:
                content += '<a title="' + cut + '" target="_blank" href="' + "https://" + cut + '" >' + cut_text + ' </a>';
            
        else:
            content += cut_text + " ";

    image_name = ""

    try:
        image = request.files.get("image")
            
        image.save(os.path.join("Images", image.filename))
        os.rename(f"Images/{image.filename}", f'Images/{image.filename.replace(" ", "")}')
        image_name += "@" + image.filename.replace(" ", "")
            
    except:
        pass # No Image

    if room == "" or room == "/":
        room = "Global"

    with open(f"{boards}/{room}.json", "r+") as file:
        message_data = json.load(file)
        if not display_name:
            display_name = "Anon"
        message_data["messages"].append({"value": content + "</h2> " + image_name, "displayname": display_name+": "})
        
        update_file(file, message_data)

    #emit("update")
    return jsonify()

@app.route("/new-room", methods=["POST"])
def new_room():
    return new_room_endpoint()

if __name__ == "__main__":
    #socket.run(app, debug=False, host="0.0.0.0") # public
    socket.run(app, debug=True)
