var socket = io.connect(window.location.origin);
if (location.pathname == "/") socket.emit("establish_relation", {room: "/Global"});
else socket.emit("establish_relation", {room: location.pathname});

socket.on("connect", function(){
    document.getElementById("disconnected").hidden = true;
    socket.emit("get-username", function(user){
        console.log(user);
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
    console.log("updater");

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
                $('#messages').append('<img src="/get-image?filename=' + image + '">');
            }
        });
    })
}

function get_rooms(){
    socket.emit("get-rooms", function(data){
        console.log(data);
        if (location.pathname.split("/")[1] == ""){
            $("#rooms").append('<a style="background-color: rgb(49, 53, 54);" href="/" > Global </a>')
        } else{
            $("#rooms").append('<a href="/" > Global </a>')
        }

        socket.emit("get-username", (user) => {
            data.forEach(function(room){
                let link = document.createElement("a");
                link.href = room["name"]
                link.textContent = room["name"]
    
                if (location.pathname.split("/")[1] == room["name"]){
                    link.style.backgroundColor = "rgb(49, 53, 54)";
                }
    
                $("#rooms").append(link);
    
                if (user.replace(" ", "") == room["creator"].replace(" ", "")){
                    let settings = document.createElement("button");
                    settings.className = "donotformatthisfuckingbutton";
                    let image = document.createElement("img");
                    image.src = "static/settings.png";
                    image.width = 20;
                    settings.innerHTML = image.outerHTML;
                    document.getElementById("rooms").lastChild.style.display = "inline-block";
                    document.getElementById("rooms").lastChild.style.marginLeft = "20%";
                    document.getElementById("rooms").lastChild.style.paddingRight = "20%";
                    $("#rooms").append(settings);
                } else console.log(room["creator"]);
            });
            $("#rooms").append('<button onclick="new_room()"> + </button>');
        });
    });
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
    
            if (image && image.type.startsWith("image/")) {
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

    $("#inlog").on("submit", function(event){
        event.preventDefault();

        socket.emit("login-attempt", formdatatodict(new FormData($("#inlog")[0])));
    });

    socket.on("login-sucess", function(username){
        console.log(username);

        document.getElementById("login").close();
        document.getElementById("account-bar").style.display = "none";

        document.getElementById("usernamedisplay").innerHTML = username;
    });

    socket.on("login-fail", function(){
        alert("Wrong Login Credentials");
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