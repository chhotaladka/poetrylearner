"""
Image processing

Supported file types:
    JPEG 2000
    JPEG
    TIFF
    PNG

"""
from __future__ import print_function
import os, sys
import traceback
from PIL import Image
from PIL import TarIO

#out = im.rotate(90) # degrees counter-clockwise

# fp = TarIO.TarIO("Imaging.tar", "Imaging/test/lena.ppm")
# im = Image.open(fp)

def main_fun():
    infile = '/home/nandan/Downloads/dli-books/1/model.png'
    print('input file :', infile)
    
    f, e = os.path.splitext(infile)
    outfile = f + ".jpg"
    if infile != outfile:
        try:
            im = Image.open(infile)
            print(infile, im.format, "%dx%d" % im.size, im.mode)            
            
            im.save(outfile, "JPEG")
            
            print('output file :', outfile)
            
        except IOError:        
            print ("DBG:: Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("DBG:: Error in %s on line %d" % (fname, lineno))
             
                
if __name__ == "__main__":
    main_fun()