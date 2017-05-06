from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
import os, sys, traceback
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from dashboard.models import UserProfile, GENDER_UNSPECIFIED
from common.const import USER_GROUP_DEFAULT

# Overriding/altering allauth default methods

class CustomAccountAdapter(DefaultAccountAdapter):
    '''
    @summary: custom account adapter class. To make it work,
    add following line in settings.py 
    ACCOUNT_ADAPTER='dashboard.views.CustomAccountAdapter'
    '''    
    def is_open_for_signup(self, request):
        # To disable account signup, return False. Otherwise return True(Default). 
        return False


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    '''
    @summary: custom social account adapter class. To make it work,
    add following line in settings.py 
    SOCIALACCOUNT_ADAPTER = 'dashboard.views.CustomSocialAccountAdapter'
    '''
    def is_open_for_signup(self, request, sociallogin):
        # To disable social account signup, return False. Otherwise return True(Default). 
        return True


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
    except UserProfile.DoesNotExist:
        print "DBG:: User profile does not exist, create a new one"
  
        profile = UserProfile()
        profile.user = user
        
        # Add `user` to default User Group
        try:
            group = Group.objects.get(name=USER_GROUP_DEFAULT)
        except Group.DoesNotExist:
            group = Group.objects.create(name=USER_GROUP_DEFAULT)
        user.groups.add(group)
        
        try:
            sociallogin = SocialAccount.objects.get(user=user)
            if('google' == sociallogin.provider ):
                user.first_name = sociallogin.extra_data['given_name']
                user.last_name = sociallogin.extra_data['family_name']
                user.save()
            elif ('facebook' == sociallogin.provider ):
                user.first_name = sociallogin.extra_data['first_name']
                user.last_name = sociallogin.extra_data['last_name']
                user.save()
            try:                
                profile.gender = sociallogin.extra_data['gender']
            except:
                print "DBG:: Gender does not exist in social account"
                profile.gender = GENDER_UNSPECIFIED
                
        except:
            print ("Error:: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno))            
            
        profile.save()


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
            extra_context['profile_url'] = profile.get_social_url(provider)
            extra_context['profile_email'] = profile.get_email(provider)
            extra_context['profile_gender'] = profile.get_gender(provider)
            social_accounts.append(extra_context)
            
    # Get groups name
    groups = list(request.user.groups.values_list('name',flat=True))
    if request.user.is_staff:
        groups.append(u'editor')
                
    ## Make the context and render     
    context = {'social_accounts': social_accounts,
               'groups': groups,
               }
    template = 'dashboard/profile-private.html'
    
    return render(request, template, context)

    
def public_profile(request, user_id, slug):
    '''
    Public profile of the user
    '''
    print "DBG:: public profile"
    user = get_object_or_404(User, pk=user_id)
    try:
        profile = UserProfile.objects.get(user=user)
    
    except ObjectDoesNotExist:
        print "ERR:: No profile entry found for user", user, user_id
        profile = None
        raise Http404
    
    if profile.is_slug_valid(slug) is False:
        raise Http404
    
    # Get groups name
    groups = list(user.groups.values_list('name',flat=True))
    if user.is_staff:
        groups.append(u'editor')
    
    ## Make the context and render     
    context = {'public_profile': profile,
               'groups': groups,}
    template = 'dashboard/profile-public.html'
    
    return render(request, template, context)
