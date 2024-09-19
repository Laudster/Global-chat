var socket = io.connect(window.location.origin);

socket.on("connect", function(){
    document.getElementById("disconnected").hidden = true;
    socket.emit("websocket_event", {data: "connection established"}, function(){
        console.log("suc");
    }).on("error", function(){
        console.log("fucked");
    });
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
                $('#messages').append('<img src="/get-image?filename=' + image + '">');
            }
        });
    })
}

function get_rooms(){
    socket.emit("get-rooms", function(data){
        if (location.pathname.split("/")[1] == ""){
            $("#rooms").append('<a style="background-color: rgb(49, 53, 54);" href="/" > Global </a>')
        } else{
            $("#rooms").append('<a href="/" > Global </a>')
        }
        
        data.forEach(function(room){
            if (location.pathname.split("/")[1] == room){
                $("#rooms").append('<a style="background-color: rgb(49, 53, 54);" href=' + room + '>' + room + '</a>');
            } else{
                $("#rooms").append('<a href=' + room + '>' + room + '</a>');
            }
        });
        $("#rooms").append('<button onclick="new_room()"> + </button>');
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

function send_message(event){
    event.preventDefault();
    let formdata = new FormData($("#poster")[0]);
    formdata.append("room", location.pathname);

    const data = {};
    
    let upload = true;

    formdata.forEach((value, key) => {
        if (value instanceof File) {
            console.log(value.size);
            if (value.size > 5000000){
                alert("Image is too big, maximum size is 5mb");
                upload = false;
            }
            data[key] = value.name;
        } else {
            data[key] = value;
        }
    });

    if (upload == true){
        socket.emit("new-message", data);
        $("#poster")[0].reset();

        const image = formdata.get("image");

        if (image && image.type.startsWith("image/")) {
        socket.emit("new-image", {"image": image, "filename": data["image"]});
        }
    }
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
});