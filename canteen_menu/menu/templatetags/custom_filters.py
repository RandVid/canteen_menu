from django import template

register = template.Library()


@register.filter(name='get_category_name')
def get_category_name(categories, category_id):
    category = categories.filter(id=category_id).first()
    return category['name'] if category else ''
