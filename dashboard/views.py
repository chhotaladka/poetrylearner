from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def user_home(request, user_id):
    '''
    Home page of the user
    '''
    
    ## Make the context and render     
    context = {}
    template = 'dashboard/base.html'
    
    return render(request, template, context)


def user_profile(request, user_id):
    '''
    Profile page of the user
    '''
    try:
        user_id = int(user_id)
        if request.user.is_authenticated():
            if request.user.id == user_id:
                scope = request.GET.get('viewas', None)
                if scope == 'public':
                    return public_profile(request, user_id)
                else:
                    return private_profile(request)

        return public_profile(request, user_id)
        
    except ValueError:
        print "DBG:: invalid request for user_id ", user_id
        raise Http404


@login_required
def private_profile(request):
    '''
    Private profile of the user
    '''

    ## Make the context and render     
    context = {}
    template = 'dashboard/profile-private.html'
    
    return render(request, template, context)

    
def public_profile(request, user_id):
    '''
    Public profile of the user
    '''
    
    user = get_object_or_404(User, pk=user_id)
    
    ## Make the context and render     
    context = {}
    template = 'dashboard/profile-public.html'
    
    return render(request, template, context)
    

def user_bookmarks(request, user_id):
    '''
    Bookmarks by the user
    '''
    
    user = get_object_or_404(User, pk=user_id)
    
    ## Make the context and render     
    context = {}
    template = 'dashboard/base.html'
    
    return render(request, template, context)


def user_favorites(request, user_id):
    '''
    Favorites of the user
    '''
    
    user = get_object_or_404(User, pk=user_id)
    
    ## Make the context and render     
    context = {}
    template = 'dashboard/base.html'
    
    return render(request, template, context)
