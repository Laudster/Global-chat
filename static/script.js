var socket = io.connect(window.location.origin);
if (location.pathname == "/") socket.emit("establish_relation", {room: "/Global"});
else socket.emit("establish_relation", {room: location.pathname});

socket.on("connect", function(){
    document.getElementById("disconnected").hidden = true;
    socket.emit("get-username", function(user){
        if (user != "Anon"){
            document.getElementById("account-bar").style.display = "none";
            document.getElementById("usernamedisplay").innerHTML = user;
        }
    })
});

socket.on("disconnect", function(){
    document.getElementById("disconnected").hidden = false;
});

function update_page() {

    socket.emit("get-messages", location.pathname, function(messages){
        $('#messages').empty();

        messages.reverse().forEach(function(message) {
            let message_text = message.value
            let image = "";

            if (message_text[message_text.length] != ">"){
                for (let i = message_text.length; i >0; i--){
                    if (message_text[i] == "|"){
                        image = message_text.substring(i + 1, message_text.length)
                        message_text = message_text.substring(0, i - 1);
                    }
                }
            }

            $('#messages').append(message_text);
            if (image != ""){
                if (!image.endsWith(".mp4") && !image.endsWith(".wav") && !image.endsWith(".mp3") && !image.endsWith(".ogv")){
                    $('#messages').append('<img src="/get-image?filename=' + image + '">');
                } else if (image.endsWith(".mp4")){
                    $('#messages').append('<video controls> <source src="/get-image?filename=' + image + '"></video>');
                } else {
                    $('#messages').append('<audio controls> <source src="/get-image?filename=' + image + '"></audio>');
                }
            }
        });
    })
}

function create_list(type){
    socket.emit("get-username", function(user){
        var head = document.createElement("div");
        head.id = type + "list";
        var new_whited = document.createElement("input");
        new_whited.type = "text";
        head.appendChild(new_whited);

        var listdiv = document.createElement("div");
        listdiv.className = "list";

        var list = document.createElement("ul");

        var listelement

        if (type != "white"){
            listelement =  document.createElement("li");
            var listelementcontent = document.createElement("p");
            listelementcontent.textContent = user;
            listelement.appendChild(listelementcontent);

            list.appendChild(listelement);
        }

        listdiv.appendChild(list);

        head.appendChild(listdiv);

        document.getElementById("room-settings").insertBefore(head, document.getElementById("enable" + type + "list").nextSibling.nextSibling.nextSibling.nextSibling.nextSibling);
    })
}

function get_rooms(){
    socket.emit("get-rooms", function(data){
        socket.emit("get-username", (user) => {
            data.forEach(function(room){
                let link = document.createElement("a");
                link.href = room["name"]
                link.textContent = room["name"]
    
                if (location.pathname.split("/")[1] == room["name"] || room["name"] == "Global" && location.pathname.split("/")[1] == ""){
                    link.style.backgroundColor = "rgb(49, 53, 54)";
                }
    
                $("#rooms").append(link);
    
                if (user.replace(" ", "") == room["creator"].replace(" ", "")){
                    let settings = document.createElement("button");
                    settings.className = "donotformatthisfuckingbutton";
                    let image = document.createElement("img");
                    image.src = "static/settings.png";
                    image.width = 20;

                    settings.onclick = () => {
                        if (document.getElementById("room-settings").style.display == "none"){
                            socket.emit("get-list-statuses", room["name"], function(data){
                                console.log(data);
                                if (data[0] != null){
                                    document.getElementById("enablewhitelist").checked = true;
                                    create_list("white");
                                    var listdiv = document.getElementById("whitelist").querySelector('div');

                                    var list = document.createElement("ul");

                                    data.forEach(member => {
                                        var listelement = document.createElement("li");
                                        listelement.textContent = member;
                                        list.appendChild(listelement);
                                    });

                                    listdiv.appendChild(list);
                                }
                                if (data[1] != null){
                                    document.getElementById("enableblacklist").checked = true;
                                    create_list("black");
                                    document.getElementById("blacklist").querySelector("div").empty();
                                }
                            });
                            document.getElementById("room-settings").style.display = "block";
                            document.getElementById("room-settings").querySelector("h3").textContent = room["name"] + " chat";
                        } else document.getElementById("room-settings").style.display = "none";
                    }

                    settings.innerHTML = image.outerHTML;
                    document.getElementById("rooms").lastChild.style.display = "inline-block";
                    $("#rooms").append(settings);
                    $("#rooms").append(document.createElement("br"));
                }
            });
            $("#rooms").append('<button onclick="new_room()"> + </button>');
        });
    });
}

function delete_room(){
    socket.emit("delete-room", document.getElementById("room-settings").querySelector("h3").textContent.split(" ")[0]);
    window.location.replace("/");
}

