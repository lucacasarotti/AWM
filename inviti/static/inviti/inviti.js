let url='.';

function getItem(val){
    let tipo;
    switch (val.tipologia) {
        case "Prime Video": tipo = "prime"; break;
        case "Disney+": tipo = "disney"; break;
        default: tipo = val.tipologia.toLowerCase();
    }
    var generi_html = '';
    for (let i=0;i<val.genere.length;i++){
        generi_html = generi_html+`
            <a href="/inviti/genere/${val.genere[i]}" style="" class="invito-item__cta" id="${tipo}-cta">${val.genere[i]}</a>`;
    }
    var div_html = '';
    var data_html = '';
    if (val.scaduto) {
        div_html = `<div class="invito-item" style="background: rgba(255,0,0,0.18);">`;
        data_html = `<span style="color: red; font-weight: bold">${val.data} - SCADUTO</span>`;
    } else {
        div_html = `<div class="invito-item">`;
        data_html = `<span>${val.data}</span>`;
    }

    return `
            ${div_html}
            <div class="invito-item__img" id="${tipo}-logo">
                <img src="../../static/images/${tipo}_logo.png" alt="">
            </div>
            <div class="invito-item__info">
                <div class="invito-item__user">
                    <a href="/utenti/profilo/${val.utente.id}">${val.utente.username}</a>
                </div>
                <div class="invito-item__date">
                    ${data_html}
                    <span>${val.orario} - ${val.tipologia}</span>
                </div>
                <a href="/inviti/invito/${val.id}"><h1 class="invito-item__title">${val.film}</h1></a>
                <p class="invito-item__text">Posti Rimasti: ${val.posti_rimasti}</p>
                ${generi_html}
                </div></div>
    `;
}

$(document).ready(function() {
    var params= {};
    var prev = 0;
    var page = 1;
    var next = 2;
    $('#pp').hide();
    if(num_pages===1) {
        $('#fp').hide();
        $('#np').hide();
        $('#lp').hide();
    }

    if(typeof generi !== 'undefined'){
        if(generi.length >= 1 && generi[0] !== ""){
            for(var i=0; i<generi.length; i++){
                var g = generi[i];
                $('#'+g).toggleClass('genere-filter-active');
                params[g] = true;
            }
        }
        params['page_no'] = 1;
        //INITIAL GET
    $.ajax({
        'method': 'GET',
        'url': url,
        'data': params,
        success: function(response) {
            prev = response.resources.previous_page; //get prev and next page
            next = response.resources.next_page;
            num_pages = response.resources.pages;
            $('#prev').attr("data-value", prev);
            $('#next').attr("data-value", next);
            if(num_pages===1) $('#fp').hide(); else $('#fp').show();
            if(prev == null) $('#pp').hide(); else $('#pp').show();
            if(next == null) $('#np').hide(); else $('#np').show();

            $('#my-placeholder').html('');
            //$('#my-placeholder').load('inviti/invito_list_serialized.html', {inviti: response.resources.data});
            $.each(response.resources.data, function(i, val) {
            $('#my-placeholder').append(getItem(val));
           });
            $(window).scrollTop(0);

        },
        error: function () {
            alert('Error Occured');
        }
    });
    }

    //CHANGE PAGE
    $('.page-cursor').click(function(event){
        event.preventDefault();
        params['page_no'] = $(this).attr('data-value');
        if(typeof passed_url !== 'undefined'){
            url = passed_url;
        }
        $.ajax({
            'method': 'GET',
            'url': url,
            'data': params,
            success: function (response) {
                prev = response.resources.previous_page; //get prev and next page
                next = response.resources.next_page;
                num_pages = response.resources.pages;
                $('#prev').attr("data-value", prev);
                $('#next').attr("data-value", next);
                if(num_pages===1) $('#fp').hide(); else $('#fp').show();
                if(prev == null) $('#pp').hide(); else $('#pp').show();
                if(next == null) $('#np').hide(); else $('#np').show();

                page = params['page_no'];

                $('#my-placeholder').html('');
                $.each(response.resources.data, function(i, val) {
                 //append to post
                $('#my-placeholder').append(getItem(val))
               });
                $(window).scrollTop(0);
            },
            error: function () {
                alert('Error Occured');
            }
        });
    });
    $('.genere').click(function(event){
        event.preventDefault();
        params['page_no'] = 1;

        $(this).toggleClass('genere-filter-active');
        if($(this).hasClass('genere-filter-active')) {
            params[this.id] = true;
        } else {
            params[this.id] = false;
        }
        $.ajax({
            'method': 'GET',
            'url': url,
            'data': params,
            success: function(response) {
                prev = response.resources.previous_page; //get prev and next page
                next = response.resources.next_page;
                num_pages = response.resources.pages;
                $('#prev').attr("data-value", prev);
                $('#next').attr("data-value", next);
                if(num_pages===1) $('#fp').hide(); else $('#fp').show();
                if(prev == null) $('#pp').hide(); else $('#pp').show();
                if(next == null) $('#np').hide(); else $('#np').show();

                $('#my-placeholder').html('');
                //$('#my-placeholder').load('inviti/invito_list_serialized.html', {inviti: response.resources.data});
                $.each(response.resources.data, function(i, val) {
                $('#my-placeholder').append(getItem(val));
               });
                $(window).scrollTop(0);

            },
            error: function () {
                alert('Error Occured');
            }
        });

    })
});