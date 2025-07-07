from rest_framework.serializers import ValidationError
import re

cuss_words = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
    'ставки',
    'продам',
    'гараж',
]
correct_link = r"^(https?://)?(www\.)?youtube\.com/"


def validate_cuss_words(value):
    if value.lower() in cuss_words:
        raise ValidationError('Использовано матерное слово')


def validate_correct_link(value):
    if value:
        pattern = correct_link
        if not re.match(pattern, value):
            raise ValidationError('Использована ссылка не на youtube.com')
