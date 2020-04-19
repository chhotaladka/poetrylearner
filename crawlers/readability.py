#coding=utf-8
#!/usr/bin/python
#
# Reference: https://github.com/PirateLearner/pi/
# Requirements:
#    BeautifulSoup <pip install bs4>
#    html5lib <pip install html5lib>

import re
from bs4 import BeautifulSoup, Comment
from bs4 import element as bs_element
from builtins import str
import math
from urllib.parse import urlparse
import requests
import collections
import copy
import sys
import traceback


class Readability():
    FLAG_STRIP_UNLIKELYS = 0x1
    FLAG_WEIGHT_CLASSES = 0x2
    FLAG_CLEAN_CONDITIONALLY = 0x4
    _status = ""
    _doc = None
    _articleTitle = None
    _uri = None
    _articleDir = None
    _articleByline = None
    DEFAULT_TAGS_TO_SCORE = "section,h2,h3,h4,h5,h6,p,td,pre".split(",")
    DIV_TO_P_ELEMS = [ "a", "blockquote", "dl", "div", "img", "ol", "p", "pre", "table", "ul", "select" ]
    ALTER_TO_DIV_EXCEPTIONS = ["div", "article", "section", "p"]
    
    _headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    Patter_unlikelyCandidates =  re.compile(r'banner|breadcrumbs|combx|comment|community|cover-wrap|disqus|extra|foot|header|legends|menu|modal\
    |related|remark|replies|rss|shoutbox|sidebar|skyscraper|social|sponsor|supplemental|ad-break|agegate|pagination|pager|popup|yom-remote|dropdown|dropdown-menu',flags = re.IGNORECASE)
    Patter_okMaybeItsACandidate = re.compile(r'and|article|body|column|main|shadow', flags = re.IGNORECASE)
    Patter_positive =  re.compile(r'article|body|content|entry|hentry|h-entry|main|page|pagination|post|text|blog|story', flags= re.IGNORECASE)
    Patter_negative = re.compile(r'hidden|^hid$| hid$| hid |^hid |banner|combx|comment|com-|contact|foot|footer|footnote|masthead|media|meta|modal\
    |outbrain|promo|related|scroll|share|shoutbox|sidebar|skyscraper|sponsor|shopping|tags|tool|widget', flags= re.IGNORECASE)
    Patter_extraneous = re.compile(r'print|archive|comment|discuss|e[\-]?mail|share|reply|all|login|sign|single|utility', flags = re.IGNORECASE)
    Patter_byline = re.compile(r'byline|author|dateline|writtenby|p-author', flags = re.IGNORECASE)
    Patter_replaceFonts = re.compile(r'<(\/?)font[^>]*>', flags = re.IGNORECASE)
    Patter_normalize= re.compile(r'\s{2,}', flags = re.IGNORECASE)
    Patter_videos= re.compile(r'\/\/(www\.)?(dailymotion|youtube|youtube-nocookie|player\.vimeo)\.com', flags = re.IGNORECASE)
    Patter_nextLink = re.compile(r'(next|weiter|continue|>([^\|]|$)|Â»([^\|]|$))', flags = re.IGNORECASE)
    Patter_prevLink = re.compile(r'(prev|earl|old|new|<|Â«)', flags = re.IGNORECASE)
    Patter_whitespace = re.compile(r'^\s*$', flags = re.IGNORECASE)
    Patter_hasContent = re.compile(r'\S$', flags = re.IGNORECASE)
     
    def __init__(self,url, *args, **kwargs):
        self._uri = urlparse(url)
        try:
            r = requests.get(url,timeout=5,headers = self._headers )
            if r.status_code == requests.codes.ok:
                self._doc = BeautifulSoup(r.text,"html5lib")
                self._flags = self.FLAG_STRIP_UNLIKELYS | self.FLAG_WEIGHT_CLASSES | self.FLAG_CLEAN_CONDITIONALLY;
            else:
                self._status = "Http Exception code " + str(r.status_code)
                print(("Unable to fetch the article status ", r.status_code));
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            self._status = "Request timeout!!!"
            pass
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            self._status = "Too many redirects!!!"
            pass
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            self._status = "Not able to fetch, SSL Error!!!"
            print(e)

    def _flagIsActive(self,flag):
            return (self._flags & flag) > 0;

    def _addFlag(self, flag):
        self._flags = self._flags | flag;

    def _removeFlag(self, flag):
        self._flags = self._flags & ~flag;

    def _nextElement(self, node):
       """
         /**
           * Finds the next element, starting from the given node, and ignoring
           * whitespace in between. If the given node is an element, the same node is
           * returned.
           */
       """
       next = node;
       while (next and  (type(next) != bs_element.Tag)):
           next = next.next_sibling;
       return next;

    def _getAllNodesWithTag(self, node, tagNames):
        
        node_list = []
        
        for tag in tagNames:
            node_list += node.find_all(tag) 
        
        return node_list

    def _removeTag(self, data, tag):
        for s in data(tag):
            s.extract()
        return

    def _checkByLine(self, node, matchstring):
        if (self._articleByline):
            return False;
        rel = node.get("rel", None);
        if (rel and (rel == "author" or self.Patter_byline.search(matchString)) and self.isValidByLine(node.string)):
            self._articleByline = node.string.strip();
            return True;
    
        return False;

  
    def _getInnerText(self, e, normalizeSpaces= False):
        """
        /**
           * Get the inner text of a node - cross browser compatibly.
           * This also strips out any excess whitespace to be found.
           *
           * @param Element
           * @param Boolean normalizeSpaces (default: True)
           * @return string
          **/
        """
        
        textContent = e.get_text().strip();

        if (normalizeSpaces):
            return self.Patter_normalize.sub(" ", textContent);
        
        return textContent;

 

    def _checkByLine(self, node, matchstring):
        """
        
        """
        if (self._articleByline):
            return False;
        
        rel = node.get("rel", None);
        if (rel and (rel == "author" or self.Patter_byline.search(matchstring)) and self.isValidByLine(node.string)):
            self._articleByline = node.string.strip();
            return True;
    
        return False;

    
    
    def isValidByLine(self, byline):
        """
        Check validity
        """
        if (isinstance(byline, str)):
            byline = byline.strip();
            return (len(byline) > 0) and (len(byline) < 100)
        return False;


    def _getRowAndColumnCount(self, table):
        """
          /**
           * Return an object indicating how many rows and columns this table has.
           */
        """
        rows = 0;
        columns = 0;
        trs = table.find_all("tr");
        for i in range(0, len(trs)):
            rowspan = trs[i].get("rowspan", 0);
            if (rowspan):
                rowspan = int(rowspan);
                rows = rows + rowspan
            else:
                rows += 1;
            
            ## Now look for column-related info
            columnsInThisRow = 0;
            cells = trs[i].find_all("td");
            for j in range( 0, len(cells)):
                colspan = cells[j].get("colspan", 0);
                if (colspan):
                    colspan = int(colspan);
                
                columnsInThisRow += (colspan or 1);
            
            columns = max(columns, columnsInThisRow);
        
        return {"rows": rows, "columns": columns};



    def _markDataTables(self, root):
       """
       
          /**
           * Look for 'data' (as opposed to 'layout') tables, for which we use
           * similar checks as
           * https://dxr.mozilla.org/mozilla-central/rev/71224049c0b52ab190564d3ea0eab089a159a4cf/accessible/html/HTMLTableAccessible.cpp#920
           */
       """
       tables = root.find_all("table");
       for i in range(0, len(tables)):
           table = tables[i];
           role = table.get("role", None);
           if (role and role == "presentation"):
               table['readabilityDataTable'] = False
               continue;
           
           datatable = table.get("datatable", None);
           if (datatable and datatable == "0"):
               table['readabilityDataTable'] = False;
               continue;
           
           summary = table.get("summary", None);
           if (summary):
               table['readabilityDataTable'] = True;
               continue;
           
           
           caption = table.find("caption");
           if (caption and len(caption.contents) > 0):
               table['readabilityDataTable'] = True;
               continue;
           
           
           ## If the table has a descendant with any of these tags, consider a data table:
           dataTableDescendants = ["col", "colgroup", "tfoot", "thead", "th"];
           descendantExists = any( True for x in dataTableDescendants if len(table.find_all(x)) > 0 );
           
           if (descendantExists):
               print("Data table because found data-y descendant");
               table['readabilityDataTable'] = True;
               continue;
           
           
           ## Nested tables indicate a layout table:
           if (table.find("table")):
               table['readabilityDataTable'] = False;
               continue;
           
           
           sizeInfo = self._getRowAndColumnCount(table);
           if (sizeInfo['rows'] >= 10 or sizeInfo['columns'] > 4):
               table['readabilityDataTable'] = True;
               continue;
           
           ## Now just go by size entirely:
           table['readabilityDataTable'] = sizeInfo['rows'] * sizeInfo['columns'] > 10;
        
   


    
    def _isElementWithoutContent(self,node):
        return (type(node) is not bs_element.NavigableString and
        type(node.string) is bs_element.NavigableString and  len(node.string.strip()) == 0 and
        (len(node.contents) == 0 or
         all(False for x in node.descendants if x.name == 'br' or x.name == 'hr')))


    def _hasSinglePInsideElement(self, element):
        """
           * Check if this node has only whitespace and a single P element
           * Returns False if the DIV node contains non-empty text nodes
           * or if it contains no P or more than 1 element.
           *
           * @param Element
        """
        ##There should be exactly 1 element child which is a P:
        if (len(element.contents) != 1 or self._nextElement(element.contents[0]) is None or   self._nextElement(element.contents[0]).name != "p"):
            return False;
    

        ## And there should be no text nodes with real content
        def is_text(node):
            return type(node) is bs_element.NavigableString and self.Patter_hasContent.search(node.string) is not None
        
        return (any(False for x in element.children if is_text(x) is True))

    def _hasChildBlockElement(self, element):
        """
          /**
           * Determine whether element has any children block level elements.
           *
           * @param Element
           */
        """
        return any( True for x in element.descendants if x.name in self.DIV_TO_P_ELEMS)

    def _cleanMatchedNodes(self, e, regex):
        """
          /**
           * Clean out elements whose id/class combinations match specific string.
           *
           * @param Element
           * @param RegExp match id/class combination.
           * @return void
           **/
           Find the decendants of this node and check for match. if found then decompose the tag
        """
        if e.decendants is None:
            return
        for node in e.decendants:
            if node is not bs_element.Tag:
                continue
            if (regex.search(node['class'] + " " + node['id'])):
                node.extract()

    def _cleanHeaders(self, e):
        """
          /**
           * Clean out spurious headers from an Element. Checks things like classnames and link density.
           *
           * @param Element
           * @return void
          **/
        """
        h1s = e.find_all('h1')
        
        for h in h1s:
            if self._getClassWeight(h) < 0:
                h.extract()

        h2s = e.find_all('h2')
        
        for h in h2s:
            if self._getClassWeight(h) < 0:
                h.extract()
                

    def _getClassWeight(self, e):
        """
          /**
           * Get an elements class/id weight. Uses regular expressions to tell if this
           * element looks good or bad.
           *
           * @param Element
           * @return number (Integer)
          **/
        """
        if (self._flagIsActive(self.FLAG_WEIGHT_CLASSES) is False):
            return 0;

        weight = 0;
    
        ## Look for a special classname
        if (self.Patter_negative.search(" ".join(e.get('class', [])))):
            weight -= 25;
    
        if (self.Patter_positive.search(" ".join(e.get('class', [])))):
            weight += 25;
    
        ## Look for a special ID
        if (self.Patter_negative.search(e.get('id', ""))):
            weight -= 25;
    
        if (self.Patter_positive.search(e.get('id', ""))):
            weight += 25;
    
        return weight;

        
        
    def _initializeNode(self, node):
        """
          /**
           * Initialize a node with the readability object. Also checks the
           * className/id for special names to add to its score.
           *
           * @param Element
           * @return void
          **/
        """
        contentScore = 0

        if node.name == 'div':
            contentScore += 5;
        elif node.name == 'blockquote':
            contentScore += 3;
        elif node.name == 'form':
            contentScore -= 3;
        elif node.name == 'th':
            contentScore -= 5;

        contentScore += self._getClassWeight(node)

        return {'score':contentScore, 'node': node}
 
    def _clean(self, e, tag):
        """
           /**
           * Clean a node of all elements of type "tag".
           * (Unless it's a youtube/vimeo video. People love movies.)
           *
           * @param Element
           * @param string tag to clean
           * @return void
           **/
        """
        if tag in ["object", "embed", "iframe"]:
            isEmbed = True
        else:
            isEmbed = False

        nodes = e.find_all(tag)
        
        for node in nodes:
            if(isEmbed):
                attributes = node.attrs
                attributeValues = "|".join(attributes)
                
                if self.Patter_videos.search(attributeValues):
                    continue
                
                if self.Patter_videos.search(str(node)):
                    continue
                
                ## reached here it means remove it
                nodestring = " ".join(node.get('class', [])) + " " + node.get('id', " ");
                print(('cleaning node ', nodestring, ' as no embed info found'))
                node.extract()


    def _getLinkDensity(self, element):
        """
          /**
           * Get the density of links as a percentage of the content
           * This is the amount of text that is inside a link divided by the total text in the node.
           *
           * @param Element
           * @return number (float)
          **/
        """
        textLength =len(element.get_text());
        if (textLength == 0):
            return 0;
        
        linkLength = 0;
        
        ## XXX implement _reduceNodeList?
        for linkNode in element.find_all("a"):
            linkLength += len(linkNode.get_text());

        
        return linkLength / textLength;

    def  _hasAncestorTag(self, node, tagName, maxDepth= 3, filterFn=False):
        depth = 0;
        while (node.parent):
            if (maxDepth > 0 and depth > maxDepth):
                return False;
            if (node.parent.name == tagName and (filterFn is None
                                                 or filterFn)):
                return True;
            node = node.parent;
            depth += 1;

        return False;
    


    def _cleanConditionally(self, e, tag):
       """
         /**
           * Clean an element of all tags of type "tag" if they look fishy.
           * "Fishy" is an algorithm based on content length, classnames, link density, number of images & embeds, etc.
           *
           * @return void
           **/
       """
       if (self._flagIsActive(self.FLAG_CLEAN_CONDITIONALLY) is False):
          return;
    
       isList = tag == "ul" or tag == "ol";
    
       ## Gather counts for other typical elements embedded within.
       ## Traverse backwards so we can remove nodes at the same time
       ## without effecting the traversal.
       ##
       ## TODO: Consider taking into account original contentScore here.
       
       try:
           nodes = e.find_all(tag)
           for node in nodes:
               if node is None:
                   continue
               
               if type(node) is not bs_element.Tag:
                   continue
               ## First check if we're in a data table, in which case don't remove us.
               
               
               isDataTable = node.get('readabilityDataTable', None);
               
               if (self._hasAncestorTag(node, "table", -1, isDataTable)):
                   continue
               
               matchString = " ".join(node.get('class', [])) + " " + node.get('id', " ");

                
               weight = self._getClassWeight(node);

               if (weight  < 0):
                   print(("Cleaning Conditionally as weight is negative ", matchString ));
                   node.extract()
                   continue
    
        
               if (node.get_text().count(',') < 10):
                   ## If there are not very many commas, and the number of
                   ## non-paragraph elements is more than paragraphs or other
                   ## ominous signs, remove the element.
                   p = len(node.find_all("p"));
                   img = len(node.find_all("img"));
                   li = len(node.find_all("li")) - 100;
                   input = len(node.find_all("input"));
        
                   embedCount = 0;
                   embeds = node.find_all(attrs={"name" : "embed"});
                   for ei in range(0, len(embeds)):
                       if (self.Patter_videos.search(embeds[ei]['src']) is not None):
                           embedCount += 1;
                   
                   linkDensity = self._getLinkDensity(node);
                   contentLength = len(node.get_text());
                   haveToRemove = (img > 1 and p / img < 0.5 and self._hasAncestorTag(node, "figure") is False)  or \
                                    (isList is False and li > p) or \
                                    (input > math.floor(p/3)) or \
                                    (isList is False and contentLength < 25 and (img == 0 or img > 2) and self._hasAncestorTag(node, "figure") is False) or \
                                    ( isList is False and weight < 25 and linkDensity > 0.2) or \
                                    (weight >= 25 and linkDensity > 0.5) or \
                                    ((embedCount == 1 and contentLength < 75) or embedCount > 1);
                   if(haveToRemove):
                       print(("Cleaning Conditionally as this doesn't seem like valid content ", matchString ));
                       node.extract()
                       continue
       except:
           print("Something wrong in _cleanConditionally")
           pass
       return
    
    def _replaceBrs(self, content):
        '''
        IMplement it later
        '''
        ## fetch the first br element
        br = content.br
        replace_br = False
        node = self._getNextTag(br)
        while(node is not None):
            if node.name == 'br':
                pass    
         
    def _replaceNodeTags(self, node, tag):
        if isinstance(node, collections.MutableSequence):
            for s in node:
                s.name = tag
        else:
            node.name = tag
         
    def _removeScripts(self,data):
        '''
        Removes script tags from the document.
        '''
       
        self._removeTag(data, "script")
        self._removeTag(data, "noscript")
     
    def _prepDocument(self):
        """
        Prepare the HTML document for readability to scrape it.
        This includes things like stripping javascript, CSS, and handling terrible markup.
        """
        ## Remove all style tags in head
        self._removeTag(self._doc, 'style')
