# STATE TRANSITION OF THE PROJECT

_Note:_
	1. The files in each archive should have names as per the proper naming convention mentioned in previous section.
	
	
## 1. PROJECT INITIATION

This is default and first state.
Create a new `Project`. Add Book, Authors and Project
The uniquenes of the Project is by the Book associated with it. So there can be no duplicate entry for the Book.
(_Two Books are identical if there `name` is same, and at least one of their `authors` are same._)
Note: Project information can be changed in this state. 


## 2. ADDING SCANNED DATA

Create `projectid_img_scanned.tar` when the first scanned image is added. 
Add all available scanned images to this archive. If the images are taken from some Online Digital Library, then update the source URL info of each page into the database (`projects.models.ImageSource`) along with the source URL of the main(detail/home) page of the book. By this, we can keep a backword link to the original source. 

Make the state transition to _SCANNED_DATA_ADDED_
And do the followings:
	
	1. Create the project directory : __media/projects/projectid_book/__
	(Where `projectid` is the primary key of the Project)
	2. Change the permissions.(?)
	3. Create `projectid_meta.json`. It contains Data of the `Project` and `Book` table.	

Note: Project information can be changed in this state. 


## 3. ADDING OCR DATA

Extract files from `projectid_img_scanned.tar` and convert them one by one by OCR software, and add the output to `projectid_ocr.tar`. Add files once you have the OCR software ready. It can be initiated page by page OR processing all images collectively.

The `image convertor tool` will convert all images of `projectid_img_scanned.tar` directory to the JPEG2000 format i.e. more suitable for display on most of the browsers, and add them to `projectid_img_jp2.tar`.

Make the state transition to _OCR_DATA_ADDED_

## 4. PROOFREADING

The manager would add OCR converted text of each page to the database (`articles.models.Article`).
Thus making the pages(Article) ready for proofreading.

In proofreading window image from `projectid_img_jp2.tar` alongside the corresponding article page from `articles.models.Article` will be displayed to the proofreader.

Proofreader can perform following operation on the Page:

	1. Save Draft (No version control for this operation).
	2. Submit (with version control, will increase the proofread level by ONE).
	3. Make query to manager. 
	4. Withdraw (from editing the Article)

Make the state transition to _PROOREADING_

There will be THREE proofreading rounds.

## 5. FORMATTING

When the proofreading of all the pages of the book would have finished all proofread levels, the Manager can initiate the Formatting round. 

Make the state transition to _FORMATTING_

There will be TWO formatting rounds
Round TWO will follow the ONE when all pages have completed round ONE.
The manager will start round TWO of the formatting.

## 6. PUBLISHED

Update the json `projectid_meta.json`
Convert finished book into different readable formats, and make it available to download by online users.
Set the `verified` flags for each page of the book.
Update the json `projectid_meta.json`

Make the state transition to _PUBLISHED_

