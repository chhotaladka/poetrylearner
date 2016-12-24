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