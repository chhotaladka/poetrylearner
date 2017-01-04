from django import template
from django.template import Node
from django.db.models import Q
import os, sys, traceback
import random
from repository.models import Poetry

register = template.Library()

# Flags
_PUBLISHED = 1
_UNPUBLISHED = 2

class RecentPoetryNode(Node):
    """
    Render the recent poetry list
    """

    def __init__(self, count=5, varname=None, creator=None, language=None, tag=None):
        self.count = count
        self.varname = varname
        self.creator = template.Variable(creator) if creator else None
        self.language = language
        self.tag = tag              

    @classmethod
    def handle_token(cls, parser, token):
        """
        Class method to parse and return a Node.
        """
        tokens = token.split_contents()        
        
        if len(tokens) < 4:
            raise template.TemplateSyntaxError, "%s tag takes at least three arguments" % tokens[0]

        # Check the 1st argument
        try:
            count = int(tokens[1])
            if count < 1:
                raise template.TemplateSyntaxError, "First argument of %s tag must be a positive integer" % tokens[0]
        except:
            raise template.TemplateSyntaxError, "First argument of %s tag must be a positive integer" % tokens[0]
        
        # Check the 2nd argument
        if tokens[2] == 'as':
            correct_syntax = "'%s [count] as [varname]'" % tokens[0]

            return cls(
                       count=count, 
                       varname = tokens[3]
                    )
            
        elif tokens[2] == 'by':            
            correct_syntax = "'%s [count] by [Person object] as [varname]'" % tokens[0]
            if len(tokens) < 6:
                raise template.TemplateSyntaxError, "Number of arguments are less. Correct syntax is " + correct_syntax
            
            if tokens[4] != 'as':
                raise template.TemplateSyntaxError, "Forth argument must be 'as'. Correct syntax is " + correct_syntax

            return cls(
                       count=count, 
                       varname = tokens[5],
                       creator = tokens[3]
                    )
    
        elif tokens[2] == 'in':
            correct_syntax = "'%s [count] in [language] as [varname]'" % tokens[0]
            if len(tokens) < 6:
                raise template.TemplateSyntaxError, "Number of arguments are less. Correct syntax is " + correct_syntax
            
            if tokens[4] != 'as':
                raise template.TemplateSyntaxError, "Forth argument must be 'as'. Correct syntax is " + correct_syntax

            return cls(
                       count=count, 
                       varname = tokens[5],
                       language = tokens[3]
                    )
                    
        elif tokens[2] == 'has':
            correct_syntax = "'%s [count] has [tag] as [varname]'" % tokens[0]
            if len(tokens) < 6:
                raise template.TemplateSyntaxError, "Number of arguments are less. Correct syntax is " + correct_syntax
            
            if tokens[4] != 'as':
                raise template.TemplateSyntaxError, "Forth argument must be 'as'. Correct syntax is " + correct_syntax
  
            return cls(
                       count=count, 
                       varname = tokens[5],
                       tag = tokens[3]
                    )                
        else:
            raise template.TemplateSyntaxError, "Wrong syntax."
        

    def render(self, context):
        q_objects = Q()
        try:
            # poetries which are published
            q_objects &= Q(date_published__isnull=False)
            
            if self.creator:
                creator = self.creator.resolve(context)
                q_objects &= Q(creator_id=creator.id)
            
            if self.language:
                q_objects &= Q(language=self.language)
                
            if self.tag:
                q_objects &= Q(keywords__slug=self.tag)
                                
            context[self.varname] = Poetry.objects.filter(q_objects).order_by('-date_modified')[:self.count]
        
        except:
            print ("Error: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno)) 
            raise template.TemplateSyntaxError, "Something went wrong. Check the queryset to resolve the error"            
            
        return ''


class SimilarPoetryNode(Node):
    """
    Render the similar poetry list
    """

    def __init__(self, count=5, varname=None, poetry=None):
        self.count = count
        self.varname = varname
        self.poetry = template.Variable(poetry) if poetry else None

    @classmethod
    def handle_token(cls, parser, token):
        """
        Class method to parse and return a Node.
        """
        tokens = token.split_contents()        
        
        if len(tokens) < 6:
            raise template.TemplateSyntaxError, "%s tag takes at least three arguments" % tokens[0]

        # Check the 1st argument
        try:
            count = int(tokens[1])
            if count < 1:
                raise template.TemplateSyntaxError, "First argument of %s tag must be a positive integer" % tokens[0]
        except:
            raise template.TemplateSyntaxError, "First argument of %s tag must be a positive integer" % tokens[0]
                
        # Check the 2nd argument
        if tokens[2] != 'like':
            correct_syntax = "'%s [count] like [Poetry object] as [varname]'" % tokens[0]
            raise template.TemplateSyntaxError, "Second argument must be 'like'. Correct syntax is " + correct_syntax
        
        # Check the 4th argument
        if tokens[4] != 'as':
            correct_syntax = "'%s [count] like [Poetry object] as [varname]'" % tokens[0]
            raise template.TemplateSyntaxError, "Forth argument must be 'as'. Correct syntax is " + correct_syntax
            
        return cls(
                   count=count, 
                   varname = tokens[5],
                   poetry = tokens[3]
                )
        

    def render(self, context):
        try:
            poetry = self.poetry.resolve(context)                            
            context[self.varname] = poetry.keywords.similar_objects()[:self.count]
    
        except:
            print ("Error: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno)) 
            raise template.TemplateSyntaxError, "Something went wrong. Check the queryset to resolve the error"            
            
        return ''


class PoetryCountNode(Node):
    """
    Render the poetry count
    """

    def __init__(self, varname=None, creator=None, language=None, tag=None, published=False):
        self.varname = varname
        self.creator = template.Variable(creator) if creator else None
        self.language = language
        self.tag = tag
        self.published = published             

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
            
        elif tokens[1] == 'by':
            correct_syntax = "'%s by [Person object] as [varname]'" % tokens[0]
            if len(tokens) < 5:
                raise template.TemplateSyntaxError, "Number of arguments are less. Correct syntax is " + correct_syntax
            
            if len(tokens) == 5:
                if tokens[3] != 'as':
                    raise template.TemplateSyntaxError, "Third argument must be 'as'. Correct syntax is " + correct_syntax
                return cls(
                           varname = tokens[4],
                           creator = tokens[2]
                        )
                
            elif len(tokens) == 6:
                if tokens[4] != 'as':
                    correct_syntax = "'%s by [Person object] published/unpublished as [varname]'" % tokens[0]
                    raise template.TemplateSyntaxError, "Fourth argument must be 'as'. Correct syntax is " + correct_syntax
                if tokens[3] == 'published':
                        return cls(
                           varname = tokens[5],
                           creator = tokens[2],
                           published = _PUBLISHED
                        )
                else:
                        return cls(
                           varname = tokens[5],
                           creator = tokens[2],
                           published = _UNPUBLISHED
                        )
    
        elif tokens[1] == 'in':
            correct_syntax = "'%s in [language] as [varname]'" % tokens[0]
            if len(tokens) < 5:
                raise template.TemplateSyntaxError, "Number of arguments are less. Correct syntax is " + correct_syntax
            
            if tokens[3] != 'as':
                raise template.TemplateSyntaxError, "Third argument must be 'as'. Correct syntax is " + correct_syntax

            return cls( 
                       varname = tokens[4],
                       language = tokens[2]
                    )
                    
        elif tokens[1] == 'has':
            correct_syntax = "'%s has [tag] as [varname]'" % tokens[0]
            if len(tokens) < 5:
                raise template.TemplateSyntaxError, "Number of arguments are less. Correct syntax is " + correct_syntax
            
            if tokens[3] != 'as':
                raise template.TemplateSyntaxError, "Third argument must be 'as'. Correct syntax is " + correct_syntax
  
            return cls(
                       varname = tokens[4],
                       tag = tokens[2]
                    )
                
        elif tokens[1] == 'published':
            correct_syntax = "'%s published as [varname]'" % tokens[0]
            if len(tokens) < 4:
                raise template.TemplateSyntaxError("Number of arguments are less. Correct syntax is " + correct_syntax)
            
            if tokens[2] != 'as':
                raise template.TemplateSyntaxError("Second argument must be 'as'. Correct syntax is " + correct_syntax)

            return cls(
                       varname = tokens[3],
                       published = _PUBLISHED
                    )

        elif tokens[1] == 'unpublished':
            correct_syntax = "'%s unpublished as [varname]'" % tokens[0]
            if len(tokens) < 4:
                raise template.TemplateSyntaxError("Number of arguments are less. Correct syntax is " + correct_syntax)
            
            if tokens[2] != 'as':
                raise template.TemplateSyntaxError("Second argument must be 'as'. Correct syntax is " + correct_syntax)

            return cls(
                       varname = tokens[3],
                       published = _UNPUBLISHED
                    )            
        else:
            raise template.TemplateSyntaxError, "Wrong syntax."
        

    def render(self, context):
        q_objects = Q()
        try:                        
            if self.creator:
                creator = self.creator.resolve(context)
                q_objects &= Q(creator_id=creator.id)
            
            if self.language:
                q_objects &= Q(language=self.language)
            
            if self.tag:
                q_objects &= Q(keywords__slug=self.tag)
            
            if self.published == _PUBLISHED:
                q_objects &= Q(date_published__isnull=False)
            elif self.published == _UNPUBLISHED:
                q_objects &= Q(date_published__isnull=True)
            
            context[self.varname] = Poetry.objects.filter(q_objects).count()
        
        except:
            print ("Error: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno)) 
            raise template.TemplateSyntaxError, "Something went wrong. Check the queryset to resolve the error"            
            
        return ''


class PoetryRandomNode(Node):
    """
    Render the poetry list (random order), published/unpublished
    """

    def __init__(self, published=True, count=5, varname=None):
        self.count = count
        self.varname = varname
        self.published = published

    @classmethod
    def handle_token(cls, parser, token, published=True):
        """
        Class method to parse and return a Node.
        """
        tokens = token.split_contents()
        
        if len(tokens) < 4:
            raise template.TemplateSyntaxError, "%s tag takes at least three arguments" % tokens[0]

        # Check the 1st argument
        try:
            count = int(tokens[1])
            if count < 1:
                raise template.TemplateSyntaxError, "First argument of %s tag must be a positive integer" % tokens[0]
        except:
            raise template.TemplateSyntaxError, "First argument of %s tag must be a positive integer" % tokens[0]
        
        # Check the 2nd argument
        if tokens[2] == 'as':
            correct_syntax = "'%s [count] as [varname]'" % tokens[0]

            return cls(
                       published = published,
                       count=count, 
                       varname = tokens[3]
                    )
        else:
            raise template.TemplateSyntaxError, "Wrong syntax."
        

    def render(self, context):
        q_objects = Q()
        try:
            # poetries which are unpublished: [:self.count]
            if self.published is True:
                q_objects &= Q(date_published__isnull=False)
            else:
                q_objects &= Q(date_published__isnull=True)
            
            obj_list = Poetry.objects.filter(q_objects)
            indexes = random.sample(range(len(obj_list)), self.count)
            result = []
            for index in indexes:
                result.append(obj_list[index])

            context[self.varname] = result
        
        except:
            print ("Error: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno)) 
            raise template.TemplateSyntaxError, "Something went wrong. Check the queryset to resolve the error"            
            
        return ''


@register.tag
def get_recent_poetries(parser, token):
    """
    Get the list of recent poetries (published only)
    
    Syntax::
        case 1: {% get_recent_poetries [count] as [varname] %}
        case 2: {% get_recent_poetries [count] by [Author object] as [varname] %}
        case 3: {% get_recent_poetries [count] in [language] as [varname] %}
        case 4: {% get_recent_poetries [count] has [tag] as [varname] %}
        
    Example usage::
        {% get_recent_poetries 5 as poetry_list %}
        {% get_recent_poetries 5 by creator as poetry_list %}
        {% get_recent_poetries 5 in hi as poetry_list %}
        {% get_recent_poetries 5 has tag1 as poetry_list %}
    """     
    
    return RecentPoetryNode.handle_token(parser, token)


@register.tag
def get_similar_poetries(parser, token):
    """
    Get the list of similar poetries
    
    Syntax::
        case 1: {% get_similar_poetries [count] like [Poetry object] as [varname] %}        
        
    Example usage::
        {% get_similar_poetries 5 like poetry as poetry_list %}
    """     
    
    return SimilarPoetryNode.handle_token(parser, token)


@register.tag
def get_poetry_count(parser, token):
    """
    Get count of the poetry
    
    Syntax::
        case 1: {% get_poetry_count as [varname] %}
        case 2: {% get_poetry_count by [Author object] as [varname] %}
        case 3: {% get_poetry_count in [language] as [varname] %}
        case 4: {% get_poetry_count has [tag] as [varname] %}
        case 5: {% get_poetry_count published as [varname] %}
        case 5: {% get_poetry_count unpublished as [varname] %}
        case 6: {% get_poetry_count by [Author object] published as [varname] %}
        case 7: {% get_poetry_count by [Author object] unpublished as [varname] %}
        
    Example usage::
        {% get_poetry_count as count %}
        {% get_poetry_count by creator as count %}
        {% get_poetry_count in hi as count %}
        {% get_poetry_count has tag1 as count %}
        {% get_poetry_count published as count %}
        {% get_poetry_count unpublished as count %}
        {% get_poetry_count by creator published as count %}
        {% get_poetry_count by creator unpublished as count %}
    """     
    
    return PoetryCountNode.handle_token(parser, token)

@register.tag
def get_poetry_unpub_rand(parser, token):
    """
    Get the list of unpublished poetries (random order)
    
    Syntax::
        case 1: {% get_poetry_unpub_rand [count] as [varname] %}
        
    Example usage::
        {% get_poetry_unpub_rand 5 as poetry_list %}
    """     
    
    return PoetryRandomNode.handle_token(parser, token, False)

@register.tag
def get_poetry_pub_rand(parser, token):
    """
    Get the list of published poetries (random order)
    
    Syntax::
        case 1: {% get_poetry_pub_rand [count] as [varname] %}
        
    Example usage::
        {% get_poetry_pub_rand 5 as poetry_list %}
    """     
    
    return PoetryRandomNode.handle_token(parser, token)