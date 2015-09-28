
# USERS, GROUPS & PROOFREADING

There is four types of user groups.

	1. Crawlers
	------------
		a. Automatic or Human.
		b. Crawl the internet or books, find out the poetry, make initial entries to the Article, Books and Author tables.
	
	2. Proofreader1
	---------------
		a. Human.
		b. Do the first level of proofreading. Correct the formatting, remove extra symbols, fill the empty entries of the tables.
		c. Can publish the article (set the **Model.Article.is_published = True**)
		d. After finishing the proofreading, user will set	**proofread_level = level 1**


	3. Proofreader2
	---------------
		a. Human.
		b. Do the second level of proofreading. < gray area >
		c. Can publish the article (set the **Model.Article.is_published = True**)
		d. After finishing the proofreading, user will set **proofread_level = level 2**
		
	4. Proofreader3
	---------------
		a. Human.
		b. Do the third level of proofreading. < gray area >
		c. Can publish the article (set the **Model.Article.is_published = True**)
		d. After finishing the proofreading, will set **proofread_level = level 3**
		
	5. Managers
	---------------
		a. Human.
		b. Do the Fourth and last level of proofreading.
		c. Can publish as well remove the article (set the **Model.Article.is_published = True/False**)
		d. After finishing the proofreading, can set **proofread_level = level 4**
		e. Can reduce the **proofread_level** to any lower level, if not satisfied with the previous proofreadings.
		f. Can change information regarding Author and Book in the DB
	

A user can only proofread an article having proofread_level one lower than the proofread_level of his own group. Finishing of the proofreading of an article means, the user has made the neccessary changes as per his ability and experience, and now ready for proofreading of other articles (having proofread_level one level down). Now he/she can't change that article again. The article will be passed to the proofreaders of the higher level (one level up).