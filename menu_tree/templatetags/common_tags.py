from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from menu_tree.models import MenuItem

register = template.Library()


@register.inclusion_tag("menu_tree/menu.html", takes_context=True)
def draw_menu(context: RequestContext, menu_title: str) -> RequestContext:
    all_menu_items = MenuItem.objects.filter(menu__title=menu_title).select_related("parent")
    main_items = [item for item in all_menu_items.filter(parent=None)]
    selected_item = context.request.path
    try:
        current_item = all_menu_items.get(url=selected_item)
        if current_item not in main_items:
            parents = [
                parent
                for parent in current_item.get_parents(ignored=main_items)[::-1]
            ]
            result_dict = main_items + parents + [current_item]
        else:
            result_dict = main_items
    except ObjectDoesNotExist:
        result_dict = main_items
    context["menu_items"] = result_dict
    return context
