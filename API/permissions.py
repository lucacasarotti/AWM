from rest_framework import permissions


class IsSameAnagraficaUserOrReadOnly(permissions.BasePermission):
    """
    update e delete concessi solo ai proprietari dei dati loggati.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsSameUserOrReadOnly(permissions.BasePermission):
    """
    update e delete concessi solo ai proprietari dei dati loggati.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user.id == request.user.id


class IsRecensionePossessorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_recensore == request.user


class IsUserLogged(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    update e delete concessi solo ai creatori degli inviti.
    """
    def has_object_permission(self, request, view, obj):
        # permesso a tutti il get
        if request.method in permissions.SAFE_METHODS:
            return True
        # tutti gli altri metodi solo se creator
        return obj.utente == request.user


class IsCompatibleUser(permissions.BasePermission):
    '''
    Controllo che la persona che vuole partecipare all'invito non sia già iscritto e non sia il proprietario
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # ammesso solo metodo PATCH per utenti diversi dal creatore
        if request.method == 'PATCH' and request.user != obj.utente:
            # per partecipare ci devono essere posti rimasti e l'utente non deve essere già tra i partecipanti
            if obj.posti_rimasti > 0 and request.user not in obj.partecipanti.all():
                return True

            # per disiscriversi l'utente deve essere già tra i partecipanti
            if request.user in obj.partecipanti.all():
                return True

        return False
