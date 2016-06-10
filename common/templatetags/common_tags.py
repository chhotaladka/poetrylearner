from __future__ import absolute_import, unicode_literals

from django import template

register = template.Library()

@register.filter
def get_range(value):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range(value)

@register.filter
def make_range(value, arg=1):
  """
    Filter - returns a list containing range made from given value to value+arg
    Usage (in template):

    <ul>{% for i in 3|get_range:"4" %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>3. Do something</li>
      <li>4. Do something</li>
      <li>5. Do something</li>
      <li>6. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range(value, value+int(arg))


@register.filter('has_group')
def has_group(user, groups):
    '''
    Pass comma separated gruop names in filter argument
    
    e.g. {{ user|has_group:"Administrator, Editor" }}
    '''
    if user:       
        group_list = [s for s in groups.split(',')]     
        if user.is_authenticated():
            if bool(user.groups.filter(name__in=group_list)) | user.is_superuser:
                return True
    return False