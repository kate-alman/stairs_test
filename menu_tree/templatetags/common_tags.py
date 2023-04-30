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
    try:
        current_item = all_menu_items.get(url=selected_item)
        parents = [
            parent
            for parent in current_item.get_parents()[::-1]
            if parent not in main_items
        ]

        result_dict = main_items + parents
        if current_item not in main_items:
            result_dict.append(current_item)
    except ObjectDoesNotExist:
        result_dict = main_items

    context["menu_items"] = result_dict
    return context
