#Requirement for crawler

pip install requests
to know more, visit 
	1. https://pypi.python.org/pypi/requests/2.7.0
	2. http://docs.python-requests.org/en/latest/

For XML/HTML parsing (to know more, visit http://lxml.de)
Used by crawler to extract information from the web pages
__ sudo pip install lxml __
You might get some error while installation. In that case install the following packages
__ sudo apt-get install libxml2-dev libxslt-dev __


# IMAGE PROCESSING SUPPORT
Used to process the scanned images. (in __projects__ app)

_References_:
	1. https://pillow.readthedocs.org/handbook/image-file-formats.html#image-file-formats
	2. https://pillow.readthedocs.org/installation.html#external-libraries

## Python Imaging Library (PIL)
First install `External Libraries` before installing the _PIL_

	pip install pip
	
	
## External Libraries
Many of PIL features require external libraries.

### JPEG
To enable JPEG support, you need to build and install the __IJG JPEG library__ before building the _Python Imaging Library_.

	sudo apt-get install libjpeg-dev

### JPEG 2000
http://www.openjpeg.org/
To enable JPEG 2000 support, you need to build and install the __OpenJPEG library__, version 2.0.0 or higher, before building the _Python Imaging Library_.

	sudo apt-get install openjpeg ??
	#sudo apt-get install openjpeg-tools ??
	
### PNG
To enable PNG support, you need to build and install the __ZLIB compression library__ before building the _Python Imaging Library_.

	sudo apt-get install zlib1g-dev
	
### TIFF
If you have __libtiff__ and its headers installed, _Python Imaging Library_ can read and write many more kinds of compressed TIFF files. If not, _Python Imaging Library_ will always write uncompressed files.

	sudo apt-get install libtiff-dev
	
### Others
libfreetype provides type related services

	sudo apt-get install libfreetype6-dev