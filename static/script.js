function update_page() {
    $.ajax({
        url: "/get-messages",
        method: "GET",
        data: {room: location.pathname},
        success: function(data) {
            $('#messages').empty();
            
            data.messages.reverse().forEach(function(message) {
                let content = '<h2 style="margin-bottom: 20px;" class="message">' + message.displayname;

                const splits = message.value.split(" ");
                
                for (let i = 0; i < splits.length; i++){
                    let cut = splits[i];
                    let cut_text = cut;

                    const domener = [".com", ".no", ".net", ".org", ".co", ".us", ".io", ".gg", ".ai", ".gov", ".info", ".se", ".de", ".edu", ".mil", ".eu"];
                    let domenet;

                    let er_lenke = false;

                    for (const domene of domener){
                        if (cut.search(domene) != -1){
                            console.log(cut);
                            er_lenke = true;
                            domenet = domene;
                        }
                    }

                    if (er_lenke == true){
                        cut_text = cut.split(domenet)[0];

                        if (cut.search("//") != - 1){
                            if (cut.search("www.")){
                                content += '<a target="_blank" href=' + cut + ' >' + cut_text.split("//")[1].split("www.")[1] + ' </a>';
                            } else{
                                content += '<a target="_blank" href=' + cut + ' >' + cut_text.split("//")[1] + ' </a>';
                            }
                        } else{
                            content += '<a target="_blank" href=' + "https://" + cut + ' >' + cut_text + ' </a>';
                        }
                    } else{
                        content += cut_text + " ";
                    }
                }

                content += '</h2>'

                $('#messages').append(content);
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

    var form = document.getElementById("poster");
    var textarea = document.getElementById("message");

    textarea.addEventListener("keydown", function(event){
        if (event.key == "Enter" && !event.shiftKey){
            event.preventDefault();
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
        }
    });
});