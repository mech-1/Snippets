from django import template
from MainApp.models import LANG_ICONS
register = template.Library()

def icon_class(value):
    """
    Возвращает класс иконки fontawesome
    """
    return LANG_ICONS.get(value)
def message_mapping(origin_class):
    mapping = {
        'error': 'danger',
        'debug': 'light',
    }
    return mapping.get(origin_class, origin_class)
# {{ lang | icon_class }}

register.filter('icon_class', icon_class)
register.filter('message_mapping', message_mapping)