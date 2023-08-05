"""Greek-specific forms helpers."""
import datetime
import re

from django.core.validators import EMPTY_VALUES
from django.forms import Field, RegexField, ValidationError
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from stdnum import luhn


class GRPostalCodeField(RegexField):
    """
    Greek Postal code field.

    Format: XXXXX, where X is any digit, and first digit is not 0 or 9.
    """

    default_error_messages = {
        'invalid': _('Enter a valid 5-digit greek postal code.'),
    }

    def __init__(self, *args, **kwargs):
        super(GRPostalCodeField, self).__init__(r'^[12345678]\d{4}$', *args, **kwargs)


class GRTaxNumberCodeField(Field):
    """
    Greek tax number field.

    The allow_test_value option can be used to enable the usage of the
    non valid 000000000 value for testing and development
    """

    default_error_messages = {
        'invalid': _('Enter a valid greek tax number (9 digits).'),
    }

    def __init__(self, allow_test_value=False, *args, **kwargs):
        self.allow_test_value = allow_test_value
        super(GRTaxNumberCodeField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(GRTaxNumberCodeField, self).clean(value)
        if value in EMPTY_VALUES:
            return ''

        val = re.sub('[\-\s\(\)]', '', force_text(value))
        if(len(val) < 9):
            raise ValidationError(self.error_messages['invalid'])
        if not all(char.isdigit() for char in val):
            raise ValidationError(self.error_messages['invalid'])
        if not self.allow_test_value and val == '000000000':
            raise ValidationError(self.error_messages['invalid'])
        digits = list(map(int, val))
        digits1 = digits[:-1]
        digits1.reverse()
        check = digits[-1]
        mod = sum([d * pow(2, i + 1) for i, d in enumerate(digits1)]) % 11
        if mod == 10:
            mod = 0
        if mod != check:
            raise ValidationError(self.error_messages['invalid'])
        return val


class GRSocialSecurityNumberCodeField(RegexField):
    """
    Greek social security number (AMKA) field.

    The allow_test_value option can be used to enable the usage of the
    non valid 00000000000 (11 zeros) value for testing and development
    """

    default_error_messages = {
        'invalid': _('Enter a valid greek social security number (AMKA - 11 digits).'),
    }

    def __init__(self, allow_test_value=False, *args, **kwargs):
        self.allow_test_value = allow_test_value
        super(GRSocialSecurityNumberCodeField, self).__init__(r'^[0-9\s\-]+$', *args, **kwargs)

    def check_date(self, val):
        try:
            datetime.datetime.strptime(val[:6], '%d%m%y')
        except:
            raise ValidationError(self.error_messages['invalid'])

    def clean(self, value):
        super(GRSocialSecurityNumberCodeField, self).clean(value)
        if value in self.empty_values:
            return self.empty_value
        val = re.sub('[\-\s]', '', force_text(value))
        if not val or len(val) < 11:
            raise ValidationError(self.error_messages['invalid'])
        if self.allow_test_value and val == '00000000000':
            return val
        if not all(char.isdigit() for char in val):
            raise ValidationError(self.error_messages['invalid'])

        self.check_date(val)
        if not luhn.is_valid(val):
            raise ValidationError(self.error_messages['invalid'])

        return val
