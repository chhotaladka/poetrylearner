import sys
import traceback

from crawlers.models import RawArticle, RawAuthor
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import json

def validate_source_url(url):
    validate = URLValidator()
    try:
        validate(url)
        return True
    except ValidationError, e:
        print e
        return False


def save_to_db_poem(data):
    """
    Save the data dictionary in the database table corresponding to "crawlers.models.RawArticle"
    data['title']
    data['author']
    data['poem']
    data['url']
    """
    
    try:        
        # Insert Raw Article information        
        raw = RawArticle()
        if validate_source_url(data['url']):
            raw.source_url = data['url']
            raw.title = data['title']
            raw.author = data['author']
            raw.content = data['poem']
            raw.save()
        else:
            print "ERROR: save_to_db_poem: URL IS NOT VALID ", data['url']
    except:
        print "Unexpected error:", sys.exc_info()[0]
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print "Error in %s on line %d" % (fname, lineno)


def save_to_db_poem_multiple(data, language):
    """
    Save the data in the db table corresponding to "crawlers.models.RawArticle"
    create new entry for url if not exist, otherwise append to the matched url
    data['title']
    data['author']
    data['poem']
    data['url']    
    """
    
    try:
        # Search for existing article using data['url']
        obj = RawArticle.objects.source_url(data['url'])
        if obj:
            # append the poem to the ``content``
            obj.content = obj.content + data['poem']
            if language == 'en':
                # override ``title`` and ``author`` part. 
                # because we need title and author only in english
                obj.title = data['title']
                obj.author = data['author']
            obj.save()
            
        else:                
            # Create new article        
            raw = RawArticle()
            if validate_source_url(data['url']):
                raw.source_url = data['url']
                raw.title = data['title']
                raw.author = data['author']
                raw.content = data['poem']
                raw.save()
            else:
                print "ERROR: save_to_db_poem: URL IS NOT VALID ", data['url']
    except:
        print "Unexpected error:", sys.exc_info()[0]
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print "Error in %s on line %d" % (fname, lineno)    
    
def save_to_db_author(data):
    """
    Save Author info to db
    data['url']
    data['name']
    data['birth']
    data['death']     
    """
    try:        
        # Insert Raw Author information        
        raw = RawAuthor()
        if validate_source_url(data['url']):
            raw.source_url = data['url']
            raw.name = data['name']
            raw.birth = data['birth']
            raw.death = data['death']        
            raw.save()
        else:
            print "ERROR: save_to_db_author: URL IS NOT VALID ", data['url']        
    except:
        print "Unexpected error:", sys.exc_info()[0]
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print "Error in %s on line %d" % (fname, lineno)    
