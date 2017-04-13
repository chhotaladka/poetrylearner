from django import template
from django.template import Node
from django.db.models import Q
import os, sys, traceback
import random
from repository.models import Person

register = template.Library()


class PersonCountNode(Node):
    """
    Render the poets count
    """

    def __init__(self, varname=None,):
        self.varname = varname

    @classmethod
    def handle_token(cls, parser, token):
        """
        Class method to parse and return a Node.
        """
        tokens = token.split_contents()        
        
        if len(tokens) < 3:
            raise template.TemplateSyntaxError, "%s tag takes at least two arguments" % tokens[0]

        # Check the 1st argument
        if tokens[1] == 'as':
            correct_syntax = "'%s as [varname]'" % tokens[0]

            return cls(
                       varname = tokens[2]
                    )
        else:
            raise template.TemplateSyntaxError, "Wrong syntax."
        

    def render(self, context):
        q_objects = Q()
        try:
            context[self.varname] = Person.objects.filter(q_objects).count()
        
        except:
            print ("Error: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno)) 
            raise template.TemplateSyntaxError, "Something went wrong. Check the queryset to resolve the error"            
            
        return ''


@register.tag
def get_poets_count(parser, token):
    """
    Get count of the poets
    
    Syntax::
        case 1: {% get_poets_count as [varname] %}
        
    Example usage::
        {% get_poets_count as count %}
    """     
    
    return PersonCountNode.handle_token(parser, token)


class PersonNode(Node):
    def __init__(self, count=5, order='recent', context_var=None):
        self.count = count
        self.order = order
        self.context_var = context_var

    @classmethod
    def handle_token(cls, parser, token, order='recent'):
        tokens = token.split_contents()
        
        if len(tokens) < 4:
            raise template.TemplateSyntaxError("%s tag takes at least three arguments" % tokens[0])

        # Check the 1st argument
        try:
            count = int(tokens[1])
            if count < 1:
                raise template.TemplateSyntaxError("First argument of %s tag must be a positive integer" % tokens[0])
        except:
            raise template.TemplateSyntaxError("First argument of %s tag must be a positive integer" % tokens[0])
        
        # Check the 2nd argument
        if tokens[2] == 'as':
            correct_syntax = "'%s [count] as [context_var]'" % tokens[0]

            return cls(
                       count = count,
                       order = order,
                       context_var = tokens[3]
                    )
        else:
            raise template.TemplateSyntaxError("Wrong syntax.")
        

    def render(self, context):
        try:
            if self.order == 'random':
                context[self.context_var] = Person.objects.random(self.count)
            else:
                context[self.context_var] = Person.objects.order_by('-date_modified')[:self.count]
        except:
            print ("Error: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno)) 
            raise template.TemplateSyntaxError, "Something went wrong. Check the queryset to resolve the error"            
            
        return ''

@register.tag
def get_person_random(parser, token):
    '''
    @summary: Get the list of persons (random order)
    
    Syntax::
        {% get_person_random [count] as [context_var] %}
        
    Example usage::
        {% get_person_random 5 as person_list %}
    '''
    return PersonNode.handle_token(parser, token, order='random')

@register.tag
def get_person_recent(parser, token):
    '''
    @summary: Get the list of persons (recent modified first)
    
    Syntax::
        {% get_person_recent [count] as [context_var] %}
        
    Example usage::
        {% get_person_recent 5 as person_list %}
    '''
    return PersonNode.handle_token(parser, token, order='recent')