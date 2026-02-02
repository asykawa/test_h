from .models import Property
from modeltranslation.translator import TranslationOptions,register

@register(Property)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'region', 'city')