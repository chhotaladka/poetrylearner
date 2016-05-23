import scrapy
import re
import json
import os, sys, traceback

try:
    from crawlers.utils import save_to_db_poem, save_to_db_author, get_language_list_for_url
except ImportError:    
    def save_to_db_poem(data):
        print data
        
    def save_to_db_author(data):
        print data
        
    def get_language_list_for_url(url):
        return []
         

def remove_tags(html, tags):
    """Returns the given HTML with given tags removed."""
    tags = [re.escape(tag) for tag in tags.split()]
    tags_re = '(%s)' % '|'.join(tags)
    starttag_re = re.compile(r'<%s(/?>|(\s+[^>]*>))' % tags_re, re.U)
    endtag_re = re.compile('</%s>' % tags_re)
    html = starttag_re.sub('', html)
    html = endtag_re.sub('', html)
    return html


class ReindeerBot(scrapy.Spider):
    '''
    Crawl the rekhta.com pages.
    '''
    name = 'rekhta'
    allowed_domains = ['rekhta.org']

    """
    DON'T CHANGE THE start_urls, all rules depend upon this page
    """
    start_urls = ["https://rekhta.org"]

    domain_name = "https://rekhta.org/"
    BASE_URL_POETS = "https://rekhta.org/poets/"
    
    # languages of the poetry to be crawled: hindi, urdu or english(default)
    LANGUAGES = ['hi', 'en', 'ur']

    ##
    # APIs

    # example of API_POETS_READ = 'https://rekhta.org/Home/Api_Poets_Read?sort=SortName-asc&page=1&pageSize=10000&lang=1&startsWith=a'
    API_POETS_READ = '/Home/Api_Poets_Read'
    
    # example of API_POET_READ = '/Home/Api_Poet_Read?sort=SortTitle-asc&page=1&lang=1&pageSize=10000&info=ghazals&id=mirza-ghalib'
    # WHERE info is in ['ghazals', 'couplets', 'nazms', 'profile', 'audio', 'video', 'ebooks']
    # id = poet slug
    # lang = 1 for eng, 2 for hindi, 3 for urdu
    API_POET_READ = '/Home/Api_Poet_Read'    

    def parse(self, response):
        #print response.body

        with open("exception_poet.txt", "w") as outfile:
            outfile.write("------------------ Exception occurred : POET LIST--------------------------------\n")
        with open("exception_poetry.txt", "w") as outfile:
            outfile.write("------------------Exception occurred : POETRY LIST--------------------------------\n")


        ABCD = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u',
                'v','x','y','z',]

        for alphabet in ABCD:
            print "Listing poets", alphabet
            url = self.domain_name + self.API_POETS_READ + '?' + '&sort=SortName-asc' + '&page=1' + '&lang=1' + '&pageSize=10000' + '&startsWith=' + alphabet

            yield scrapy.Request(url, callback=self.l2_parse_poets_list)



    def l2_parse_poets_list(self, response):
        '''
        Level 2: parse poets list and crawl to next level i.e. individual poet's page and its subsections
        '''
        i = response.url.find('&startsWith=')
        print "l2_parse_poets_list:", response.url[i+12]

        data = json.loads(response.body)
        poets = data['Data']
        total = data['Total']
        errors = data['Errors']
        count = len(poets)
        print "l2_parse_poets_list: result has", count, "of", total, "poets"

        for poet in poets:
            # extract info of a poet and save
            #print poet
            poet_info = {}
            poet_info['name'] = poet['Name']
            poet_info['birth'] = poet['FromDate']
            poet_info['death'] = poet['ToDate']
            poet_info['url'] = self.BASE_URL_POETS + poet['SEOSlug'] + "/"

            # save poet info to db
            save_to_db_author(poet_info)

            # Crawl poet's page
            url_base = self.domain_name + self.API_POET_READ + '?' + '&sort=SortTitle-asc' + '&page=1' + '&lang=1' + '&pageSize=10000' + '&id=' + poet['SEOSlug']
            for info in ['ghazals', 'couplets', 'nazms',]:
                url = url_base + '&info=' + info
                print url
                yield scrapy.Request(url, callback=self.l3_parse_poetry_list)

    
    def l3_parse_poetry_list(self, response):
        '''
        Level 3: parse poet's poetry list
        '''
        i = response.url.find('&id=')
        print "l3_parse_poetry_list:", response.url[i+4:]
        
        data = json.loads(response.body)

        poetries = data['Data']
        total = data['Total']
        errors = data['Errors']
        count = len(poetries)
        print "l3_parse_poetry_list: result has", count, "of", total, "poetries"        

        for poetry in poetries:
            # extract info of the poetry, and crawl poetry page
            #print poetry
            content_slug = poetry['ContentSlug']
            type_slug = poetry['TypeSlug']

            # Crate url
            url = self.domain_name + type_slug + '/' + content_slug
            
            # Check if the entry for ``url`` exist in db,
            # Also find out the list of languages in which the content is there.
            lang_list = get_language_list_for_url(url)
            
            # Now crawl poetry page only for remaining langauge
            for lang in (x for x in self.LANGUAGES if x not in lang_list):
                    url_t = url + '?lang=' + lang
                    yield scrapy.Request(url_t, callback=self.l4_parse_poetry)                    
                        
#             for lang in self.LANGUAGES:
#                 if lang not in lang_list:
#                     url_t = url + '?lang=' + lang
#                     yield scrapy.Request(url_t, callback=self.l4_parse_poetry)                          
                            

    def l4_parse_poetry(self, response):
        '''
        Level 4: parse poetry page, extract poetry, and save.
        '''
        #print response.url
    
        try:
            # extract data    
            content = response.xpath("//div[@id='ImageHost']//div[@class='PoemDisplay']/span").extract()[0]
            title = response.xpath("//div[@class='shayariContainerDiv']/div[@class='left_pan_shayari']/div[@class='shayari_first']/h1/text()").extract()[0]
            
            #poet = response.xpath("//div[@class='artist_img_descrpt']/div[@class='about_artist']/h2/text()").extract()[0]
            # poet name must be in english, that is why we have to discard the previous one. 
            poet_href = response.xpath("//div[@class='artist_img']//a/@href").extract()[0]
            p = re.compile(ur'poets/(.+)/') #href="/poets/anjum-tarazi/?lang=Hi"
            poet = p.search(poet_href).group(1)
            poet = poet.replace('-', ' ')
            
            poem = remove_tags(content, 'span')                    

        except:
            print "ERROR: l4_parse_poetry: failed to extract data"
            with open("exception_poetry.txt", "a") as outfile:
                json.dump({'link': response.url, 'error': 'parsing failed'}, outfile, indent=4)
        
        try:                
            # check response.url for language information: https://.....xyz/?lang=hi
            tmp = response.url
            tmp = tmp.split('?')
            url = tmp[0]
            language = tmp[1].split('=')[1]            
                                            
            data = {}
            data['poem'] = poem
            data['url'] = url
            data['title'] = title
            data['author'] = poet.title()
            data['language'] = language
 
            # Store these information in DB
            save_to_db_poem(data)

        except:
            print("ERROR: l4_parse_poetry: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno))            
            with open("exception_poetry.txt", "a") as outfile:
                json.dump({'link': response.url, 'error': sys.exc_info()[0]}, outfile, indent=4)