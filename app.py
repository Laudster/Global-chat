from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import json
import os

app = Flask(__name__)

boards = "boards"

def update_file(file, data):
    file.seek(0)
    file.truncate()
    json.dump(data, file, indent=4)

@app.route("/")
def globall():
    messages : str
    display_name = request.args.get("display_name")\

    with open(f"{boards}/Global.json", "r") as file:
        data = json.load(file)
        messages = data["messages"]

    return render_template("global.html", messages=messages, displayer=display_name)

@app.route("/<room>")
def room(room):
    if os.path.exists(f"{boards}/{room}.json"):
        messages : str
        display_name = request.args.get("display_name")

        with open(f"{boards}/{room}.json", "r") as file:
            data = json.load(file)
            messages = data["messages"]

        return render_template("global.html", messages=messages, displayer=display_name)
    
    return redirect(url_for("globall"))


@app.route("/get-messages", methods=["GET"])
def get_messages():
    room = request.args.get("room")

    room = room[1:len(room)]

    if room == "/" or room == "":
        room = "Global"
    elif os.path.exists(f"{boards}/{room}.json") == True:
        with open(f"{boards}/{room}.json", "r") as file:
            message_data = json.load(file)

        return jsonify(message_data)

    with open(f"{boards}/{room}.json", "r") as file:
        message_data = json.load(file)

    return jsonify(message_data)

@app.route("/get-image", methods=["GET"])
def get_image():
    filename : str
    filename = str(request.args.get("filename"))

    return send_file(os.path.join("Images", filename), mimetype="image/jpeg")

@app.route("/get-rooms", methods=["GET"])
def get_rooms():
    data = [os.path.join(boards, f) for f in os.listdir(boards) if os.path.isfile(os.path.join(boards, f))]
    data = sorted(data, key=lambda x: os.path.getctime(x))

    for i, v in enumerate(data):
        if v.find("\\") != -1:
            split = v.split("\\")
            data[i] = split[len(split) - 1]
        else:
            split = v.split("/")
            data[i] = split[len(split) - 1]
    
    for i, v in enumerate(data):
        split = v.split(".")
        data[i] = split[0]

    data.remove("Global")
    
    return data

@app.route("/new-message", methods=["POST"])
def post():
    message = request.form.get("message")
    display_name = request.form.get("display_name")

    room = request.form.get("room")
    room = room[1:len(room)]

    image_name = ""

    try:
        image = request.files.get("image")
            
        image.save(os.path.join("Images", image.filename))
        print(image.filename.replace(" ", ""))
        os.rename(f"Images/{image.filename}", f"Images/{image.filename.replace(" ", "")}")
        image_name += " @" + image.filename.replace(" ", "")
            
    except:
        pass # No Image

    if room == "" or room == "/":
        room = "Global"

    with open(f"{boards}/{room}.json", "r+") as file:
        message_data = json.load(file)
        if not display_name:
            display_name = "Anon"
        message_data["messages"].append({"value": message + image_name, "displayname": display_name+": "})
        update_file(file, message_data)

    return jsonify()

@app.route("/new-room", methods=["POST"])
def new_room():
    room_name = request.form.get("room_name")

    if not os.path.exists(f"{boards}/" + room_name + ".json"):
        with open(f"{boards}/{room_name}.json", "w") as file:
            data = {"messages": []}
            json.dump(data, file, indent=4)
    
    return room_name


if __name__ == "__main__":
    #app.run(debug=False, host="0.0.0.0") # public
    app.run(debug=True) # debug