#         if(self._doc.body):
#             self._replaceBrs(self._doc.body)
         
        self._replaceNodeTags(self._doc.find_all('font'), 'span')
         
    def _getArticleTitle(self):
        """
        Get the article title as an H1.
        """
        curTitle = "";
        origTitle = "";
 
        try:
          curTitle = origTitle = self._doc.title.string;
          ## If they had an element with id "title" in their HTML
        except:
            pass
 
        titleHadHierarchicalSeparators = False;
         
        def wordCount(str):
            return len(str.split(r'\s+'));
         
 
        ## If there's a separator in the title, first remove the final part
        if (re.search(r'[\|\-\\\/>Â»]' , curTitle)):
            
            titleHadHierarchicalSeparators = re.search(r'[\\\/>Â»]',curTitle);
            pattern = re.compile(r'(.*)[\|\-\\\/>Â»] .*',re.IGNORECASE)
            curTitle = pattern.sub('\1',origTitle)
 
            ## If the resulting title is too short (3 words or fewer), remove
            ## the first part instead:
            if (wordCount(curTitle) < 3):
                pattern = re.compile(r'[^\|\-\\\/>Â»]*[\|\-\\\/>Â»](.*)',re.IGNORECASE)
                curTitle = pattern.sub('\1',origTitle)

        elif (': ' in curTitle ):
            ## Check if we have an heading containing this exact string, so we
            ## could assume it's the full title.
            
            headings = self._doc.find_all('h1') + self._doc.find_all('h2') 
            match = any([True for x in headings if x.string == curTitle ])
            ## If we don't, let's extract the title out of the original title string.
            if (match == False):
                curTitle = origTitle[origTitle.rindex(':') + 1 :-1]
                ## If the title is now too short, try the first colon instead:
                if (wordCount(curTitle) < 3):
                    curTitle = origTitle[origTitle.index(':') + 1 :-1]
            
        elif (len(curTitle) > 150 or len(curTitle) < 15):
            hOnes = self._doc.find_all('h1')
            if (len(hOnes) == 1):
                curTitle = hOnes[0].string;
           
 
        curTitle = curTitle.strip();
        ## If we now have 4 words or fewer as our title, and either no
        ## 'hierarchical' separators (\, /, > or Â») were found in the original
        ## title or we decreased the number of words by more than 1 word, use
        ## the original title.
        curTitleWordCount = wordCount(curTitle);
        pattern = re.compile(r'[\|\-\\\/>Â»]+')
        tmp = pattern.sub('',origTitle)

        if (curTitleWordCount <= 4 and
            (titleHadHierarchicalSeparators  is None or
             curTitleWordCount != wordCount(tmp) - 1)):
            curTitle = origTitle;
        
        
        return curTitle;
    def _nodeString(self, node):
        if(node):
            return " ".join(node.get('class', [])) + " " + node.get('id', " ");
        
 
    def _getArticleMetadata(self):
        """
        Attempts to get excerpt and byline metadata for the article.
        """
        metadata = {}
        values = {}
        metaelements = self._doc.find_all('meta')
         
        ## Match "description", or Twitter's "twitter:description" (Cards)
        ## in name attribute.
        namePattern = re.compile('^\s*((twitter)\s*:\s*)?(description|title)\s*$', flags=re.IGNORECASE)
         
        ## Match Facebook's Open Graph title & description properties.
        propertyPattern = re.compile('^\s*og\s*:\s*(description|title)\s*$', flags=re.IGNORECASE)
         
        for ele in metaelements:
            elementName = ele.get('name', None)
            elementProperty = ele.get('property', None) 
 
            ## if author is present in name or property
            ## set the byline with its content and continue
            if "author" in [elementName, elementProperty]:
                metadata['byline'] = ele['content']
                continue
             
            name = None
            if(elementName and namePattern.search(elementName)):
                name = elementName
            elif (elementProperty and propertyPattern.search(elementProperty)):
                name = elementProperty
                 
            if(name):
                content = ele['content']
                if(content):
                    name = name.lower()
                    name = name.replace('\s', '')
                    values[name] = content.strip();
 
        if ("description" in values):
            metadata['excerpt'] = values["description"]
             
        elif ("og:description" in values):
            ## Use facebook open graph description.
            metadata['excerpt'] = values["og:description"]
        elif ("twitter:description" in values):
            ## Use twitter cards description.
            metadata['excerpt'] = values["twitter:description"]
             
        metadata['title'] = self._getArticleTitle()
         
        if (metadata['title'] is None): 
            if ("og:title" in values):
                ## Use facebook open graph title.
                metadata['title']  = values["og:title"]
        elif ("twitter:title" in values):
            ## Use twitter cards title.
            metadata['title']  = values["twitter:title"];
     
        return metadata;                
                     
    
    def _getScore(self, node, candidates):
        candidate = candidates.get(hash(str(node)),None)
        if candidate:
            return candidate['score']
        else:
            return None
        
 
     
    def _grabArticle(self, page):
        
        print("**** grabArticle ****");
        ## We can't grab an article if we don't have a page!
        if (page is None):
            print("No body found in document. Abort.")
            return null;
        
        pageCacheHtml = str(page);

        while (True):
                     
            ## First, node prepping. Trash nodes that look cruddy (like ones with the
            ## class name "comment", etc), and turn divs into P tags where they have been
            ## used inappropriately (as in, where they contain no other block level elements.)
            
            stripUnlikelyCandidates = self._flagIsActive(self.FLAG_STRIP_UNLIKELYS);
            elementsToScore = [];
            
