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

    # Make sure it's unicode
    str = unicode(str)

    str.replace("<[\s]*\/?br[\s]*\/?>","\n")
    str = strip_tags(str)
    ## Split the string by lines and remove blank elements if any 
    str = [val for val in str.splitlines() if len(val) > 0]    

    # Cut the string
    str = str[:limit]

    # Join the words and return
    return '\n'.join(str) + '...'
    