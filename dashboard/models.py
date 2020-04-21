from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from allauth.socialaccount.models import SocialAccount

from common.slugify import slugify

# Default ``gender`` value if not specified in data from social account
GENDER_UNSPECIFIED = "---"

# Create your models here.

class UserProfile(models.Model):
    '''
    User profile populated using social account from Facebook, Google and Twitter respectively.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    signup_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):          # on Python 3
        return "{}'s profile".format(self.user.username)
    
    def __unicode__(self):      # on Python 2
        return "{}'s profile".format(self.user.username)        
 
    class Meta:
        db_table = 'user_profile'
    

    def get_absolute_url(self):        
        kwargs = {'user_id': self.user.id, 'slug': self.get_slug()}
        return reverse('dashboard:public-profile', kwargs=kwargs)
        
    def _get_social_account(self, provider=None):
        '''
        Return the social account object of Google, Facebook, and Twitter in that order if provier is None else return the provider account.
        '''
        if provider != None:
            account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider=provider)
            if len(account_uid):
                return account_uid[0]
            else:
                return None
            
        try:
            account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='google')
            if len(account_uid):
                return account_uid[0]

            account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
            if len(account_uid):
                return account_uid[0]
    
            account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='twitter')
            if len(account_uid):
                return account_uid[0]
        except:
            return None
    
    def is_social_account_exist(self, provider):
            account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider=provider)
            if len(account_uid):
                return True
            else:
                return False
        
    
    def get_avatar_url(self, provider=None):
        '''
        If provider is None, return the avatar of preferred social account.
        TODO: return default avatar if no social account is found.
        '''
        profile = self._get_social_account(provider)
        if profile != None:
            return profile.get_avatar_url()
        else:
            return None
    
    def get_username(self, provider=None):
        '''
        If provider is None, return the username of preferred social account.
        '''
        profile = self._get_social_account(provider)
        if profile != None:
            if self.get_provider_name(profile.provider) == 'facebook':
                return self._get_fb_username(profile)
            elif self.get_provider_name(profile.provider) == 'google':
                return self._get_google_username(profile)
            elif self.get_provider_name(profile.provider) == 'twitter':
                return self._get_tw_username(profile)
            else:
                return self.user.username
        else:
            return self.user.username

    def get_name(self, provider=None):
        return "{0} {1}".format(self.get_first_name(provider), self.get_last_name(provider))

    def get_first_name(self, provider=None):
        '''
        Return the first name from preferred social account, if provider is None.
        TODO: return default first name from User model if no social account is found.
        '''
        profile = self._get_social_account(provider)
        if profile != None:
            if self.get_provider_name(profile.provider) == 'facebook':
                return self._get_fb_fname(profile)
            elif self.get_provider_name(profile.provider) == 'google':
                return self._get_google_fname(profile)
            elif self.get_provider_name(profile.provider) == 'twitter':
                return self._get_tw_fname(profile)
            else:
                return self.user.first_name
        else:
            return self.user.first_name
    
    def get_last_name(self, provider=None):
        '''
        Return the last name from preferred social account, if provider is None.
        TODO: return default last name from User model if no social account is found.
        '''
        profile = self._get_social_account(provider)
        if profile != None:
            if self.get_provider_name(profile.provider) == 'facebook':
                return self._get_fb_lname(profile)
            elif self.get_provider_name(profile.provider) == 'google':
                return self._get_google_lname(profile)
            elif self.get_provider_name(profile.provider) == 'twitter':
                return self._get_tw_lname(profile)
            else:
                return self.user.last_name

        else:
            return self.user.last_name
    
    def get_slug(self):
        return slugify(self.get_first_name())
        
    def is_slug_valid(self, slug):
        '''
        Validate the slug
        '''
        if slug == self.get_slug():
            return True
        else:
            return False            

    def get_gender(self, provider=None):
        '''
        Return the gender from preferred social account, if provider is None.
        '''
        profile = self._get_social_account(provider)
        if profile != None:
            if self.get_provider_name(profile.provider) == 'twitter':
                # Twitter do not provide gender information
                return GENDER_UNSPECIFIED
            return profile.extra_data.get('gender', GENDER_UNSPECIFIED)
        else:
            return GENDER_UNSPECIFIED

    def get_email(self, provider=None):
        '''
        Return the email of preferred social account, if provider is None.
        TODO: return default email if no social account is found.
        '''
        profile = self._get_social_account(provider)
        if profile != None:
            if self.get_provider_name(profile.provider) == 'twitter':
                return self.user.email
            return profile.extra_data.get('email', '')
        else:
            return self.user.email
        
    def get_contact(self, provider=None):
        '''
        Returns Email address. In case of Twitter, returns screen name e.g. @chhotaladka
        '''
        profile = self._get_social_account(provider)
        if profile != None:
            if self.get_provider_name(profile.provider) == 'twitter':
                return "@{0}".format(profile.extra_data.get('screen_name', ''))
            return profile.extra_data.get('email', '')
        else:
            return self.user.email        

    def get_social_url(self, provider=None):
        '''
        Return the social url of preferred social account, if provider is None.
        todo: return default blank  if no social account is found.
        '''
        profile = self._get_social_account(provider)
        if profile != None:
            #print profile.extra_data
            if self.get_provider_name(profile.provider) == 'facebook':
                return self._get_fb_link(profile)
            elif self.get_provider_name(profile.provider) == 'google':
                return self._get_google_link(profile)
            elif self.get_provider_name(profile.provider) == 'twitter':
                return self._get_tw_link(profile)
            else:
                return ""
        else:
            return ""
       
    def get_provider_name(self,provider=None):
        '''
        Return the provider name of preferred social account, if provider is None.
        TODO: return default blank  if no social account is found.
        '''
        profile = self._get_social_account(provider)
        if profile != None:
            return profile.provider
        else:
            return provider    

    def get_birthday(self):
        return self.date_birth  
    
    def get_signup_time(self):
        return self.signup_date

    ##
    # Private functions for retrieving the fname, lname, email etc. from GooGle, Facebook and twitter
    def _get_google_fname(self,profile):
        return profile.extra_data.get('name', '').split()[0]
    
    def _get_google_lname(self,profile):
        return profile.extra_data.get('family_name', '')

    def _get_google_email(self,profile):
        return profile.extra_data.get('email', '')

    def _get_google_username(self,profile):
        return profile.extra_data.get('given_name', '')

    def _get_google_link(self,profile):
        return profile.extra_data.get('link', '')

    def _get_fb_fname(self,profile):
        return profile.extra_data.get('first_name', '')
    
    def _get_fb_lname(self,profile):
        return profile.extra_data.get('last_name', '')

    def _get_fb_email(self,profile):
        return profile.extra_data.get('email', '')

    def _get_fb_username(self,profile):
        return profile.extra_data.get('name', '')

    def _get_fb_link(self,profile):
        return profile.extra_data.get('link', '')
    
    def _get_tw_fname(self,profile):
        return profile.extra_data.get('name', '').split()[0]

    def _get_tw_lname(self,profile):
        names = profile.extra_data.get('name', '').split()
        if len(names) > 1:
            return names[-1]
        else:
            return ''

    def _get_tw_username(self,profile):
        return profile.extra_data.get('screen_name', '')

    def _get_tw_link(self,profile):
        return  "//twitter.com/" + profile.extra_data.get('screen_name', '')


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
