import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _('Password harus minimal 8 karakter.'),
                code='password_too_short',
            )
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _('Password harus mengandung minimal satu huruf besar.'),
                code='password_no_upper',
            )
        
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _('Password harus mengandung minimal satu huruf kecil.'),
                code='password_no_lower',
            )
        
        if not re.search(r'\d', password):
            raise ValidationError(
                _('Password harus mengandung minimal satu angka.'),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            'Password harus minimal 8 karakter dengan huruf besar, huruf kecil, dan angka.'
        )