#             print("*** searching on page decendants*******")         
            for node in  page.find_all(True):
#                 print("**** Analysing node ", type(node), " *****")
                if type(node) is not bs_element.Tag:
                    continue
                
                for element in node(text=lambda text: isinstance(text, Comment)):
                    element.extract()
                
                matchString = " ".join(node.get('class', [])) + " " + node.get('id', " ");
                ## Check to see if this node is a byline, and remove it if it is.
                if (self._checkByLine(node, matchString)):
#                     print("Removing unlikely candidate - " + matchString);
                    node.extract()
                    continue;
        
                ## Remove unlikely candidates
                if (stripUnlikelyCandidates):
                    if (self.Patter_unlikelyCandidates.search(matchString) and
                        not self.Patter_okMaybeItsACandidate.search(matchString) and
                        node.name != "body" and node.name != "a"):
#                         print("Removing unlikely candidate - " + matchString);
                        node.extract()
                        continue;
                
        
                ## Remove DIV, SECTION, and HEADER nodes without any content(e.g. text, image, video, or iframe).
                if ((node.name == "div" or node.name == "section" or node.name == "header" or
                     node.name == "h1" or node.name == "h2" or node.name == "h3" or
                     node.name == "h4" or node.name == "h5" or node.name == "h6") and
                    self._isElementWithoutContent(node)):
