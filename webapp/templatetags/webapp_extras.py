from django import template

register = template.Library()


@register.simple_tag
def multiply(qty, unit_price):
    # you would need to do any localization of the result here
    return qty * unit_price
