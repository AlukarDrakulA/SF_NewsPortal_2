from django import template


register = template.Library()

CENSOR_WORDS = ['some']

@register.filter()
def censor(value):

    for i in CENSOR_WORDS:
        if i.find(value):
            value = value.replace(i[1::], "*" * len(i))
    return f'{value}'