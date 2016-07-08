'''
Post processing of data crawled by ``ReindeerBot`` of rekhta.com
'''
import requests
import tempfile
import difflib

from crawlers.models import RawArticle

def download_image(image_url):
    '''
    @summary: Returns image downloaded from `image_url`
    '''
    # Steam the image from the url
    request = requests.get(image_url, stream=True)

    # Was the request OK?
    if request.status_code != requests.codes.ok:
        # Nope, error handling, skip file etc etc etc
        print 'ERR: response is', request.status_code
        return False

    # Get the filename from the url, used for saving later
    file_name = image_url.split('/')[-1]

    # Create a temporary file
    lf = tempfile.NamedTemporaryFile()

    # Read the streamed image in sections
    for block in request.iter_content(1024 * 8):

        # If no more file then stop
        if not block:
            break

        # Write image block to temporary file
        lf.write(block)

    # Print details of file `lf`
    
    
    return lf


def get_poetry_img_url(poetry_url, language):
    '''
    @summary: Returns poetry image URL form ``poetry_url`` of language ``language`` 
    
    @note: ``poetry_url`` can be like 'https://rekhta.org/nazms/chand-roz-aur-mirii-jaan-faiz-ahmad-faiz-nazms?lang=hi'
    or 'https://rekhta.org/nazms/chand-roz-aur-mirii-jaan-faiz-ahmad-faiz-nazms'
    If ``language`` is 'hi', poetry image url will be 'https://rekhta.org/Images/UrduShayari/hi_chand-roz-aur-mirii-jaan-faiz-ahmad-faiz-nazms.png'
    '''
    
    base_url  = 'http://rekhta.org/Images/UrduShayari/'
    # I'm using http because https is giving SSLError, and I don't want to debug :P
         
    poetry_slug = poetry_url.split('/')[-1].split('?')[0]
    
    return base_url + language + '_' + poetry_slug + '.png'
    
    
def measure_similarity(str1, str2):
    '''
    @summary: Returns a float in [0, 1], measuring the similarity between two strings. 
    As a rule of thumb, a value over 0.6 means the strings are close matches.
    
    @note: https://docs.python.org/2/library/difflib.html
    '''
    
    d = difflib.SequenceMatcher(None, str1, str2)
    s = round(d.ratio(), 3)
    #print 'DBG: similarity is ', s
    return s


def _is_similar(str1, str2):
    s = measure_similarity(str1, str2)
    if s > 0.6: #TODO: increase the value if you are not getting correct output
        return True
    else:
        return False
    

def correct_poetry_lines_order(shuffled_lines, ocr_lines):
    ''' 
    @summary: Correct the line ordering of shuffled_lines
    
    @shuffled_lines: Individual lines are correct, and ordering of lines are incorrect.
    @ocr_lines: Individual lines are partially correct, and ordering of lines are correct. 
    '''
    
    len_suffled = len(shuffled_lines)
    len_ocr = len(ocr_lines)
    print 'len_suffled', len_suffled, 'len_ocr', len_ocr
    
    mapping = {}
    matched_ocr_lines = []

    for i in range(0, len_suffled):
        mapping[i] = {'index': i, 'weight': 0, 'final': -1}
        for j in range(0, len(ocr_lines)):            
            if j not in matched_ocr_lines:
                s = measure_similarity(shuffled_lines[i], ocr_lines[j])
                if s > mapping[i]['weight'] and s > 0.6:
                    # Assuming s > 0.6 is very similar
                   mapping[i] = {'index': j, 'weight': s, 'final': j}
        
        # Mark the best match from ocr_lines\
        if mapping[i]['weight'] > 0:
            matched_ocr_lines.append(mapping[i]['index'])
               
    print mapping
    
    ordered_lines = []
    for i in range(0, len_suffled):
        ordered_lines.append('')
        
    dup_lines = [] # For duplicate entries
    
    # Detect duplicate mapping and decide the winner(final)
    for i in range(0, len_suffled):
        for j in range(i+1, len_suffled):
            if mapping[i]['index'] == mapping[j]['index']:
                if mapping[i]['weight'] < mapping[j]['weight']:
                    mapping[i]['final'] = -1
                else:
                    mapping[j]['final'] = -1
    
    print mapping            
    
    for key, val in mapping.items():
        if mapping[key]['final'] == -1:
            dup_lines.append(shuffled_lines[key])
        else:
            ordered_lines[val['index']] = shuffled_lines[key]    
    
    if len(dup_lines):
        ordered_lines.append("###")
    
    return ordered_lines + dup_lines     
    

def refine_poetry(poetry, url, language):
    '''
    '''
    
    # Get image of the poetry
    
    # Get text from poetry image : ocr_text
    
    # Make list of lines from ``poetry`` and ``ocr_text``
    
    # Correct the line order of ``poetry``
    
    # Insert html br tags to make stanza
            
    # Return    


def process_items_by_reindeer():
    '''
    Post processing of items crawled by the ``ReindeerBot``
    '''
    pass