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