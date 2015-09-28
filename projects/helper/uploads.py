import tarfile
import os, sys, traceback
import StringIO


"""
Functions to handle uploaded scanned image files
 @file: uploaded file
 @dest: destination archive name
 @name: final file name
"""
def handle_uploaded_scanned_image(file, dest, name):
    print "DBG:: processing uploaded scanned image: ", file, file.size, "Bytes"
    print "DBG:: dest", dest, "name", name
    
    # Check if the `dest` is tarfile
    try:
        if tarfile.is_tarfile(dest) is False:
            # file is not a tarfile
            print "ERROR:: dest is not a tarfile"
            return 101
            
    except IOError, err:
        print 'WARNING:: a %s' % (err)
        pass
    
    # Create StringIO
    try:
        myfile = StringIO.StringIO()
        for chunk in file.chunks():
            # generate chunk
            myfile.write(chunk)
        myfile.seek(0)
    except IOError, err:
        print 'ERROR:: %s' % (err)
        return 102
    
        
    # Add the `file` into archive `dest` as `name`
    out = tarfile.open(dest, mode='a')        
    try:        
        info = tarfile.TarInfo(name=name)
        info.size = len(myfile.buf)        
        out.addfile(tarinfo=info, fileobj=myfile)        
        
    except:
        print ("ERROR:: Unexpected error:", sys.exc_info()[0])
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print ("ERROR:: Error in %s on line %d" % (fname, lineno))
        return 103
    
    finally:        
        out.close()

        
#     try:
#         with open('/home/nandan/test/a.jpg', 'wb+') as destination:
#             for chunk in file.chunks():
#                 print "chunk"
#                 destination.write(chunk)
#     except IOError, err:
#         print 'ERROR:: %s' % (err)
#         return 11
    
    return 0
        