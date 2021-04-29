from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_date(date):
    if date < timezone.now().date():
        raise ValidationError(
            _('Viaggi nel tempo per caso?'),
            params={'value': date},
        )
