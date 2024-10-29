from flask import request, send_file
from json import load
from os import path, listdir

boards = "boards"

def get_messages_endpoint(data):
    room = data

    room = room[1:len(room)]

    if room == "/" or room == "":
        room = "Global"
    elif path.exists(f"{boards}/{room}.json") == True:
        with open(f"{boards}/{room}.json", "r") as file:
            message_data = load(file)

        return message_data["messages"]

    with open(f"{boards}/{room}.json", "r") as file:
        message_data = load(file)

    return message_data["messages"]

def get_image_endpoint():
    filename : str
    filename = str(request.args.get("filename"))

    print(path.join("Images", filename))

    return send_file(path.join("Images", filename))