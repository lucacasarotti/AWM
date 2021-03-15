from django.contrib import admin
from .models import Invito


class InvitoAdmin(admin.ModelAdmin):
    filter_horizontal = ('partecipanti', )


admin.site.register(Invito, InvitoAdmin)
