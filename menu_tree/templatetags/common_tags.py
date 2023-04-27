from django import template

from menu_tree.models import MenuItem

register = template.Library()


@register.inclusion_tag('menu_tree/menu.html', takes_context=True)
def show_menu(context, menu_title):
    # TODO
    context['menu_items'] = MenuItem.objects.filter(menu__title=menu_title)
    return context