#                     print("Removing unlikely candidate - " + matchString);
                    node.extract()
                    continue;
                
        
                if ( node.name in self.DEFAULT_TAGS_TO_SCORE):
#                     print("**** appending node to elementsToScore*****")
#                     print(type(node))
                    elementsToScore.append(node);
                    continue
                
        
                ## Turn all divs that don't have children block level elements into p's
                if (node.name == "div"):
                    ## Sites like http://mobile.slate.com encloses each paragraph with a DIV
                    ##element. DIVs with only a P element inside and no text content can be
                    ## safely converted into plain P elements to avoid confusing the scoring
                    ## algorithm with DIVs with are, in practice, paragraphs.
                    if (self._hasSinglePInsideElement(node)):
                        node.unwrap();
                    elif (self._hasChildBlockElement(node) is False):
                        self._replaceNodeTags(node, "p");
#                         print("**** appending node to elementsToScore*****")
#                         print(type(node))
                        elementsToScore.append(node);
                
                ## end of for loop
        
            ## Loop through all paragraphs, and assign a score to them based on how content-y they look.
            ## Then add their score to their parent node.
            ##
            ## A score is determined by things like number of commas, class names, etc. Maybe eventually link density.
            ##
            candidates = {};
#             print("**** Analysing elementsToScore *****")
            for node in elementsToScore:
                if node is None:
                    continue

                parentNode = node.parent
                grandParentNode = parentNode.parent
                                              
                if (node.parent is None):
