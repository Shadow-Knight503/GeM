from django import  template

register = template.Library()

# Returns Dictionary Key
@register.filter()
def key(val):
    return "Hello World"