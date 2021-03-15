from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_date(date):
    if date < timezone.now().date():
        raise ValidationError(
            _('%(value)s deve essere una data futura'),
            params={'value': date},
        )