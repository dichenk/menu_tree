from django import template
from apps.menu.models import Menu
from django.urls import resolve


register = template.Library()


@register.inclusion_tag("menu/menu.html", takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    path = request.path
    try:
        menu = Menu.objects.prefetch_related("items__parent").get(name=menu_name)
    except Menu.DoesNotExist:
        return {"menu_tree": [], "active_path": []}

    items = menu.items.all()
    item_dict = {item.id: item for item in items}
    for item in items:
        item.url = item.get_absolute_url()
        item.is_active = path == item.url
        item.children_list = []

    tree = []
    for item in items:
        if item.parent_id:
            parent = item_dict[item.parent_id]
            parent.children_list.append(item)
        else:
            tree.append(item)

    active_path = []
    for item in items:
        if item.is_active:
            while item:
                active_path.append(item.id)
                item = item.parent if hasattr(item, 'parent') else None
            break

    return {"menu_tree": tree, "active_path": set(active_path)}
