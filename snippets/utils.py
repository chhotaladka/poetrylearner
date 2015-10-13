
def format_text_as_html():
    pass


def truncatewords(Value,limit=30):
    try:
        limit = int(limit)
        # invalid literal for int()
    except ValueError:
        # Fail silently.
        return Value

    # Make sure it's unicode
    Value = unicode(Value)

    # Return the string itself if length is smaller or equal to the limit
    if len(Value) <= limit:
        return Value

    # Cut the string
    Value = Value[:limit]

    # Break into words and remove the last
    words = Value.split(' ')[:-1]

    # Join the words and return
    return ' '.join(words) + '...'
    