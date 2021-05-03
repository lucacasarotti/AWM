from django.shortcuts import render
from utenti.models import Profile


def nega_accesso_senza_profilo(request):
    """
    Funzione utilizzata dalle view per negare l'accesso agli utenti oauth loggati e sprovvisti di un profilo
    (perchè non hanno completato la registrazione del proprio profilo).

    :param request: request utente.
    :return: render della pagina scelta_profilo_oauth.
    """

    # if request.user.is_authenticated:
    #     try:
    #         Profile.objects.get(user=request.user.id)
    #     except Exception:
    #         return True

    if request.user.is_authenticated:
        profilo = Profile.objects.get(user=request.user.id)
        if len(profilo.indirizzo) == 0:
            return True
    return False


def error_404_view(request, exception):
    return render(request, '404.html', status=404)


def error_500_view(request):
    return render(request, '500.html', status=500)


def error_403_view(request, exception):
    return render(request, '403.html', status=403)