#                     print("Node parent is null continue ", node.name)
                    continue

                ## If this paragraph is less than 25 characters, don't even count it.
                innerText = node.get_text();
                if (len(innerText) < 25):
#                     print("Node text is less than 25 ", node.name)
                    continue

                ancestors = self._getNodeAncestors(node,3)
                if (len(ancestors) == 0):
                    continue;

                contentScore = 1
                contentScore += innerText.count(',')
                contentScore += innerText.count('，')
                contentScore +=  min(math.floor(len(innerText) / 100), 3)

                def scoreNode(ance, level):
                    if(ance is None or type(ance) is not bs_element.Tag):
                        return
                    nodeHash = hash(str(ance))
                    
                    if nodeHash not in candidates:
                        candidates[nodeHash] = self._initializeNode(ance)
#                         print('candidate ', self._nodeString(ance), ' initialized with score ', candidates[nodeHash]['score'])
                    scoreDivider = 1;
                    if level == 0:
                        scoreDivider = 1;
                    elif level == 1:
                        scoreDivider = 2;
                    else:
                        scoreDivider = level* 3;
                    
                    candidates[nodeHash]['score'] = candidates[nodeHash]['score'] +  (contentScore / scoreDivider)
#                     print('candidate added ', self._nodeString(ance), ' with score ', candidates[nodeHash]['score'])
                    
                for i in range(0, len(ancestors)):
                    scoreNode(ancestors[i], i)
        
            ## After we've calculated scores, loop through all of the possible
            ## candidate nodes we found and find the one with the highest score.
            topCandidates = [];
            cl = len(candidates)
#             print("**** Canidates found ", cl , "**********"  )
            if (cl == 0):
                page = BeautifulSoup(pageCacheHtml, "html5lib");
                if (self._flagIsActive(self.FLAG_STRIP_UNLIKELYS)):
                    self._removeFlag(self.FLAG_STRIP_UNLIKELYS);
                    continue
                elif (self._flagIsActive(self.FLAG_WEIGHT_CLASSES)):
                    self._removeFlag(self.FLAG_WEIGHT_CLASSES);
                    continue
                elif (self._flagIsActive(self.FLAG_CLEAN_CONDITIONALLY)):
                    self._removeFlag(self.FLAG_CLEAN_CONDITIONALLY);
                    continue
                else:
                  return None;

            
            
            for key in candidates:
    #             print '======================='
    #             print self.candidates[key]['score']
    #             print self.candidates[key]['node']
    
                candidates[key]['score'] = candidates[key]['score'] * \
                                                (1 - self._getLinkDensity(candidates[key]['node']))

                inserted = False
                
                for t in range(0, len(topCandidates)):
                    if topCandidates[t]['score'] < candidates[key]['score']:
                        topCandidates.insert(t, candidates[key])
                        inserted = True
                        break
                    elif topCandidates[t]['score'] == candidates[key]['score'] and \
                     len(topCandidates[t]['node'].get_text()) <   len(candidates[key]['node'].get_text()):
                        topCandidates.insert(t, candidates[key])
                        inserted = True
                        break
                        
                        
                if inserted == False:
#                     print(candidates[key]);
                    topCandidates.insert(len(topCandidates), candidates[key])
            
#             print('Top 5 candidates are')
#             count = 0
#             for cd in topCandidates:
#                 if(count > 5 or cd is None):
#                     break
#                 else:
#                     nodestring = " ".join(cd['node'].get('class', [])) + " " + cd['node'].get('id', " ");
#                     parentstring = " ".join(cd['node'].parent.get('class', [])) + " " + cd['node'].parent.get('id', " ");
#                     print(nodestring , " with score ", str(cd['score']),
#                     "parent ", parentstring, " ********"  )
#                     count  += 1
            
