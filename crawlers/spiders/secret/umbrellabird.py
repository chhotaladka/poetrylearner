import scrapy
import re
import json

try:
    from crawlers.utils import save_to_db_poem, save_to_db_author, get_language_list_for_url
except ImportError:    
    def save_to_db_poem(data):
        print data
        
    def save_to_db_author(data):
        print data
        
    def get_language_list_for_url(url):
        print url


class UmbrellabirdBot(scrapy.Spider):
    """
    Crawl the urdupoetry.com pages.
    It starts crwaling from the "poet list" page.
    Crawls all poets' creations till the poem page, and finally save the extracted poem into
    the database i.e. crawlers.models.RawArticle

    """

    name = 'urdupoetry'
    allowed_domains = ['urdupoetry.com']
    
    """
    DON'T CHANGE THE start_urls, all rules depend upon this page
    """
    start_urls = ["http://www.urdupoetry.com/poetlist.html"]
    
    domain_name = "http://www.urdupoetry.com/"
    
    count_visit_author = 0
    count_visit_article = 0
    count_articles = 0
    
    def parse(self, response):
        #print response.body
        
        with open("up_exception_author.txt", "w") as outfile:
            outfile.write("------------------ Exception occurred : AUTHOR LIST--------------------------------\n")
        with open("up_exception_article.txt", "w") as outfile:
            outfile.write("------------------Exception occurred : ARTICLE LIST--------------------------------\n")

        links = response.xpath("/html/body/table//tr[2]/td[2]/div[2]/table//tr/td/a/@href").extract()
        
        author_links = [self.domain_name + x for x in links]
        
        for url in author_links:
            print "Visiting URL ", url
            yield scrapy.Request(url, callback=self.parse_author_contents)


    def parse_author_contents(self, response):
        self.count_visit_author = self.count_visit_author + 1

        author_link = response.url
        
        print "Parsing author No. ", self.count_visit_author
	
        # Parse the page, find out the articles list, generate request for each article          
        try:
            print "Extracting poem links from Author page"
            articles = response.xpath("/html/body/table//tr[3]/td/table//tr/td/a/@href").extract()

            articles_links = [self.domain_name + x for x in articles]
            
            for url in articles_links:
                print "Visiting ARTICLE ", url
                yield scrapy.Request(url, callback=self.parse_article_page)
        except:
            print "Nothing found in Author page!!!"
            with open("up_exception_author.txt", "a") as outfile:
                json.dump({'index': self.count_visit_author, 'link': response.url}, outfile, indent=4)
                   

    """
    First check for the page containing div[@class='poem'] in the XPATH
    1. If found then extract the poem.
    """
    def parse_article_page(self, response):
        self.count_visit_article = self.count_visit_article + 1
        try:
            print "Extracting poem ", self.count_visit_article, " from Article page"
            p = response.xpath("/html/body/table//tr[2]/td/table//tr/td/pre").extract()
            poem = " ".join(x.encode('utf-8') for x in p)
            
            if poem:
                title = response.xpath("/html/body/table//tr[2]/td/table//tr/td/p/strong/text()").extract()[0].encode('utf-8')
                
                self.count_articles = self.count_articles + 1
                
                data = {}
                data['index'] = self.count_articles
                data['title'] = title
                data['author'] = ''
                data['poem'] = poem
                data['url'] = response.url.encode('utf-8')
                
                # Store these information in DB
                save_to_db_poem(data)
                
            else:
                print "First method failed trying another xpath"
                p = response.xpath("/html/body/center/p").extract()
                poem = " ".join(x.encode('utf-8') for x in p)
                
                if poem:
                    title = response.xpath("/html/body/center/p[1]/strong/text()").extract()[0].encode('utf-8')
                    author = response.xpath("/html/body/center/p[1]/a/em/text()").extract()[0].encode('utf-8')
                    self.count_articles = self.count_articles + 1
                    
                    data = {}
                    data['index'] = self.count_articles
                    data['title'] = "".join(x.encode('utf-8') for x in title)
                    data['author'] = "".join(x.encode('utf-8') for x in author)
                    data['poem'] = poem
                    data['url'] = response.url.encode('utf-8')
                    
                    # Store these information in DB
                    save_to_db_poem(data)
                
                else:
                    print "Both method failed write it in file for further processing"
        except:
            print "Error Article page!!!"
            with open("up_exception_article.txt", "a") as outfile:
                json.dump({'index': self.count_visit_article, 'link': response.url}, outfile, indent=4)
