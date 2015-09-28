import scrapy
import re

class WikiSpider(scrapy.Spider):
    """
    Crawl the wikipedia page, 
    extract the basic info from the page like first paragraph and
    the infobox table
    """

    name = 'wikipedia'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Gulzar']

    def parse(self, response):
        # Select the first paragraph of the wiki article
        #p = response.xpath("//div[@class='mw-content-ltr']/p[1]/descendant::text()").extract()
        p = response.xpath("id('mw-content-text')/p[1]/descendant::text()").extract()
        info = refine_string(p)

        # Select the Infobox table (displayed on the right side of the wiki page)
        infobox_th = response.xpath("//div[@class='mw-content-ltr']/table[1]//tr[position()>2]/th/descendant::text()").extract()
        c_th = len(infobox_th)
        
        infobox_td = []
        for i in range(3, c_th + 3):
            td = response.xpath("//div[@class='mw-content-ltr']/table[1]/tr[%(id)s]/td/descendant::text()"%{"id":i}).extract()
            td_refined = "".join(x.encode('utf-8') for x in td)
            infobox_td.append(td_refined)
        
        infobox = []
        for i in range(c_th):
            temp = []
            temp.append(infobox_th[i])
            temp.append(infobox_td[i])
            infobox.append(temp)

        ret = {
            'title': response.css('h1::text').extract()[0],
            'info': info,
            'infobox': infobox,
            'link': response.url,
        }
        print ret
        yield ret
        
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