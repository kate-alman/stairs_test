from django.views.generic import ListView

from menu_tree.models import MenuItem


class MainPageView(ListView):
    model = MenuItem
    template_name = "menu_tree/base.html"
    extra_context = {"title": "Main Page"}
    context_object_name = "items"
