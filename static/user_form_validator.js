$.validator.methods.email = function( value, element ) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return this.optional( element ) || emailReg.test( value );
};

jQuery.validator.setDefaults({
    success: 'valid'
});

jQuery.validator.addMethod("lettersonly", function(value, element) {
    return this.optional(element) || /^[a-z\s]+$/i.test(value);
}, "Caratteri numerici non ammessi");

jQuery.validator.addMethod("username_unique", function(value) {
    var isSuccess = false;

    $.ajax({ url: "/utenti/check_username",
        type: "GET",
        data: "username=" + value,
        async: false,
        dataType:"html",
        success: function(msg) { isSuccess = msg === "True" }
    });
    return isSuccess;
}, "Username non disponibile");

jQuery.validator.addMethod("date",function(value,element){

  var reg = /(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d/;
  return this.optional(element) || reg.test(value);
},"Formato data non corretto");


$( '#user-form' ).validate({
    rules: {
        'username':{
            required: true,
            minlength: 3,
            maxlength: 30,
            username_unique: true
        },
        'email':{
            required: true,
            email: true,
            minlength: 5,
            maxlength: 50
        },
        'password':{
            required: true,
            minlength: 4,
            maxlength: 20
        },
        'conferma_password':{
            equalTo: '#password',
            minlength: 4,
            maxlength: 20
        },
        'first_name': {
            required: true,
            lettersonly: true,
            maxlength: 30
        },
        'last_name':{
            required: true,
            lettersonly: true,
            maxlength: 30
        },
        'indirizzo': {
            required: true,
            minlength: 3,
            maxlength: 50
        },
        'citta':{
            required: true,
            lettersonly: true,
            minlength: 3,
            maxlength: 50
        },
        'telefono':{
            required: true,
            number: true,
            minlength: 3,
            maxlength: 30
        },
        'data_nascita':{
            required: true,
            date: true,
        },
        'posti_macchina':{
            number:true,
            min:0,
            max:8
        }
    },
    messages:
    {
        'username':{
            required: "Il campo username è obbligatorio",
            minlength: "Scegli un username di almeno 3 lettere",
            maxlength: "Limite di 30 caratteri superato"
            },
        'email':{
            required: "Il campo email è obbligatorio",
            email: "Inserisci un valido indirizzo email",
            minlength: "Limite minimo di 5 carattere",
            maxlength: "Limite di 50 caratteri superato"
            },
        'password':{
            required: "Il campo password è obbligatorio",
            minlength: "Inserisci una password di almeno 4 caratteri",
            maxlength: "Limite di 20 caratteri superato"
            },
        'conferma_password':{
            equalTo: "Le due password non coincidono",
            minlength: "Inserisci una password di almeno 4 caratteri",
            maxlength: "Limite di 20 caratteri superato"
            },
        'first_name': {
            required: "Il campo nome è obbligatorio",
            notNumber: "Caratteri numerici non consentiti",
            maxlength: "Limite di 30 caratteri superato"
          },
        'last_name':{
            required: "Il campo cognome è obbligatorio",
            maxlength: "Limite di 30 caratteri superato"
          },
        'indirizzo': {
            required: "Il campo indirizzo è obbligatorio",
            minlength: "Limite minimo di 3 caratteri",
            maxlength: "Limite di 50 caratteri superato"
          },
        'citta':{
            required: "Il campo citta è obbligatorio",
            minlength: "Limite minimo di 3 caratteri",
            maxlength: "Limite di 50 caratteri superato"
         },
        'telefono':{
            required: "Il campo telefono è obbligatorio",
            number: "Inserisci un numero valido",
            minlength: "Limite minimo di 3 caratteri",
            maxlength: "Limite di 30 caratteri superato"
         },
        'data_nascita':{
            required: "Il campo data nascita è obbligatorio",
            date: "Inserisci una data in formato dd/mm/YYYY"
        },
        'posti_macchina':{
            number: "Inserisci un numero valido",
            min: "Devi inserire un numero maggiore o uguale a 0",
            max:"Devi inserire un numero minore o uguale a 8"

        }
    }
});
