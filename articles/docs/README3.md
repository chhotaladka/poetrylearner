# How to select an Article for editing (proofreading, formatting etc)

Note: In USER model, there should be a list of contribution entry (Article.ID edited)

1. List would be shown to user depending upon the current level of user (identified by `Article.meta.proofread_level`) and status of the Article (identified by `Article.meta.is_active`)

2. When user selects an Article, it will trigger a request to server notifying that this page has been selected for edting.
Server will perform following atomic operations:
	
	1. Mark this article as ACTIVE (i.e. `Article.meta.is_active` = True)
	2. Change Article.modified_by = User
	3. Add Article.ID in __User.Contribution__ table
	
3. User can view currently his/her selected pages on the DASHBOARD.
	__Article.IDs__ FROM __User.Contribution__ WHERE __Article.meta.is_active=True__ AND __Article.modified_by=User__
	
4. User can also withdraw from editing anytime. Do the following upon his/her action:

	1. Entry(__Article.ID__) from __User.Contribution__ would be deleted.
	2. Article would be restored to it's previous version (title, content and modified_by)
	3. Set `Article.meta.is_active` = False
	
5. If User save the Article as draft for further editing. Do the following:

	1. User can only change Article.title and Article.content
	2. No version control for this operation
	
6. If User finishes the editing process and `submit`s the Article

	1. Make a new version and save in version control table.
	2. Mark the Article as inactive i.e. `Article.meta.is_active` = false
	3. Change the proofread level of the Article.
	4. Make an entry of User in `Project.contributors`
	5. Update User performance stats.
	

# CRON JOB for monitoring progress of Article  

Any User can HOLD an Article for not more than __7 Days__
To ensure this, a cron job will run on server once in two day and will perform following operations:

1. Check for idle Articles by __Article.meta.is_active=True__ AND __Article.meta.date_modified__
2. If Article is idle for more than or equal to __4 days__, send a notification to the __Article.modified_by__
3. If it is idle for more than or equal to __7 days__, notify the User and initiate Article withdrawl operation described above (href: section 4 i.e. same as the self withdrawl procedure initiated by the User).
4. TODO: Collect User performance stats. 