function new_room(){
    let room_name = prompt("New Room");

    if (room_name){
        if (room_name.search(" ") != -1){
            alert("Room name may not contain spaces");
        } else{
            socket.emit("new-room", room_name, function(room){
                window.location.replace("/" + room);
            })
        }
    }
}

socket.on("update", update_page);

function formdatatodict(formdata)
{
    const data = {};

    formdata.forEach((value, key) => {
        if (value instanceof File) {
            if (value.size >= 5000000){
                alert("Image is too big, maximum size is 5mb");
                upload = false;
            }
            data[key] = value.name;
        } else {
            data[key] = value;
        }
    });

    return data;
}

function send_message(event){
    event.preventDefault();

    socket.emit("get-username", function(username){
        let formdata = new FormData($("#poster")[0]);
        formdata.append("room", location.pathname);
        formdata.append("display_name", username);

        document.getElementById("usernamedisplay").innerHTML = username;
    
        const data = formdatatodict(formdata);

        let upload = true;
    
        if (upload == true){
            socket.emit("new-message", data);
            $("#poster")[0].reset();
    
            const image = formdata.get("image");
    
            if (image && image.type.startsWith("image/") || image && image.type.startsWith("video/") || image && image.type.startsWith("audio/")) {
            socket.emit("new-image", {"image": image, "filename": data["image"]});
            }
        }
    });
}

$(document).ready(function() {
    get_rooms();
    update_page();

    let title = document.getElementById("title")
    title.href = "#" + location.pathname
    if (location.pathname == "/"){
        title.textContent = "Global chat"
    } else{
        title.textContent = location.pathname.split("/")[1] + " chat"
    }

    $("#poster").on("submit", event => send_message(event));

    $("#message").on("keydown", event => {
        if (event.key == "Enter" && !event.shiftKey) {
            send_message(event);
        }
    });


    document.getElementById("enableblacklist").addEventListener("change", (event) => {
        if (event.target.checked == true){
            create_list("black");
            socket.emit("init-list", {"type": "black", "room": event.target.parentElement.querySelector("h3").textContent.split(" ")[0]});
        } else if (event.target.checked == false){
            document.getElementById("blacklist").remove();
            socket.emit("remove-list", {"type": "black", "room": event.target.parentElement.querySelector("h3").textContent.split(" ")[0]});
        }
    })

    document.getElementById("enablewhitelist").addEventListener("change", (event) => {
        if (event.target.checked == true){
            create_list("white");
            socket.emit("init-list", {"type": "white", "room": event.target.parentElement.querySelector("h3").textContent.split(" ")[0]});
        } else if (event.target.checked == false){
            document.getElementById("whitelist").remove();
            socket.emit("remove-list", {"type": "white", "room": event.target.parentElement.querySelector("h3").textContent.split(" ")[0]});
        }
    })

    $("#inlog").on("submit", function(event){
        event.preventDefault();

        fetch("/login-attempt", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formdatatodict(new FormData($("#inlog")[0])))
        })
        .then (response => response.json())
        .then (data => {
            if (data.status == "login-sucess"){
                location.reload();

                document.getElementById("login").close();
                document.getElementById("account-bar").style.display = "none";

                document.getElementById("usernamedisplay").innerHTML = data.username;
            } else if (data.status == "login-fail"){
                alert("Wrong Login Credentials");
            }
        })
    });

    $("#accountcreate").on("submit", function(event){
        event.preventDefault();
        
        socket.emit("check-for-email", document.getElementById("emailcreate").value);
    });

    socket.on("email-used", function(){
        $("#accountcreate")[0].reset();
        alert("Email Already In Use");
    });

    socket.on("email-free", function(){
        socket.emit("email-confirm", document.getElementById("emailcreate").value);

        document.getElementById("createaccount").close();
        document.getElementById("confirmemail").showModal();
    });

    $("#emailconfirm").on("submit", function(event){
        event.preventDefault();

        socket.emit("email-code", {"code": document.getElementById("emailcode").value})
    });

    socket.on("correct code", function(){
        document.getElementById("confirmemail").close();
        document.getElementById("accountinfo").showModal();
    });

    socket.on("incorrect code", function(){
        alert("Incorrect Code");
    });

    $("#infoaccount").on("submit", function(event)
    {
        event.preventDefault();

        if (document.getElementById("password").value == document.getElementById("passwordconfirm").value)
            {
                socket.emit("username-check", document.getElementById("username").value);
            } else
            {
                alert("Passwords don't match");
                $("#infoaccount")[0].reset();
            }
    });

    socket.on("username-used", function(){
        alert("Username already in use");
        $("#infoaccount")[0].reset();
    });

    socket.on("username-free", function(){
        socket.emit("account-create", {"username": document.getElementById("username").value, "password": document.getElementById("password").value});
        document.getElementById("accountinfo").close();
        document.getElementById("accountcreated").showModal();
    });
});