#             print("**** Top Canidate found ", self._nodeString(topCandidates[0]['node']) , " with score ", str(topCandidates[0]['score']))
#             print(topCandidates[0])
            topCandidate = topCandidates[0];
            neededToCreateTopCandidate = False;
            parentOfTopCandidate = None;
        
            ## If we still have no top candidate, just use the body as a last resort.
            ## We also have to copy the body node so it is something we can modify.
            if (topCandidate == None or topCandidate['node'].name == "body"):
                ## Move all of the page's children into topCandidate
                topCandidate['node'] = self._doc.new_tag("div");
                neededToCreateTopCandidate = True;
                ## Move everything (not just elements, also text nodes etc.) into the container
                ## so we even include text directly in the body:
                kids = page.descendants;
                for kid in kids:
#                     print("Moving child out:", kid);
                    topCandidate['node'].append(kid);
                
    
                page.append(topCandidate['node']);
                topCandidate = self._initializeNode(topCandidate['node']);
            elif (topCandidate):
                try:
                    ## Find a better top candidate node if it contains (at least three) nodes which belong to `topCandidates` array
                    ## and whose scores are quite closed with current `topCandidate` node.
                    alternativeCandidateAncestors = [];
                    for i in range(1,len(topCandidates)):
                        if ((topCandidates[i]['score'] / topCandidate['score']) >= 0.75):
                            alternativeCandidateAncestors.append([ hash(str(x)) for x in topCandidates[i]['node'].parents]);
                    MINIMUM_TOPCANDIDATES = 3;
#                     print("Alternate candidates founb ", len(alternativeCandidateAncestors))
                    if (len(alternativeCandidateAncestors) >= MINIMUM_TOPCANDIDATES):
                        parentOfTopCandidate = topCandidate['node'].parent;
                        while (parentOfTopCandidate is not None and parentOfTopCandidate.name != "body"):
                            listsContainingThisAncestor = 0;
                            for ancestorIndex in range(0, len(alternativeCandidateAncestors)):
                                listsContainingThisAncestor +=alternativeCandidateAncestors[ancestorIndex].count(hash(str(parentOfTopCandidate)));
                            
                            if (listsContainingThisAncestor >= MINIMUM_TOPCANDIDATES):
                                topCandidate['node'] = parentOfTopCandidate;
                                if( hash(str(parentOfTopCandidate)) in candidates):
                                    topCandidate['score'] = candidates[hash(str(parentOfTopCandidate))]['score']
                                break;
                            
                            parentOfTopCandidate = parentOfTopCandidate.parent;
                            
                        
                    if (topCandidate.get('score',None) is None):
#                         print("Initialize new top candidate score")
                        topCandidate = self._initializeNode(topCandidate['node']);
                        
                    nodestring = " ".join(topCandidate['node'].get('class', [])) + " " + topCandidate['node'].get('id', " ");
#                     print("***Now top Candidate is ", nodestring, " score ", topCandidate.get('score',None))
#                     print(topCandidate)
                    ## Because of our bonus system, parents of candidates might have scores
                    ## themselves. They get half of the node. There won't be nodes with higher
                    ## scores than our topCandidate, but if we see the score going *up* in the first
                    ## few steps up the tree, that's a decent sign that there might be more content
                    ## lurking in other places that we want to unify in. The sibling stuff
                    ## below does some of that - but only if we've looked high enough up the DOM
                    ## tree.
                    parentOfTopCandidate = topCandidate['node'].parent;
                    lastScore = topCandidate['score'];
                    ## The scores shouldn't get too low.
                    scoreThreshold = lastScore / 3;
                    while (parentOfTopCandidate and parentOfTopCandidate.name != "body"):
                        
                        if ( hash(str(parentOfTopCandidate)) not in candidates):
                            parentOfTopCandidate = parentOfTopCandidate.parent;
                            continue;
                        
                        parentScore = self._getScore(parentOfTopCandidate, candidates);
#                         print('parent found ', self._nodeString(parentOfTopCandidate), ' with score ', parentScore, ' threshold ', scoreThreshold,
#                                ' lastScore ', lastScore)
                        
                        if (parentScore < scoreThreshold):
                            break;
                        if (parentScore > lastScore):
#                             print('Founb new top ', self._nodeSting(parentOfTopCandidate), ' score ', parentScore)
                            topCandidate = {'node' : parentOfTopCandidate, 'score': parentScore };
                            break;
                        
                        lastScore = parentScore;
                        parentOfTopCandidate = parentOfTopCandidate.parent;
            
                    ## If the top candidate is the only child, use parent instead. This will help sibling
                    ## joining logic when adjacent content is actually located in parent's sibling node.
                    parentOfTopCandidate = topCandidate['node'].parent;
                    while (parentOfTopCandidate and parentOfTopCandidate.name != "body" and len(parentOfTopCandidate.contents) == 1 and
                           hash(str(parentOfTopCandidate)) in candidates ):
                        topCandidate = {'node': parentOfTopCandidate, 'score': self._getScore(parentOfTopCandidate, candidates)};
                        parentOfTopCandidate = topCandidate['node'].parent;
                    
                    
                    if (topCandidate.get('score',None) is None):
#                         print('initialize new top ', self._nodeString(topCandidate['node']))
                        topCandidate = self._initializeNode(topCandidate['node']);
                        
                except:
                    print("Exception in finding alternate top candidate:")
                    print('-'*60)
                    traceback.print_exc(file=sys.stdout)
                    print('-'*60)
                    sys.exc_clear()
                    

#             print("***Now top Candidate is ", self._nodeString(topCandidate['node']), " score ", topCandidate.get('score',None))
#             print(topCandidate)
            ## Now that we have the top candidate, look through its siblings for content
            ## that might also be related. Things like preambles, content split by ads
            ## that we removed, etc.
            articleContent = self._doc.new_tag("div");
            articleContent['id'] = "readability-content";
    
#             articleContent.append(topCandidate)
            siblingScoreThreshold = max(10, int(topCandidate['score']) * 0.2);
            
            ## Keep potential top candidate's parent node to try to get text direction of it later.
            parentOfTopCandidate = topCandidate['node'].parent;
