from django import template
from django.template import Node
from django.db.models import Q
import os, sys, traceback
import random
from repository.models import *

register = template.Library()


def _resolve_item_type(item_type):
    '''
    Check the item_type i.e. item_type and retunr the model class and template.
    '''
    item_cls = None
    
    if item_type == Snippet.item_type():
        item_cls = Snippet
        
    elif item_type == Poetry.item_type():
        item_cls = Poetry
        
    elif item_type == Person.item_type():
        item_cls = Person
        
    elif item_type == Place.item_type():
        item_cls = Place
        
    elif item_type == Product.item_type():
        item_cls = Product
        
    elif item_type == Event.item_type():
        item_cls = Event
        
    elif item_type == Organization.item_type():
        item_cls = Organization
        
    elif item_type == Book.item_type():
        item_cls = Book
        
    return item_cls


class ItemCountNode(Node):
    '''
    Render the repository items count
    '''
    def __init__(self, item_class, context_var):
        self.item_class = item_class
        self.context_var = context_var
    
    def render(self, context):
        context[self.context_var] = self.item_class.objects.count()
        return ''


@register.tag
def get_items_count(parser, token):
    """
    Get count of the items of given type
    
    Syntax::
        case 1: {% get_items_count [item_type] as [varname] %}
        
    Example usage::
        {% get_items_count person as count %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes exactly three arguments" % bits[0])

    item_class = _resolve_item_type(bits[1])
    if item_class is None:
        raise template.TemplateSyntaxError("first argument of %s tag must be a repository item type" % bits[0])
    
    if bits[2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    
    return ItemCountNode(item_class, bits[3])


class ItemNode(Node):
    def __init__(self, item_class, count, context_var, order='recent'):
        self.item_class = item_class
        self.count = count
        self.context_var = context_var
        self.order = order

    def render(self, context):
        try:
            if self.order == 'random':
                context[self.context_var] = self.item_class.objects.random(self.count)
            else:
                context[self.context_var] = self.item_class.objects.order_by('-date_modified')[:self.count]
        except:
            print ("Error: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno)) 
            raise template.TemplateSyntaxError("Something went wrong. Check the queryset to resolve the error")
        
        return ''

@register.tag
def get_item_random(parser, token):
    '''
    @summary: Get the list of items of given type (random order)
    
    Syntax::
        {% get_item_random [item_type] [count] as [context_var] %}
        
    Example usage::
        {% get_item_random person 5 as person_list %}
    '''
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes exactly four arguments" % bits[0])

    item_class = _resolve_item_type(bits[1])
    if item_class is None:
        raise template.TemplateSyntaxError("first argument of %s tag must be a repository item type" % bits[0])
    
    try:
        count = int(bits[2])
        if count < 1:
            raise template.TemplateSyntaxError("second argument of %s tag must be a positive integer" % bits[0])
    except:
        raise template.TemplateSyntaxError("second argument of %s tag must be a positive integer" % bits[0])
    
    if bits[3] != 'as':
        raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
    
    return ItemNode(item_class, count, bits[4], order='random')


@register.tag
def get_item_recent(parser, token):
    '''
    @summary: Get the list of items of given type (recent modified first)
    
    Syntax::
        {% get_item_recent [item_type] [count] as [context_var] %}
        
    Example usage::
        {% get_item_recent person 5 as person_list %}
    '''
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes exactly four arguments" % bits[0])

    item_class = _resolve_item_type(bits[1])
    if item_class is None:
        raise template.TemplateSyntaxError("first argument of %s tag must be a repository item type" % bits[0])
    
    try:
        count = int(bits[2])
        if count < 1:
            raise template.TemplateSyntaxError("second argument of %s tag must be a positive integer" % bits[0])
    except:
        raise template.TemplateSyntaxError("second argument of %s tag must be a positive integer" % bits[0])
    
    if bits[3] != 'as':
        raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
    
    return ItemNode(item_class, count, bits[4], order='recent')

