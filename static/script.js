function update_page() {
    $.ajax({
        url: "/get-messages",
        method: "GET",
        data: {room: location.pathname},
        success: function(data) {
            $('#messages').empty();
            
            data.messages.reverse().forEach(function(message) {
                let ra = message.value
                let image = "";

                if (ra[ra.length] != ">"){
                    for (let i = ra.length; i >0; i--){
                        if (ra[i] == "@"){
                            image = ra.substring(i + 1, ra.length)
                            ra = ra.substring(0, i - 1);
                        }
                    }
                }

                $('#messages').append(ra);
                if (image != ""){
                    $('#messages').append('<img src="/get-image?filename=' + image + '">');
                }
            });
        }
    });
}

function situation_update(){
    if (document.getElementById("messages").childElementCount > 0){
        $.ajax({
            url: "/get-situation",
            method: "GET",
            data: {newest_message: document.getElementById("messages").firstElementChild.outerHTML, room: location.pathname},
            success: function(data){
                if (data == true){
                    update_page();
                }
            }
        });
    }
}

function get_rooms(){
    $.ajax({
        url: "/get-rooms",
        method: "GET",
        success: function(data){
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
        }
    });
}

function new_room(){
    let room_name = prompt("New Room");

    if (room_name){
        if (room_name.search(" ") != -1){
            alert("Room name may not contain spaces");
        } else{
                $.ajax({
                url: "/new-room",
                method: "POST",
                data: {room_name: room_name},
                success: function(response)
                {
                    window.location.replace("/" + room_name);
                }
            });
        }
    }
}

function send_message(event){
    event.preventDefault();

    let formdata = new FormData($("#poster")[0]);
    formdata.append('room', location.pathname);

    $.ajax({
        url: "/new-message",
        method: "POST",
        data: formdata,
        processData: false,
        contentType: false,
        success: function(response) {
            $("#poster").find("input[type=text], input[type=file], textarea").val('');
            update_page();
        }
    });
}

setInterval(situation_update, 1000);

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