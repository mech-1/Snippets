from django import template
from MainApp.models import LANG_ICONS
register = template.Library()

def icon_class(value):
    """
    Возвращает класс иконки fontawesome
    """
    return LANG_ICONS.get(value)

# {{ lang | icon_class }}

register.filter('icon_class', icon_class)