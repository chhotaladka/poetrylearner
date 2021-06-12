from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.conf.global_settings import LANGUAGES
import traceback, sys
import json

from crawlers.models import RawArticle, RawAuthor

# Minimum length of an article to be qualified as valid Article
ARTICLE_MIN_LEN = 32


def validate_source_url(url):
    validate = URLValidator()
    try:
        validate(url)
        return True
    except ValidationError as e:
        print(e)
        return False

def validate_language(language):
    if language in LANGUAGES:
        return True
    else:
        return False
    

def get_language_list_for_url(url):
    '''
    @summary: In how many languages the entry exist in ``RawArticle`` table for the 'url'.
    Empty list means, there is no entry for 'url'
    '''
    list = RawArticle.objects.get_languages_for_url(url)
    return list


def save_to_db_poem(data):
    '''
    @summary: Save the data dictionary in the database table corresponding to "crawlers.models.RawArticle"
    
    data['title']
    data['author']
    data['poem']
    data['url']
    data['language']
    '''
    
    try:
        # validate fields
        if validate_source_url(data['url']) is False:
            print("ERROR: save_to_db_poem: URL IS NOT VALID ", data['url'])
            return False
        
        if validate_language(data['language']):
            print("ERROR: save_to_db_poem: language is NOT VALID ", data['language'])
            return False
                
        # Insert Raw Article information        
        raw = RawArticle()
        raw.source_url = data['url']
        raw.title = data['title']
        raw.author = data['author']
        raw.content = data['poem']
        raw.language = data['language']
        raw.save()
        
    except:
        print("Unexpected error:", sys.exc_info()[0])
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print("Error in %s on line %d" % (fname, lineno))
  
    
def save_to_db_author(data):
    '''
    @summary:  Save Author info to db
    
    data['url']
    data['name']
    data['birth']
    data['death']     
    '''
    try:
        # validate fields
        if validate_source_url(data['url']) is False:
            print("ERROR: save_to_db_author: URL IS NOT VALID ", data['url'])
            return False
        
        # Check if entry for ``url`` already exists
        list = RawAuthor.objects.source_url(data['url'])
        if list:
            print("WARNING:: save_to_db_author: url already exists", data['url'])
            return False
                      
        # Create a new entry        
        raw = RawAuthor()
        raw.source_url = data['url']
        raw.name = data['name']
        raw.birth = data['birth']
        raw.death = data['death']        
        raw.save()
        
    except:
        print("Unexpected error:", sys.exc_info()[0])
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print("Error in %s on line %d" % (fname, lineno))    
