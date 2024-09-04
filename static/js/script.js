function update_page() {
    $.ajax({
        url: "/get-messages",
        method: "GET",
        data: {room: location.pathname},
        success: function(data) {
            $('#messages').empty();
            
            data.messages.reverse().forEach(function(message) {
                $('#messages').append('<h2 class="message">' + message.displayname + message.value + '</h2>');
            });
        }
    });
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
    var room_name = prompt("New Room");

    if (room_name.search(" ") != -1){
        alert("Room name may not contain spaces");
    } else{
            $.ajax({
            url: "/new-room",
            method: "POST",
            data: {room_name: room_name},
            success: function(response)
            {
                location.reload();
            }
        });
    }
}

setInterval(update_page, 5000);

$(document).ready(function() {
    get_rooms();
    update_page();

    var title = document.getElementById("title")
    title.href = "#" + location.pathname
    if (location.pathname == "/"){
        title.textContent = "Global chat"
    } else{
        title.textContent = location.pathname.split("/")[1] + " chat"
    }

    $("#poster").on("submit", function(event) {
        event.preventDefault(); // Prevent the default form submission

        var formdata = $(this).serialize(); // Serialize form data
        formdata += '&room=' + encodeURIComponent(location.pathname);

        $.ajax({
            url: "/new-message",
            method: "POST",
            data: formdata,
            success: function(response) {
                $("#poster").find("input[type=text], textarea").val('');
                update_page();
            }
        });
    });
});