from django_mobile2 import get_flavour
from django_mobile2.conf import settings


def flavour(request):
    return {
        'flavour': get_flavour(),
    }


def is_mobile(request):
    return {
        'is_mobile': get_flavour() == settings.DEFAULT_MOBILE_FLAVOUR,
    }
