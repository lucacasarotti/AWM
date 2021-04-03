jQuery.validator.setDefaults({
    success: "valid"
});

jQuery.validator.addMethod("cinema",function(value, element){
  var reg = /[A-Za-z0-9 ]+( \([A-Za-z]+\))$/;
  return this.optional(element) || reg.test(value);
}, "Mantieni il formato: Nome del cinema (Città)");

jQuery.validator.addMethod("safeString",function(value, element){
  var reg = /\w+$/;
  return this.optional(element) || reg.test(value);
}, "Attenzione ai caratteri");



jQuery.validator.addMethod("notInThePast", function(value, element) {
    return this.optional(element) || moment(value,"DD/MM/YYYY") > moment();
}, "Viaggi nel tempo per caso?");

$.validator.addMethod('lowStrict', function (value, el, param) {
    return value < param;
});

$( "#invito-form" ).validate({
    rules: {
        'tipologia':{
            required: true,
        },
        'cinema':{
            required: true,
            maxlength: 95,
            cinema: true,
        },
        'film': {
            required: true,
            maxlength: 95,
            safeString: true,
        },
        'data': {
            required: true,
            notInThePast: true,
        },
        'orario': {
            required: true,
        },
        'limite_persone': {
            required: true,
            number: true,
            lowStrict: 25,
        },
        'commento': {
            maxlength: 245,
        },
    },
    messages:
    {
        'tipologia':{
            required: "Il campo tipologia è obbligatorio",
        },
        'cinema':{
            required: "Il campo cinema è obbligatorio",
            maxlength: "Limite di 95 caratteri superato"
        },

        'film': {
            required: "Il campo film è obbligatorio",
            maxlength: "Limite di 95 caratteri superato"
        },
        'data': {
            required: "Il campo data è obbligatorio",
        },
        'orario': {
            required: "Il campo orario è obbligatorio",
        },
        'limite_persone': {
            required: "Il campo limite_persone è obbligatorio",
            number: "Inserire un numero valido",
            lowStrict: "Limite superato",
        },
        'commento': {
            maxlength: "Limite di 245 caratteri superato",
        },
    }
});