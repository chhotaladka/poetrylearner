import tarfile

def get_available_pages(filename):
    """
    `filename`: full path of tar file having scanned-image/jp2-image/ocr-data of the pages 
    Get the list of page numbers avalibale in the tarfile `filename`
    Extract the page number from the name of the file(image)
    """
    pages = []
    print "DBG:: get_available_pages: ", filename
    
    try:
        if tarfile.is_tarfile(filename):
            t = tarfile.open(filename, 'r')
                        
            for name in t.getnames():
                # assuming, the file name is like `projectid_00001.xyz`
                num = name.split('.')[0] # remove the extension (filetype)
                num = num.split('_')[-1] # remove the `projectid` part
                pages.append(int(num))
            
            #print pages
            return pages
            
    except IOError, err:
        print 'ERROR:: get_available_pages: %s' % (err)
        return pages



