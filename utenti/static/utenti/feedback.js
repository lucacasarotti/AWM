let feedbackList=$('#feedback-list');
let nextPage='';
function drawReview(feedback) {

    let feedbackItem =
        `<div class="media-body">
           `;
    for (let i of Array(5).keys()){
        if (i < feedback.voto) {
           feedbackItem+=`<i class="fas fa-heart fa-lg"  style="color:red"></i>`;
        }
        else {
            feedbackItem+=`<i class="far fa-heart fa-lg" style="color:red"></i>`;
        }
    }
    feedbackItem+=
        `<div class="reviews-members-body">
            <h3><p>${feedback.titolo}</p></h3>
                ${feedback.descrizione}
        </div>
         </div>
        <p class="divider-text"></p>`;

    $(feedbackItem).appendTo('#feedback-list');
}

 $(document).ready(function () {
        var params={};
        params['user_recensito']=user;
        $.ajax({
            'method': 'GET',
            'url': myurl,
            'data': params,
            success: function (data) {
                console.log(data);
            nextPage = data.next;
             for (let i = data['results'].length - 1; i >= 0; i--) {
                drawReview(data['results'][i]);
             }


            },
            error: function () {
                alert('Error Occured');
            }
        });


});


$(feedbackList).on('scroll', function() {


   var scrollTop = $(this).scrollTop();
   if (scrollTop + $(this).innerHeight() >= this.scrollHeight) {
       if (nextPage==null){
           return;
       }
       $.getJSON(nextPage, function (data) {
        nextPage=data.next;
        for (let i = 0; i <data['results'].length; i++) {
              drawReview(data['results'][i]);

        }
    });
   }
});