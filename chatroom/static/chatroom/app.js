let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let messageList = $('#messages');
let nextPage='';
let retrieveData=messageToLoad;
function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.timestamp);
    if (message.user === currentUser) position = 'right';
    const messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.user}</div>
                    <div class="text_wrapper">
                        <div class="text">${message.body}<br>
                            <span class="small">${date}</span>
                    </div>
                </div>
            </li>`;
    $(messageItem).appendTo('#messages');
}

function getConversation(recipient) {
    $.getJSON(window.location+`api/v1/message/?target=${recipient}`, function (data) {
        nextPage=data.next;
        console.log(data);

        messageList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });

}

function getMessageById(message) {
    id = JSON.parse(message).message;
    $.getJSON(window.location+`api/v1/message/${id}/`, function (data) {
        drawMessage(data);
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });
}

function sendMessage(recipient, body) {

    $.post(window.location+'api/v1/message/', {
        recipient: recipient,
        body: body
    }).fail(function () {
        alert('Error! Check console!');
    });
}



$(document).ready(function () {

    getConversation(currentRecipient);
//    let socket = new WebSocket(`ws://127.0.0.1:8000/?session_key=${sessionKey}`);
    var socket = new WebSocket(
        'ws://' + window.location.host + '/ws'+window.location.pathname);
    chatInput.keypress(function (e) {
        if (e.keyCode === 13) {
            chatButton.click();
        }
    });

    chatButton.click(function () {

        if (chatInput.val().length > 0) {
            sendMessage(currentRecipient, chatInput.val());
            chatInput.val('');

        }
    });

    socket.onmessage = function (e) {

        getMessageById(e.data);
    };
});


$(messageList).on('scroll', function() {

   if (messageList.scrollTop()==0) {
       if (!(retrieveData==messageToLoad)){
           return
       }
       var lastMsg = $('#messages:last-child');
       $.getJSON(nextPage, function (data) {
        console.log(data);

        nextPage=data.next;
        retrieveData=data['results'].length;
        for (let i = 0; i <retrieveData; i++) {
           let position = 'left';
            const date = new Date(data['results'][i].timestamp);
            if (data['results'][i].user === currentUser) position = 'right';
                const messageItem = `
                    <li class="message ${position}">
                        <div class="avatar">${data['results'][i].user}</div>
                            <div class="text_wrapper">
                                 <div class="text">${data['results'][i].body}<br>
                                    <span class="small">${date}</span>
                                </div>
                            </div>
                    </li>`;
        $(messageItem).prependTo('#messages');
        messageList.scrollTop(lastMsg.offset().top);

        }
    });
   }
});