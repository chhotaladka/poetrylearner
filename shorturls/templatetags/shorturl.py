import urllib.parse
from django import template
from django.conf import settings
from django.urls import reverse, NoReverseMatch
from django.utils.safestring import mark_safe
from shorturls import default_converter as converter

class ShortURL(template.Node):
    @classmethod
    def parse(cls, parser, token):
        parts = token.split_contents()
        if len(parts) == 2:
            return cls(template.Variable(parts[1]))
        elif len(parts) == 4 and parts[2] == 'as':
            return cls(template.Variable(parts[1]),
                       parts[3])
        else:
            correct_syntax = "1) '%s [obj]'  OR 2) '%s [obj] as [context_var]'" % (parts[0], parts[0])
            raise template.TemplateSyntaxError("Correct syntax: %s" % correct_syntax)
        
    def __init__(self, obj=None, context_var=None):
        self.obj = obj
        self.varname = context_var
        
    def render(self, context):
        try:
            obj = self.obj.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        
        try:
            prefix = self.get_prefix(obj)
        except (AttributeError, KeyError):
            return ''
        
        tinyid = converter.from_decimal(obj.pk)
        
        if hasattr(settings, 'SHORT_BASE_URL') and settings.SHORT_BASE_URL:
            short_url = urllib.parse.urljoin(settings.SHORT_BASE_URL, prefix+tinyid)
            if self.varname:
                context[self.varname] = short_url
                return ''
            else:
                return short_url
            
        try:
            short_url = reverse('shorturls:redirect', kwargs = {
                'prefix': prefix,
                'tiny': tinyid
            })
            if self.varname:
                context[self.varname] = short_url
                return ''
            else:
                return short_url
        except NoReverseMatch:
            return ''
            
    def get_prefix(self, model):
        if not hasattr(self.__class__, '_prefixmap'):
            self.__class__._prefixmap = dict((m,p) for p,m in list(settings.SHORTEN_MODELS.items()))
        key = '%s.%s' % (model._meta.app_label, model.__class__.__name__.lower())
        return self.__class__._prefixmap[key]
        
class RevCanonical(ShortURL):
    def render(self, context):
        url = super(RevCanonical, self).render(context)
        if url:
            return mark_safe('<link rev="canonical" href="%s">' % url)
        else:
            return ''

register = template.Library()
register.tag('shorturl', ShortURL.parse)
register.tag('revcanonical', RevCanonical.parse)