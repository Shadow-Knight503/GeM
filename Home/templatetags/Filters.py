from django import  template

register = template.Library()

# Returns Dictionary Key
@register.filter()
def tnc(val, arg):
    return " ".join(val.split()[: int(arg)]) + "..."

@register.filter()
def inty(val):
    return int(val.split(".")[0].strip("₹").replace(",", ""))

@register.filter()
def prcm(val, arg):
    return abs(int(inty(val)) - int(inty(arg)))
