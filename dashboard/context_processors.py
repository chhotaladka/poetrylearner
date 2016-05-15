  
def profile(request):
    """
    Add ``profile`` in context if user is authenticated
    """
    if request.user.is_authenticated():
        return {'profile': request.user.profile}
    else:
        return {'profile': None}  
