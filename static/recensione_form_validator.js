jQuery.validator.setDefaults({
    success: "valid"
});

$( "#recensione-form" ).validate({
    rules: {
        'titolo':{
            required: true,
            maxlength: 95
        },
        'descrizione':{
            required: true,
            maxlength: 245
        }
    },
    messages:
    {
        'titolo':{
            required: "Il campo titolo è obbligatorio",
            maxlength: "Limite di 95 caratteri superato"
        },
        'descrizione':{
            required: "Il campo descrizione è obbligatorio",
            maxlength: "Limite di 245 caratteri superato"
        }
    }
});
