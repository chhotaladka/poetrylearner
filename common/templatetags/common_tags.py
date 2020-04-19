

from django import template
from datetime import date, datetime
from django.utils.timezone import is_aware, utc
from django.utils.translation import pgettext, ugettext as _, ungettext

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
  return list(range(value))

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
  return list(range(value, value+int(arg)))


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


@register.filter
def niceday(value):
    '''
    For date & datetime values, compared to current timestamp returns representing string.
    '''
    if not isinstance(value, date):  # datetime is a subclass of date
        return value
    
    if isinstance(value, datetime):
        now = datetime.now(utc if is_aware(value) else None).date()
        value = value.date()
    else:
        now = datetime.now().date()
        
    delta = now - value
    day_delta = delta.days
    
    if day_delta == 0:
        return "today"
    elif day_delta == 1:
        return "yesterday"
    elif day_delta == -1:
        return "tomorrow"
    elif value.year == now.year:
        return value.strftime("%B %d")
    else:
        return value.strftime("%B %d, %Y")


# Copied from django.contrib.humanize templatetags `naturaltime`
@register.filter
def nicetime(value):
    """
    For datetime values shows how many seconds, minutes or hours ago
    compared to current timestamp returns representing string.
    """
    if not isinstance(value, date):  # datetime is a subclass of date
        return value

    now = datetime.now(utc if is_aware(value) else None)
    if value < now:
        delta = now - value
        if delta.days != 0:
            if delta.days == 1:
                return 'yesterday'
            elif value.year == now.year:
                return value.strftime("%B %d")
            else:
                return value.strftime("%B %d, %Y")
        
        elif delta.seconds == 0:
            return _('now')
        elif delta.seconds < 60:
            return ungettext(
                # Translators: please keep a non-breaking space (U+00A0)
                # between count and time unit.
                'a second ago', '%(count)s seconds ago', delta.seconds
            ) % {'count': delta.seconds}
        elif delta.seconds // 60 < 60:
            count = delta.seconds // 60
            return ungettext(
                # Translators: please keep a non-breaking space (U+00A0)
                # between count and time unit.
                'a minute ago', '%(count)s minutes ago', count
                ) % {'count': count}
        else:
            count = delta.seconds // 60 // 60
            return ungettext(
                # Translators: please keep a non-breaking space (U+00A0)
                # between count and time unit.
                'an hour ago', '%(count)s hours ago', count
                ) % {'count': count}
    else:
        delta = value - now
        if delta.days != 0:
            if delta.days == 1:
                return 'tomorrow'
            elif value.year == now.year:
                return value.strftime("%B %d")
            else:
                return value.strftime("%B %d, %Y")
        elif delta.seconds == 0:
            return _('now')
        elif delta.seconds < 60:
            return ungettext(
                # Translators: please keep a non-breaking space (U+00A0)
                # between count and time unit.
                'a second from now', '%(count)s seconds from now', delta.seconds
            ) % {'count': delta.seconds}
        elif delta.seconds // 60 < 60:
            count = delta.seconds // 60
            return ungettext(
                # Translators: please keep a non-breaking space (U+00A0)
                # between count and time unit.
                'a minute from now', '%(count)s minutes from now', count
            ) % {'count': count}
        else:
            count = delta.seconds // 60 // 60
            return ungettext(
                # Translators: please keep a non-breaking space (U+00A0)
                # between count and time unit.
                'an hour from now', '%(count)s hours from now', count
            ) % {'count': count}