import sys
import traceback
#from crawlers.forms import RawArticleForm
from crawlers.models import RawArticle
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


def save_to_db(data):
    """
    Save the data dictionary in the database table corresponding to "crawlers.models.RawArticle"
    data['index'] 
    data['title']
    data['author']
    data['poem']
    data['url']
    """
  
    print "-----------------------------------------"
    print data['index']
    print data
    print "-----------------------------------------"
    
    try:        
        # Insert Raw Article information        
        raw = RawArticle()
        if validate_source_url(data['url']):
            raw.source_url = data['url']
            raw.content = json.dumps(data)
            raw.save()
        else:
            print "ERROR: URL IS NOT VALID ", data['url']
    except:
        print "Unexpected error:", sys.exc_info()[0]
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print "Error in %s on line %d" % (fname, lineno)
    

if __name__ == "__main__":
    save_to_db()