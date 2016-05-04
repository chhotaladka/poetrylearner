from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
import os, sys, traceback
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount

from dashboard.models import UserProfile

# Create your views here.

@receiver(user_logged_in)
def CreateProfile(sender, request, user,**kwargs):
    '''
    This function catches the signal for social login or social account add, 
    and check for the User profile object: if exist then do nothing,
    if not then create it and set the gender field.
    '''
    try:        
        profile = UserProfile.objects.get(user=user)
        print "DBG:: User profile exist, do nothing"
    except UserProfile.DoesNotExist:
        print "DBG:: User profile does not exist, create a new one"
  
        profile = UserProfile()
        profile.user = user
        try:
            sociallogin = SocialAccount.objects.get(user=user)
            print "DBG:: Caught the signal--> Printing extra data of the account: \n", sociallogin.extra_data
            if('google' == sociallogin.provider ):
                user.first_name = sociallogin.extra_data['given_name']
                user.last_name = sociallogin.extra_data['family_name']
                user.save()
            elif ('facebook' == sociallogin.provider ):
                user.first_name = sociallogin.extra_data['first_name']
                user.last_name = sociallogin.extra_data['last_name']
                user.save()
            profile.gender = sociallogin.extra_data['gender']
        except:
            print ("Error:: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno))           
            print "DBG:: Gender does not exist in social account"
            
        profile.save()


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
    print "user profile of ", user_id
    try:
        user_id = int(user_id) # required for comparision
    except ValueError:
        print "DBG:: invalid request for user_id ", user_id
        raise Http404
            
    if request.user.is_authenticated():
        if request.user.id == user_id:
            scope = request.GET.get('viewas', None)
            if scope == 'public':
                return public_profile(request, user_id)
            else:
                return private_profile(request)

    return public_profile(request, user_id)
        

@login_required
def private_profile(request):
    '''
    Private profile of the user
    '''
    print "DBG:: private profile"
    profile = UserProfile.objects.get(user=request.user.id)

    social_accounts = []
    providers = ["Facebook", "Google", "Twitter"]
    for provider in providers:
        if profile.is_social_account_exist(provider):
            extra_context = {}
            extra_context['provider_name'] = profile.get_provider_name(provider)
            extra_context['profile_image'] = profile.get_avatar_url(provider)
            extra_context['profile_username'] = profile.get_name(provider)
            extra_context['profile_gender'] = profile.get_gender(provider)
            extra_context['profile_url'] = profile.get_social_url(provider)
            extra_context['profile_email'] = profile.get_email(provider)
            social_accounts.append(extra_context)
                
    ## Make the context and render     
    context = {'profile': profile, 'social_accounts': social_accounts}
    template = 'dashboard/profile-private.html'
    
    return render(request, template, context)

    
def public_profile(request, user_id):
    '''
    Public profile of the user
    '''
    print "DBG:: public profile"
    user = get_object_or_404(User, pk=user_id)
    profile = UserProfile.objects.get(user=user) or None #FIXME: giving error when entry does not exist
    
    ## Make the context and render     
    context = {'profile': profile}
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
