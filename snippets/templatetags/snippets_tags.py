from django import template
from django.template import Node
from django.db.models import Q
import os, sys, traceback
from snippets.models import Snippet

register = template.Library()


class RecentSnippetsNode(Node):
    """
    Render the recent snippets list
    """

    def __init__(self, count=5, varname=None, author=None, language=None, tag=None, published=False):
        self.count = count
        self.varname = varname
        self.author = template.Variable(author)
        self.language = language
        self.tag = tag
        self.published = published              

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
            print "case 1"
            return cls(
                       count=count, 
                       varname = tokens[3]
                    )
            
        elif tokens[2] == 'by':            
            correct_syntax = "'%s [count] by [Author object] as [varname]'" % tokens[0]
            if len(tokens) < 6:
                raise template.TemplateSyntaxError, "Number of arguments are less. Correct syntax is " + correct_syntax
            
            if tokens[4] != 'as':
                raise template.TemplateSyntaxError, "Forth argument must be 'as'. Correct syntax is " + correct_syntax
            
            print "case 2"
            return cls(
                       count=count, 
                       varname = tokens[5],
                       author = tokens[3]
                    )
    
        elif tokens[2] == 'in':
            correct_syntax = "'%s [count] in [language] as [varname]'" % tokens[0]
            if len(tokens) < 6:
                raise template.TemplateSyntaxError, "Number of arguments are less. Correct syntax is " + correct_syntax
            
            if tokens[4] != 'as':
                raise template.TemplateSyntaxError, "Forth argument must be 'as'. Correct syntax is " + correct_syntax
            
            print "case 3"    
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
            
            print "case 4"    
            return cls(
                       count=count, 
                       varname = tokens[5],
                       tag = tokens[3]
                    )
                
        elif tokens[2] == 'published':
            correct_syntax = "'%s [count] published as [varname]'" % tokens[0]
            if len(tokens) < 5:
                raise template.TemplateSyntaxError("Number of arguments are less. Correct syntax is " + correct_syntax)
            
            if tokens[3] != 'as':
                raise template.TemplateSyntaxError("Third argument must be 'as'. Correct syntax is " + correct_syntax)
            
            print "case 5"
            return cls(
                       count=count, 
                       varname = tokens[4],
                       published = True
                    )
        else:
            raise template.TemplateSyntaxError, "Wrong syntax."
        

    def render(self, context):
        q_objects = Q()
        try:
            if self.author:
                author = self.author.resolve(context)
                q_objects &= Q(author__id=author.id)
            
            if self.language:
                q_objects &= Q(language=self.language)
                
            if self.tag:
                q_objects &= Q(tags__slug=self.tag)
            
            if self.published:
                q_objects &= Q(published=True)
                                
            context[self.varname] = Snippet.objects.filter(q_objects).order_by('-updated_at')[:self.count]
        
        except:
            print ("Error: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno)) 
            raise template.TemplateSyntaxError, "Something went wrong. Check the queryset to resolve the error"            
            
        return ''


class SimilarSnippetsNode(Node):
    """
    Render the similar snippets list
    """

    def __init__(self, count=5, varname=None, snippet=None):
        self.count = count
        self.varname = varname
        self.snippet = template.Variable(snippet)

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
            correct_syntax = "'%s [count] like [Snippet object] as [varname]'" % tokens[0]
            raise template.TemplateSyntaxError, "Second argument must be 'like'. Correct syntax is " + correct_syntax
        
        # Check the 4th argument
        if tokens[4] != 'as':
            correct_syntax = "'%s [count] like [Snippet object] as [varname]'" % tokens[0]
            raise template.TemplateSyntaxError, "Forth argument must be 'as'. Correct syntax is " + correct_syntax
            
        return cls(
                   count=count, 
                   varname = tokens[5],
                   snippet = tokens[3]
                )
        

    def render(self, context):
        try:
            snippet = self.snippet.resolve(context)                            
            context[self.varname] = snippet.tags.similar_objects()[:self.count]
    
        except:
            print ("Error: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno)) 
            raise template.TemplateSyntaxError, "Something went wrong. Check the queryset to resolve the error"            
            
        return ''


@register.tag
def get_recent_snippets(parser, token):
    """
    Get the list of recent snippets
    
    Syntax::
        case 1: {% get_recent_snippets [count] as [varname] %}
        case 2: {% get_recent_snippets [count] by [Author object] as [varname] %}
        case 3: {% get_recent_snippets [count] in [language] as [varname] %}
        case 4: {% get_recent_snippets [count] has [tag] as [varname] %}
        case 5: {% get_recent_snippets [count] published as [varname] %}
        
    Example usage::
        {% get_recent_snippets 5 as snippets %}
        {% get_recent_snippets 5 by author as snippets %}
        {% get_recent_snippets 5 in hi as snippets %}
        {% get_recent_snippets 5 has tag1 as snippets %}
        {% get_recent_snippets 5 published as snippets %}
    """     
    
    return RecentSnippetsNode.handle_token(parser, token)


@register.tag
def get_similar_snippets(parser, token):
    """
    Get the list of similar snippets
    
    Syntax::
        case 1: {% get_similar_snippets [count] like [Snippet object] as [varname] %}        
        
    Example usage::
        {% get_recent_snippets 5 like snippet as snippet_list %}
    """     
    
    return SimilarSnippetsNode.handle_token(parser, token)