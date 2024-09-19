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

    return send_file(path.join("Images", filename), mimetype="image/jpeg")

def get_rooms_endpoint():
    data = [path.join(boards, f) for f in listdir(boards) if path.isfile(path.join(boards, f))]
    data = sorted(data, key=lambda x: path.getctime(x))

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

def get_rooms():
    return get_rooms_endpoint()