from flask import request, jsonify
from flask_socketio import send
import json
import os   

boards = "boards"

def update_file(file, data):
    file.seek(0)
    file.truncate()
    json.dump(data, file, indent=4)

"""
def post_endpoint():
    message = request.form.get("message")
    display_name = request.form.get("display_name")

    if display_name == "":
        display_name = "Anon"

    room = request.form.get("room")
    room = room[1:len(room)]

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

    send("new-message")
    return jsonify()

"""

def new_room_endpoint():
    room_name = request.form.get("room_name")

    if not os.path.exists(f"{boards}/" + room_name + ".json"):
        with open(f"{boards}/{room_name}.json", "w") as file:
            data = {"messages": []}
            json.dump(data, file, indent=4)
    
    return room_name