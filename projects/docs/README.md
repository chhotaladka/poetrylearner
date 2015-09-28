# DESCRIPTION OF _PROJECTS_ APP

The `project` app is responsible for creating a new project and 
managing through out its lifecycle.

# MODELS DETAILS

## 1. Author model

* __name__		: Name of the Author/Poet/Artist
* __sobriquet__		: Nickname or Penname
* __date_birth__	: Date of birth
* __date_death__	: Date of death
* __image__		: Profile picture**
* __summary__		: Short introduction
*  __source_url__	: For further references, URL of the wiki page.
* __date_modified__	: Last modified on (date and time)
* __modified_by__	: Last modified by


## 2. Book model

* __name__		: Original title
* __authors__		: Foreign key of _projects.models.Authors (Multiple Authors possible)
* __pid__		: Published ID. Dictionary field, having ISBN-10, ISBN-13 and other ID's mapping
* __publisher__		: Name and other details of publisher
* __year_published__: Year of publication
* __language__		: Language
* __date_modified__	: Last modified on (date and time)
* __modified_by__	: Last modified by

Note 1: Once a book is linked with some project, it's `name`, `authors` and `language` field can't be changed.


## 3. Project model

* __book__		: Foreign key of _projects.models.Book_
* __source__		: Source of the scanned images of the book i.e. scanned by ourself or copied from digital library. Two options are there: 1. Scanned by ourself (`offline`), 2. Online digital library (`online`)
* __source_url__	: URL of the digital library's book page. Leave empty of you have selected option 1 (scanned) in the __source__
* __start_date__	: Date of initiation
* __end_date__		: Date of finishing
* __pages__		: Total number of pages of the Book
* __scanned_pages__	: Total number of available scanned pages
* __contributors__	: Users contributed. OneToMany Field
* __manager__		: User who is managing this project
* __date_modified__	: Last modified on (date and time)
* __note__		: Note about the `Project`
* __state__		: Choice Field having following states	
				
				1. PROJECT INITIATION
				2. ADDING SCANNED DATA
				3. ADDING OCR DATA
				4. PROOREADING
				5. FORMATTING
				6. PUBLISHED

Note 1: Once a project is created, it's `book` field can't be changed.
Note 2: Only `manager` has write access to the project, but the Administrator can change the `manager` field and assign new `user` as `manager`. 


## 4. ImageSource model

Stores the source URLs of the images of scanned pages taken from the Digital Library 
(`online`).

* __page_num__	: Page number or sequence number of the scanned image correspoding to the page number of book.
* __url__		: Source URL of the page
* __project__	: Foreign key of _Project_



# PROJECTS FILES AND RULES FOR STORAGE

Path of the project files : __media/projects/projectid_book/__
Where `projectid` is the primary key of the Project.

There would be following project files:-

__projectid_img_scanned.tar__ : Contains raw scanned images or the images downloaded from Digital Library. Usually in TIFF format.
__projectid_img_jp2.tar__ : Contains processed JPEG2000 or other format images, these are scaled and displayed in the proofreader section.
__projectid_ocr.tar__ : Contains OCR data XML format.
__projectid_meta.json__ : contains bibliographic metadata about the book.
__projectid_ebooks.tar__ : Contains the finished book, converted into different formats, and available to download by online users.


## Detail description of each project file

### projectid_img_scanned.tar

Contains raw scanned images or the images downloaded from Digital Library. Usually in TIFF format.
These images will be input for the OCR as well as for the processed JPEG2000 convertor.

Directory structure:
	./projectid_0001.tif
	./projectid_0002.tif 

Note:
	1. After completion of OCR process, there is no use of this directory, and it can be stored as for reference purpose only.
	
### projectid_img_jp2.tar

Contains processed JPEG2000 or other format images, these are scaled and displayed in the proofreader section.

Directory structure:
	./projectid_0001.jpg
	./projectid_0002.jpg
	
Note:
	1. APIs to get an image, edit(rotate), and save it back.
	2. APIs to get the image for proofreading.
	
### projectid_ocr.tar

Contains OCR data in XML format, used by proofreading at very first level. The manager will copy the OCR data of a page into `Article` table to start the proofreading process.

Directory structure:
	./projectid_0001.xml
	./projectid_0002.xml
	
Note:


### projectid_meta.json
 
contains bibliographic metadata about the book.
It's structure is given below: TODO


### projectid_ebooks.tar

Contains finished book, converted into different readable formats, and make them available to download by online users.

Directory structure:
	./projectid.html
	./projectid.txt  /* UTF-8 */
	./projectid.mobi /* kindle */
	./projectid.epub
	
## Rules for Books, Scanned Manually by ourself

It means __Project.source = offline__
In this case the manager will browse the scanned image, convert it into desired format, rename it and add into __projectid_img.gz__.
Suppose, if `Project.id` is __2365__ and page number is __10__, 
then image name would be __2365_0010.jpg__ (assuming jpg format), 
and the relative path in the project directory would be __/projectid_book/projectid_img/projectid_0010.jpg__
i.e. /2365_book/2365_img/2365_0010.jpg

Process of renaming and saving into final directory will be automatic.


## Rules for Books, Taken from Digital Library

It means __Project.source = online__
The manager would enter the page URL one by one, download the image, rename and finally save into appropriate directory as per the rules mentioned in the previous section.

Process will be fully automatic if rules for scrapping __Project.source_url__ is present, otherwise the manager has to put the link of each page one by one, or in worst case download the whole book manully and repeat the the process of previous section.

## Lifetime of stored images

Save the images scanned manually as long as possible.
As for the images taken from the Digital Library (`online`), after completion of the project we can delete the images if storage constraints are there.
 
## Supported file formats

Supported input image formats:

    JPEG 2000
    JPEG
    TIFF
    PNG

Supported output image formats (these are formats that all browsers can display):

    JPEG
    PNG

Supported archive formats:

    ZIP
    Tar

Supported image operations:

    Scaling by powers of two
    Scaling by an arbitrary factor (increases server load)
    Rotation by 90 degrees

