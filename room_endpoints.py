from os import path, remove, listdir
from flask import session
from json import dump, load

boards = "boards"

def update_file(file, data):
    file.seek(0)
    file.truncate()
    dump(data, file, indent=4)

def new_room_endpoint(data) -> str:
    room_name = data

    if not path.exists(f"boards/{room_name}.json"):
        with open(f"boards/{room_name}.json", "w") as file:
            data = {"creator": session.get("login", "Anon"), "whitelist": None, "blacklist": None, "messages": []}
            dump(data, file, indent=4)
    
    return room_name

def delete_room_endpoint(data) -> str:
    remove(f"boards/{data}.json")

    return ""

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

    data = []

    for v in names:
        creator : str
        with open(f"{boards}/{v}.json", "r") as file:
            board_data = load(file)
            creator = board_data["creator"]
        data.append({"name": v, "creator": creator})

    return data

def init_list_endpoint(data):
    with open(f"{boards}/{data['room']}.json", "r+") as file:
        board_data = load(file)
        board_data[data["type"] + "list"] = [session.get("login")]
        update_file(file, board_data)

def remove_list_endpoint(data):
    with open(f"{boards}/{data['room']}.json", "r+") as file:
        board_data = load(file)
        board_data[data["type"] + "list"] = None
        update_file(file, board_data)

def get_list_statuses_endpoint(data):
    contents = []

    for v in ["white", "black"]:
         with open(f"{boards}/{data}.json", "r+") as file:
            board_data = load(file)
            contents.append(board_data[v + "list"])
    
    return contents