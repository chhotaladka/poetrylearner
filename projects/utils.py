import requests
import traceback
import sys
from lxml import etree
from urllib import urlencode
from urlparse import urlparse, parse_qs, urlunparse
import string
import re

    
"""
Fetch data from 'url' and Extract relevent information

Returns dictionary having following contents:-
> title: title of the page
> description: first para of wiki article
> source: Source website name
"""
def fetch(url):

    try:
        return_dict = {}
        r = requests.get(url, timeout=3, allow_redirects=False)
        if r.status_code == requests.codes.ok:
            #print "LOGS: encoding is" + r.encoding
            provider = get_provider_name(url)
            return_dict = extract_data(r.text, provider)
            
            return return_dict
        else:
            return None
    except:
        print "LOGS: Some error in fetching url !!!"
        print "LOGS: Unexpected error:", sys.exc_info()[0]
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print "LOGS: Error in %s on line %d" % (fname, lineno)
        return None


"""
Returns provider names
"""
def get_provider_name(url):
    if ".wikipedia.org" in url:
        return "wiki"
    elif "goodreads.com" in url:
        return "goodreads"
    else:
        return None
    
    
"""
Extract data from @data
provider: wiki/goodreads/...

"""
def extract_data(data, provider):
    
    #First parsing it with lxml 
    hparser = etree.HTMLParser(encoding='utf-8')
    html = etree.HTML(data,parser=hparser)
#     result = etree.tostring(html, pretty_print=True, method="html")
#     print(result)
    

    return_dict = {}
    
    if provider is "wiki":
        return_dict = extract_info_from_wiki(html)
    elif provider is "goodreads":
        return_dict = extract_info_from_goodreads(html)
    else:
        return None
        
    return return_dict



"""
Extract content from wikipedia.org

"""
def extract_info_from_wiki(tree): 

    return_dict = {}
    try:
        return_dict['title'] = tree.xpath("//h1[@id='firstHeading']/text()")[0] 
        
        ## Select the first paragraph of the wiki article
        description = tree.xpath("//div[@class='mw-content-ltr']/p[1]/descendant::text()")
              
        return_dict['description'] = refine_string(description)       
        return_dict['source'] = "Wikipedia"
        
        return return_dict        
        
    except:
        print "Unexpected error:", sys.exc_info()[0]
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print "Error in %s on line %d" % (fname, lineno)
        return None
    
    return None
        
"""
Extract content from goodreads.com
"""
def extract_info_from_goodreads(tree):
    return None


"""
Remove the extra symbols from the string
"""
def refine_string(str):
    s1 = "".join(x.encode('utf-8') for x in str)
    # to remove contents inside " ()"
    s2 = re.sub(r'\s\(.*?\)', '',s1)
    # to remove contents inside "[]"
    s3 = re.sub(r'\[.*?\]', '', s2)
    return s3