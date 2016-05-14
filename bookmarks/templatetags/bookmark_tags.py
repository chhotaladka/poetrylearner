from django import template
from bookmarks.models import Bookmark

register = template.Library()


class BookmarkByUserNode(template.Node):
    def __init__(self, user, object, context_var):
        self.user = user
        self.object = object
        self.context_var = context_var

    def render(self, context):
        try:
            user = template.resolve_variable(self.user, context)
            object = template.resolve_variable(self.object, context)
        except template.VariableDoesNotExist:
            return ''
        context[self.context_var] = Bookmark.objects.get_for_user(object, user)
        return ''


class BookmarksByUserNode(template.Node):
    def __init__(self, user, context_var):
        self.user = user
        self.context_var = context_var

    def render(self, context):
        try:
            user = template.resolve_variable(self.user, context)
        except template.VariableDoesNotExist:
            return ''
        context[self.context_var] = Bookmark.objects.get_all_for_user(user)
        return ''


def do_bookmark_by_user(parser, token):
    '''
    Retrieves the ``Bookmark`` made by a user on a particular object and
    stores it in a context variable. If the user has not bookmarked, the
    context variable will be ``None``.
    
    Example usage::    
        {% bookmark_by_user user on object as bookmark %}
        
    '''
    bits = token.contents.split()
    if len(bits) != 6:
        raise template.TemplateSyntaxError("'%s' tag takes exactly five arguments" % bits[0])
    if bits[2] != 'on':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'on'" % bits[0])
    if bits[4] != 'as':
        raise template.TemplateSyntaxError("fourth argument to '%s' tag must be 'as'" % bits[0])    
    return BookmarkByUserNode(bits[1], bits[3], bits[5])


def do_bookmarks_by_user(parser, token):
    """
    Retrieves all bookmarks made by a user and stores it in a context
    variable.
    
    Example usage::
        {% bookmarks_by_user user as bookmarks %}
        
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes exactly three arguments" % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return BookmarksByUserNode(bits[1], bits[3])


register.tag('bookmark_by_user', do_bookmark_by_user)
register.tag('bookmarks_by_user', do_bookmarks_by_user)