from django import template
from django.db import connection

from menu.models import MenuItem

register = template.Library()


@register.simple_tag
def draw_menu(menu_name, current_url):
    query = f'''
        WITH RECURSIVE menu_items AS (
            SELECT
                id,
                text,
                url,
                named_url,
                parent_id
            FROM
                menu_menuitem
            WHERE
                menu_name = '{menu_name}' AND parent_id IS NULL
            UNION ALL
            SELECT
                child.id,
                child.text,
                child.url,
                child.named_url,
                child.parent_id
            FROM
                menu_menuitem child
            INNER JOIN
                menu_items parent
            ON
                parent.id = child.parent_id
        )
        SELECT
            id,
            text,
            url,
            named_url,
            parent_id
        FROM
            menu_items;
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    def render_menu_items(menu_items, parent_id=None):
        menu_html = "<ul>"
        for item in menu_items:
            if item[4] == parent_id:
                is_active = current_url == (item[2] if item[2] else item[3])
                menu_html += f'<li>'
                menu_html += f'<a href="{item[2] if item[2] else item[3]}" {"class=active" if is_active else ""}>{item[1]}</a>'
                menu_html += render_menu_items(menu_items, parent_id=item[0])
                menu_html += '</li>'
        menu_html += "</ul>"
        return menu_html

    return render_menu_items(results)


# @register.simple_tag
# def draw_menu(menu_name, parent=None):
#
#     menu_items = MenuItem.objects.filter(menu_name=menu_name, parent=parent).prefetch_related('children')
#
#     def render_menu_items(menu_items):
#         if not menu_items:
#             return ""
#
#         menu_html = "<ul>"
#         for item in menu_items:
#             menu_html += f'<li><a href="{item.get_url()}">{item.text}</a>'
#             if item.children.all():
#                 menu_html += draw_menu(menu_name, parent=item)
#             menu_html += '</li>'
#         menu_html += "</ul>"
#         return menu_html
#
#     return render_menu_items(menu_items)