#             print('Checking the children for parent of top ', self._nodeString(parentOfTopCandidate))
            siblings  = parentOfTopCandidate.contents
            for sibling in siblings:
                
                if type(sibling) is not bs_element.Tag or sibling.name == 'None':
                    continue
#                 print(type(sibling), sibling.name)
#                 print('childrens are ', [self._nodeString(x) for x in siblings if type(x) is bs_element.Tag])
                append = False;
#                 print('sibling ', self._nodeString(sibling))
                if (sibling == topCandidate['node']):
                    print("Sibling is top candidate append it")
                    append = True;
                else:
                    contentBonus = 0;
                    ## Give a bonus if sibling nodes and top candidates have the example same classname
                    sibling_class = sibling.get('class',[])
                    top_class =  topCandidate['node'].get('class', [])
                    sibling_score_exist = candidates.get(hash(str(sibling)), None)
                    for cls in sibling_class:
                        if cls in top_class:
                            contentBonus += int(topCandidate['score']) * 0.2
                            break
                    
                    if (sibling_score_exist and
                      ((candidates.get(hash(str(sibling)))['score'] + contentBonus) >= siblingScoreThreshold)):
                        print('Sibling score is compareble so append it')
                        append = True;
                    elif (sibling.name == "p"):
                        linkDensity = self._getLinkDensity(sibling);
                        nodeContent = sibling.get_text().encode('utf-8');
                        nodeLength = len(nodeContent)
        
                        if (nodeLength > 80 and linkDensity < 0.25):
                            append = True;
                            print('Sibling is p with valid length and link density, so append it')
                        elif (nodeLength < 80 and nodeLength > 0 and linkDensity == 0 and
                               re.search('\.( |$)', nodeContent) is not None):
                            print('Sibling is p with valid data appending it')
                            append = True
                if (append):
                    print(("Appending node:", self._nodeString(sibling), " score ", self._getScore(sibling, candidates)));
                    if ( sibling.name not in self.ALTER_TO_DIV_EXCEPTIONS):
                        ## We have a node that isn't a common block level element, like a form or td tag.
                        ## Turn it into a div so it doesn't get filtered out later by accident.
#                         print("Altering sibling:", sibling.name, 'to div.')
                        sibling.name = "div"
                    articleContent.append(copy.copy(sibling))
                    continue

        
                
#             print("Article content pre-prep: ", str(articleContent));
            ## So we have all of the content that we need. Now we clean it up for presentation.
            print("Now preping the Main content")
            self._prepArticle(articleContent);
#             print("Article content post-prep: " + str(articleContent));
        
            ## Now that we've gone through the full algorithm, check to see if
            ## we got any meaningful content. If we didn't, we may need to re-run
            ## grabArticle with different flags set. This gives us a higher likelihood of
            ## finding the content, and the sieve approach gives us a higher likelihood of
            ## finding the -right- content.
            if (len(articleContent.get_text()) < 500):
                page = BeautifulSoup(pageCacheHtml, "html5lib");
    
                if (self._flagIsActive(self.FLAG_STRIP_UNLIKELYS)):
                    self._removeFlag(self.FLAG_STRIP_UNLIKELYS);
                    continue
                elif (self._flagIsActive(self.FLAG_WEIGHT_CLASSES)):
                    self._removeFlag(self.FLAG_WEIGHT_CLASSES);
                    continue
                elif (self._flagIsActive(self.FLAG_CLEAN_CONDITIONALLY)):
                    self._removeFlag(self.FLAG_CLEAN_CONDITIONALLY);
                    continue
                else:
                    self._status = "Not able to find the relevant content"
                    return None;
                
            else:
                ## Find out text direction from ancestors of final top candidate.
                def set_dir(node):
                     articleDir = node.get("dir",None)
                     if(articleDir):
                         self._articleDir = articleDir;
                         return True
                     return False
                 
                any(set_dir(x) for x in topCandidate['node'].parents)
            return articleContent;

    def _getNodeAncestors(self, node, maxDepth = 0):
        i = 0
        ancestors = [];
        while (node.parent):
            ancestors.append(node.parent);
            i +=1
            if (maxDepth and i == maxDepth):
                break;
            node = node.parent;
        return ancestors;



     
    def _getFirstParagraph(self, articleContent):
        paragraphs = articleContent.find_all("p");
        
        for p in paragraphs:
            if (len(p.get_text()) > 0):
                return p.get_text().strip();
        
        return ""

    def _getFirstImage(self, data):
        try:
            matches = re.findall(
                r'(<img[^>].*?src\s*=\s*"([^"]+)")', data
            )
            if matches:
                return str(matches[0][1])
            else:
                return None
        except:
            print("Error in get_imageurl_from_data")
            pass
        
        return None

    def _fixRelativeUris(self, articleContent):
        """
          /**
           * Converts each <a> and <img> uri in the given element to an absolute URI,
           * ignoring #ref URIs.
           *
           * @param Element
           * @return void
           */
        """
        scheme = self._uri.scheme;
        prePath = self._uri.netloc;
        pathBase = self._uri.path;
        
        def toAbsoluteURI(uri):
            
            ## If this is already an absolute URI, return it.
            abs_uri = re.compile('^[a-zA-Z][a-zA-Z0-9\+\-\.]*:')
            
            if (abs_uri.search(uri)):
                return uri;
            
            ## Scheme-rooted relative URI.
            if (uri[0:2] == "//"):
                return scheme + "://" + uri[2:-1];
            
            ## Prepath-rooted relative URI.
            if (uri[0] == "/"):
                return scheme + "://" + prePath + uri;
            
            ## Dotslash relative URI.
            if (uri[0:2] == "./"):
                return pathBase + uri[2:-1];
            
            ## Ignore hash URIs:
            if (uri[0] == "#"):
                return uri;
            
            ## Standard relative URI; add entire path. pathBase already includes a
            ## trailing "/".
            return pathBase + uri;
        

        links = articleContent.find_all("a");
        for link in links:
            href = link.get("href", None);
            if (href):
                ## Replace links with javascript: URIs with text content, since
                ## they won't work after scripts have been removed from the page.
                if ("javascript:" in href):
                    text = self._doc.new_tag("span");
                    text.string = link.get_text()
                    link.parent.append(text);
                    link.extract()
                else:
                    link["href"] = toAbsoluteURI(href);
                
        imgs = articleContent.find_all("img");
        for img in imgs:
            src = img.get("src", None);
            if (src):
                img["src"] =  toAbsoluteURI(src);



    def _postProcessContent(self,content):
        """
          /**
           * Run any post-process modifications to article content as necessary.
           *
           * @param Element
           * @return void
          **/
        """
        ## Readability cannot open relative uris so we convert them to absolute uris.
        self._fixRelativeUris(content);

        pass

    def _prepArticle(self,articleContent):
       """
         /**
           * Prepare the article node for display. Clean out any inline styles,
           * iframes, forms, strip extraneous <p> tags, etc.
           *
           * @param Element
           * @return void
           **/
       """
