from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from menu_tree.models import MenuItem

register = template.Library()


@register.inclusion_tag("menu_tree/menu.html", takes_context=True)
def draw_menu(context: RequestContext, menu_title: str) -> RequestContext:
    all_menu_items = MenuItem.objects.filter(menu__title=menu_title)
    main_items = [item for item in all_menu_items.filter(parent=None)]
    selected_item = context.request.path
    have_child = {}
    try:
        current_item = all_menu_items.get(url=selected_item)
        if current_item not in main_items:
            have_child[current_item.title] = current_item.get_parents(current_item.pk)
            results = main_items + [item for item in have_child[current_item.title] if item not in main_items]
        else:
            results = main_items
    except ObjectDoesNotExist:
        results = main_items
    context["menu_items"] = results
    return context
