'''
Post processing of data crawled by ``ReindeerBot`` of rekhta.com
'''
import requests
import tempfile
import difflib


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
    print 'DBG: similarity is ', s
    return s


def _is_similar(str1, str2):
    s = measure_similarity(str1, str2)
    if s > 0.6: #TODO: increase the value if you are not getting correct output
        return True
    else:
        return False
    

def correct_poetry_lines_order(shuffled_lines, ocr_lines):
    '''
    '''
    
    len_suffled = len(shuffled_lines)
    len_ocr = len(ocr_lines)
    print 'len_suffled', len_suffled, 'len_ocr', len_ocr
    
    mapping = {}

    for i in range(0, len_suffled):
        mapping[i] = {'index': i, 'weight': 0}
        for j in range(0, len_ocr):
            s = measure_similarity(shuffled_lines[i], ocr_lines[j])
            if s > mapping[i]['weight']:
               mapping[i] = {'index': j, 'weight': s}
               
    print mapping
    
#http://poetrylearner.com/c/article/82009    
s1 = 'आबादियों में खो गया सहराओं का जुनून\
शहरों का जमघटों में गया गाँव का सुकून\
ये तजरबा भी गर्दिश-ए-हालात से हुआ\
लो काम होश से ये नया दौर है मतीन\
कैसे सपेद होता है हर आश्ना का ख़ून\
फिर उस जगह चलें जहाँ खो आए हैं सुकून\
बेचैन ज़िंदगी के तक़ाज़े अजीब हैं\
माज़ी की यादगार मिरे इल्म और फ़ुनून\
चेहरे पे जिन के दौड़ता था नाज़ुकी का ख़ून\
हालात के असीर हुए मस्ख़ हो गए\
तहज़ीब-ए-नौ की रौशनी में जल-बुझे तमाम\
वहशत न साथ देगी न काम आएगा जुनून'

list1 = s1.split('\n')

s2 = "आबादियो है रपो गया सहराओं का जुनून\
शहरो का जमघटो है गया गॉव का सुकून\
\
हालात के असीर हुए मस्ख तो गए\
चेहरे पे जिन के दौडता था नाजुकी का खून\
\
त्तहजीबच्चोंएच्चोंनां की रोशनी से जल'बुझे तमाम\
माजी की यादगार मिरे इल्म और फुनून\
\
बेचैन जिदगी के तकाजे अजीब है\
फिर उस जगह चलै जहाँ रपो आए है सुकून\
\
है त्तज़रबा गी गर्दिश'ए'हालात से हुआ\
कैसे सपेद माता है पृष्ट आश्रा का खून\
\
लां काम होश से है नया दोर है 'मतीन'\
वहशत न साथ देगी न काम आएगा जुनून"

list2 = [x for x in s2.split('\n') if len(x) > 1]          


            
            
        
    