#        self._cleanStyles(articleContent);
       
       for e in articleContent.findAll(True):
            for attribute in e.attrs:
                if attribute[0] == 'style':
                    del e[attribute[0]]

       ## Check for data tables before we continue, to avoid removing items in
       ## those tables, which will often be isolated even though they're
       ## visually linked to other content-ful elements (text, images, etc.).
       self._markDataTables(articleContent);
       
       ## Clean out junk from the article content
       self._cleanConditionally(articleContent, "form");
       self._cleanConditionally(articleContent, "fieldset");
       self._clean(articleContent, "object");
       self._clean(articleContent, "embed");
       self._clean(articleContent, "h1");
       self._clean(articleContent, "footer");
       
       ## Clean out elements have "share" in their id/class combinations from final top candidates,
       ## which means we don't remove the top candidates even they have "share".
       for topCandidate in articleContent.children:
           if type(topCandidate) is bs_element.Tag: 
               self._cleanMatchedNodes(topCandidate, "share");
       
       ## If there is only one h2 and its text content substantially equals article title,
       ## they are probably using it as a header and not a subheader,
       ## so remove it since we already extract the title separately.
       h2 = articleContent.find_all('h2');
       if (len(h2) == 1):
           lengthSimilarRate = (len(h2[0].get_text()) - len(self._articleTitle)) / len(self._articleTitle);
           if (math.fabs(lengthSimilarRate) < 0.5 and
               (self._articleTitle in h2[0].get_text() or 
                                   h2[0].get_text() in self._articleTitle)):
               self._clean(articleContent, "h2");
       self._clean(articleContent, "iframe");
       self._clean(articleContent, "input");
       self._clean(articleContent, "textarea");
       self._clean(articleContent, "select");
       self._clean(articleContent, "button");
       self._cleanHeaders(articleContent);
       
       ## Do these last as the previous stuff may have removed junk
       ## that will affect these
       self._cleanConditionally(articleContent, "table");
       self._cleanConditionally(articleContent, "ul");
       self._cleanConditionally(articleContent, "div");
       
       ## Remove extra paragraphs
       paragraphs = articleContent.find_all('p')
       for paragraph in paragraphs:
           imgCount = len(paragraph.find_all('img'));
           embedCount = len(paragraph.find_all('embed'));
           objectCount = len(paragraph.find_all('object'));
           
           ## At this point, nasty iframes have been removed, only remain embedded video ones.
           iframeCount = len(paragraph.find_all('iframe'));
           totalCount = imgCount + embedCount + objectCount + iframeCount;
           
           remove_cond =  totalCount == 0 and self._getInnerText(paragraph, False) is None;
           if(remove_cond):
               nodestring = " ".join(paragraph.get('class', [])) + " " + paragraph.get('id', " ");
               print(('Removing the paragraph ', nodestring, ' as no images or text'))
               paragraph.extract()
       
       for br in self._getAllNodesWithTag(articleContent, ["br"]):
           next = self._nextElement(br.next_sibling);
           if (next and next.name == "p"):
               print('removing br as next element is p')
               br.extract();

     
    def parse(self):
        """
        Runs readability.
        
        Workflow:
         1. Prep the document by removing script tags, css, etc.
         2. Build readability's DOM tree.
         3. Grab the article content from the current dom tree.
         4. Replace the current DOM tree with the new one.
         5. Read peacefully.
     
        """
         
        ## check if request was successfull or not
        if self._doc is None:
            return {'message': self._status, 'content': None}
         
        ## Remove script tags from the document.
        self._removeScripts(self._doc)
         
        ## prepare the document for processing
        self._prepDocument()
 
        ## extract the title
        metadata = self._getArticleMetadata();
        self._articleTitle = metadata['title'];
         
        print(('************Title ', self._articleTitle, ' ***************'))
        ## Grab the article content
        try:
            articleContent = self._grabArticle(self._doc.body);
            if articleContent is None:
                return {'message': self._status, 'content': None}
        except:
            print("Exception in user code:")
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            return {'message': "Parsing Error", 'content': None}
        
        
#         print('*******', type(articleContent), '**********')
        ## post processing
        self._postProcessContent(articleContent);
 
        ## If we haven't found an excerpt in the article's metadata, use the article's
        ## first paragraph as the excerpt. This is used for displaying a preview of
        ## the article's content.
        if (metadata.get('excerpt', None) is None ):
            metadata['excerpt'] = self._getFirstParagraph(articleContent)
         
        textContent = articleContent.get_text();
 
        return {
          'uri': self._uri.geturl(),
          'title': self._articleTitle,
          'byline': metadata.get('byline', False) or self._articleByline,
          'dir': self._articleDir,
          'content': str(articleContent),
          'textContent': textContent,
          'length': len(textContent),
          'excerpt': metadata.get('excerpt',None),
          'image': self._getFirstImage(str(articleContent)),
          }
 
         