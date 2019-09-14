//web socket
var loc = window.location;
var message = $(".chat_input");
var form = $("#form");
var username = $("#username");
var endpoint = 'ws://' + loc.host + loc.pathname;
var chat_page = 1;
if(1 == $("#pagesNumber").val()){
    $(".chat-upload").hide();
}

$(".chat-upload").click(function(){
    if(chat_page == $("#pagesNumber").val()){
        $(this).hide();
    }
    else{
    var xml = new XMLHttpRequest();
    xml.open('GET', 'http://127.0.0.1:8000/chat/json/' + loc.pathname.substring(6) + "?page=" + String(chat_page))
    xml.onload = function(){
        messages = JSON.parse(xml.responseText);
        for(var i=0;i<messages.length;i++)
            if(messages[i].sender == username.val())
            $(".chat-upload").after("<div class='row msg_container base_sent'><div class='col-md-10 col-xs-10'><div class='messages msg_sent'><p>"+messages[i].message+"</p><time datetime='2009-11-13T20:00'>Timothy • 51 min</time></div></div><div class='col-md-2 col-xs-2 avatar'><img src='"+ messages[i].photo_url+"' class='img-responsive'></div></div>");
            else
                $(".chat-upload").after("<div class='row msg_container base_receive'><div class='col-md-2 col-xs-2 avatar'><img src='"+ messages[i].photo_url+"' class='img-responsive'></div><div class='col-md-10 col-xs-10'><div class='messages msg_receive'><p>"+messages[i].message+"</p><time datetime='2009-11-13T20:00'>Timothy • 51 min</time></div></div></div>");
    }
    xml.send();
    chat_page++; 
    }
})
var socket = new WebSocket(endpoint);
socket.onopen = function(e){
        form.submit(function(event){
            console.log("Yes");
            event.preventDefault();
            data = {"message": message.val()};
            socket.send(JSON.stringify(data));
            form[0].reset();
})
}
socket.onmessage = function(e){
        data = JSON.parse(e.data)
        if(username.val() == data["username"])
            $(".msg_container").last().after("<div class='row msg_container base_sent'><div class='col-md-10 col-xs-10'><div class='messages msg_sent'><p>"+data["message"]+"</p><time datetime='2009-11-13T20:00'>Timothy • 51 min</time></div></div><div class='col-md-2 col-xs-2 avatar'><img src='"+ data["photo_url"]+"' class='img-responsive'></div></div>");
        else
        $(".msg_container").last().after("<div class='row msg_container base_receive'><div class='col-md-2 col-xs-2 avatar'><img src='"+ data["photo_url"]+"' class='img-responsive'></div><div class='col-md-10 col-xs-10'><div class='messages msg_receive'><p>"+data["message"]+"</p><time datetime='2009-11-13T20:00'>Timothy • 51 min</time></div></div></div>");

}
socket.onerror = function(e){
    console.log("error", e)
}
socket.onclose = function(e){
    console.log("close", e)
}