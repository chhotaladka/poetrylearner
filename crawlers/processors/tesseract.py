'''
Methods to use tesseract-ocr functions to operate an image.
Source: https://github.com/tesseract-ocr

Installation: https://github.com/tesseract-ocr/tesseract/blob/master/INSTALL

You may required following packages while compiling/installing tesseract:
 > sudo apt-get install autotools-dev autoconf automake libtool checkinstall
 > leptonica - is image processing library
    # wget http://www.leptonica.org/source/leptonica-1.73.tar.gz
    # tar -zxvf leptonica-1.73.tar.gz
    # cd leptonica-1.73
    # ./configure
    # make
    # sudo checkinstall
    # sudo ldconfig
    
Download training data from https://github.com/tesseract-ocr/tessdata
and copy the .traineddata file into the 'tessdata' directory, 
probably /usr/local/share/tesseract-ocr/tessdata or /usr/local/share/tessdata.

For image pre processing to remove rekhta watermark
    # sudo apt-get install imagemagick
    # convert img-in -background white img-out
'''
import subprocess
import os
import tempfile
from exceptions import Exception
import codecs


def check_packages():
    '''
    @summary: Return True if required packages are installed in system.
    '''    
    FNULL = open(os.devnull, 'w')
    
    # Check tesseract
    print('package check: tesseract...')
    try:
        subprocess.call(["tesseract", "-v"], stdout=FNULL)
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            # handle file not found error.
            print('ERR: "tesseract" not found on this system.')
            print('Installation help: https://github.com/tesseract-ocr/tesseract/blob/master/INSTALL')
            return False
        else:
            # Something else went wrong while trying to run `tesseract`
            print('ERR: Something went wrong while trying to run "tesseract".')
            return False
    
    # Check tesseract Language packs
    print('package check: tesseract language packs...')
    try:
        out = subprocess.check_output(["tesseract", "--list-langs"])
        #print out
    except:
        # handle file not found error.
        print('ERR: "No language pack of tesseract found on this system.')
        print('----->')
        print('- Download training data from https://github.com/tesseract-ocr/tessdata')
        print('- and copy the .traineddata file into the "tessdata" directory,') 
        print('- probably /usr/local/share/tesseract-ocr/tessdata or /usr/local/share/tessdata.')
        print('- Installation help: https://github.com/tesseract-ocr/tesseract/blob/master/INSTALL')
        print('----->')
        return False
    
    # Check imagemagick convert
    print('package check: imagemagick convert...')
    try:
        subprocess.call(["convert", "-v"], stdout=FNULL)
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            # handle file not found error.
            print('ERR: "convert" not found on this system.')
            print('Install "imagemagick" package.')
            return False
        else:
            # Something else went wrong while trying to run `convert`
            print('ERR: Something went wrong while trying to run "convert".')
            return False
        
    # All passed, now return True
    print('package check: all present.')
    return True     
        

def image_to_text_for_reindeer(in_image, language):
    '''
    @in_image: full path of input image
    @language: language code for the content in the in_image e.g. hi, en, ur etc.
    
    @summary: Convert image to text. Pre-processing of image is tested for reindeer only
    '''    
    
    # Check for language support of tesseract
    #print 'tesseract: checking language support...'
    if language == 'hi':
        lang = 'hin'
    elif language == 'en':
        lang = 'eng'
    elif language == 'ur':
        lang = 'urd'
    else:
        print('ERR: language pack for', language, 'is not supported.')
        return False        
    
    # Preprocess image with imageMagick convert, to set background white
    # <rekhta watermark was creating trouble for tesseract>
    
    #print 'tesseract: Input image:', in_image
    print('tesseract: preprocessing using imageMagick convert...')    
    try:        
        retcode = subprocess.check_call(['convert', in_image, '-background', 'white', in_image])
    except subprocess.CalledProcessError as e:
        print('ERR:: "convert" command failed, unexpected error:', e)
        return False        
    
    # Now run the tesseract to read the text from image and store it to text file
    print('tesseract: converting image to text...')        
    try:
        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        out = tmp_file.name # To generate random name, I used temfile
        retcode = subprocess.check_call(['tesseract', in_image, '-l', lang, out])
        # output file name will be `out`.txt
        out_file = out + '.txt'
        #print 'tesseract: output text is', out_file
        
    except subprocess.CalledProcessError as e:
        print('ERR:: "tesseract" command failed, unexpected error:', e)
        return False  
    
    # Read the text from `out_file`
    with codecs.open(out_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Delete the `out_file` from the storage
    try:
        os.remove(out_file)
    except:
        print('ERR:: failed to delete out_file')
        pass
    
    # Return poetry text
    return text