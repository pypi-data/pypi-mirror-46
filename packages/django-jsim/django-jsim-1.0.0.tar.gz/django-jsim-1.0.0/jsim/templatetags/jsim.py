from django import template
from django.core.paginator import Paginator

register = template.Library()

@register.inclusion_tag('jsim/jsim.html')
def jsim():
    return {}

# @register.simple_tag(takes_context=True)
# def eget(context, show, shell, callback='', callback_error=''):
    # lst = show.split(maxsplit=1)
# 
    # url = '{% url ' + "'%s' " % lst[0] + lst[1] + ' %}'
# 
    # tmp = """
    # data-show="%s"
    # data-shell="%s" 
    # data-callback="%s" data-callback-error="%s"
    # """ % (url, '#%s' % shell, callback, callback_error)
# 
    # tmp = template.Template(tmp)
    # return tmp.render(context)
# 
# @register.simple_tag(takes_context=True)
# def epost(context, show, shell, form='', callback='', callback_error=''):
    # lst = show.split(maxsplit=1)
# 
    # url = '{% url ' + "'%s' " % lst[0] + lst[1] + ' %}'
# 
    # tmp = """
    # data-show="%s"
    # data-shell="%s" 
    # data-form="%s"
    # data-callback="%s" data-callback-error="%s"
    # """ % (url, '#%s' % shell, callback, callback_error, form)
# 
    # tmp = template.Template(tmp)
    # return tmp.render(context)
# 
# 
# 


