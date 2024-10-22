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
    names = [path.join(boards, f) for f in listdir(boards) if path.isfile(path.join(boards, f))]
    names = sorted(names, key=lambda x: path.getctime(x))

    for i, v in enumerate(names):
        if v.find("\\") != -1:
            split = v.split("\\")
            names[i] = split[len(split) - 1]
        else:
            split = v.split("/")
            names[i] = split[len(split) - 1]
    
    for i, v in enumerate(names):
        split = v.split(".")
        names[i] = split[0]

    names.remove("Global")

    data = []

    for v in names:
        creator : str
        with open(f"{boards}/{v}.json", "r") as file:
            board_data = load(file)
            creator = board_data["creator"]
        data.append({"name": v, "creator": creator})

    return data