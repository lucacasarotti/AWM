let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let messageList = $('#messages');
let nextPage='';
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

function getMessageById(message) {
    id = JSON.parse(message).message;
    console.log(myurl);
    $.getJSON(myurl+`${id}/`, function (data) {
        console.log(data);
        drawMessage(data);
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });
}

function sendMessage(recipient, body) {

    $.post(myurl, {
        recipient: recipient,
        body: body
    }).fail(function () {
        alert('Error! Check console!');
    });
}



$(document).ready(function () {

    var socket = new WebSocket(
        'ws://' + window.location.host + '/ws'+window.location.pathname);
    console.log(socket);
    var params={};
    params['target']=currentRecipient;
    console.log(params);
    console.log(myurl);
    $.ajax({
            'method': 'GET',
            'url': myurl,
            'data': params,
            success: function (data) {
                 nextPage=data.next;
                console.log(data);

                messageList.children('.message').remove();
                for (let i = data['results'].length - 1; i >= 0; i--) {
                    drawMessage(data['results'][i]);
                 }
                messageList.animate({scrollTop: messageList.prop('scrollHeight')});
            },
            error: function (e) {
                console.log(e);
                alert('Error Occured');
            }
        });
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
        console.log(e.data);
        getMessageById(e.data);
    };
});


$(messageList).on('scroll', function() {

   if (messageList.scrollTop()==0) {
       if (nextPage==null){
           return
       }
       var lastMsg = $('#messages:last-child');
       $.getJSON(nextPage, function (data) {
        console.log(data);

        nextPage=data.next;

        for (let i = 0; i <data['results'].length; i++) {
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