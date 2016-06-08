import os, sys, traceback
from django.utils.html import strip_tags

def format_text_as_html():
    pass


def truncatewords(str, limit=30):
    """
    Returns first `limit` characters from the `str` string
    """
    try:
        limit = int(limit)
        # invalid literal for int()
    except ValueError:
        # Fail silently.
        return str

    # Make sure it's unicode
    str = unicode(str)

    # Return the string itself if length is smaller or equal to the limit
    if len(str) <= limit:
        return str

    # Cut the string
    str = str[:limit]

    # Break into words and remove the last
    words = str.split(' ')[:-1]

    # Join the words and return
    return ' '.join(words) + '...'


def truncatelines(str, limit=4):
    """
    Returns first `limit` lines from the `str` string
    strip the html tags.
    """
    try:
        limit = int(limit)
        # invalid literal for int()
    except ValueError:
        # Fail silently.
        return str
    
    try:
        # Make sure it's unicode
        str = unicode(str)
    
        str.replace("<[\s]*\/?br[\s]*\/?>","\n")
        str = strip_tags(str)
        ## Split the string by lines and remove blank elements if any 
        str = [val for val in str.splitlines() if len(val) > 0]    
    
        # Cut the string
        str = str[:limit]
        str = '\n'.join(str) + '...'
    except:
        print ("Error: Unexpected error:", sys.exc_info()[0])
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print ("DBG:: Error in %s on line %d" % (fname, lineno))

    # Join the words and return
    return str


def html_to_plain_text(str):
    """
    Convert the html string `str` to plain text. 
    Without disturbing the formatting e.g. change <br> to `/n' etc
    Remove leading and ending white spaces.
    """
    
    try:
        # Make sure it's unicode
        str = unicode(str)
        # Replace html break line tags with newline '\n'
        str.replace("<[\s]*\/?br[\s]*\/?>","\n")
        # Strip remaining html
        str = strip_tags(str)
        # Remove leading and ending white spaces
        str = str.strip()
        
    except:
        print ("Error: Unexpected error:", sys.exc_info()[0])
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print ("DBG:: Error in %s on line %d" % (fname, lineno))
                 
    return str


def user_has_group(user, groups):
    '''
    @summary: returns True if user is in given ``groups`` list
        like ['Administrator', 'Editor']
    '''
    if user.is_authenticated():       
        if bool(user.groups.filter(name__in=groups)) | user.is_superuser:
            return True
    return False        