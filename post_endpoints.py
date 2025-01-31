from json import dump, load
from os import path

def update_file(file, data):
    file.seek(0)
    file.truncate()
    dump(data, file, indent=4)

def new_image_endpoint(image) -> str:
    image_file = image.get("image")
    filename = image.get("filename").replace(" ", "")
    with open(f"Images/{filename}", "wb") as file:
        file.write(image_file)

    return "image sent"

def post_endpoint(data, socket) -> str:
    message = data.get("message")
    display_name = data.get("display_name")

    if display_name == "":
        display_name = "Anon"

    room = data.get("room")

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
        image = data.get("image")
        image_name += "|" + image.replace(" ", "")
            
    except:
        pass

    if room == "" or room == "/":
        room = "/Global"

    with open(f"boards/{room}.json", "r+") as file:
        message_data = load(file)
        if not display_name:
            display_name = "Anon"
        message_data["messages"].append({"value": content + "</h2> " + image_name, "displayname": display_name+": "})
        
        update_file(file, message_data)

    if image_name == "|":
        socket.emit("update", room=room) # , to=room
    else:
        while not path.exists(f"Images/{image_name[1:len(image_name)]}") == True:
            pass
        socket.emit("update", room=room) #, room="/" + room

    return "Great success"