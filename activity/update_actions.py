# Fuctions to update the actions which have been occurred before
# this app. 

from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from repository.models import Poetry, Person, Book
from activity.models import Action, VERBS 

ACCESS_CODE = 'ykM3'

def update_action_from_repository(code):
    '''
    @summary: Collect the records of the actions happened on items of ``repository``.
    Basically, we can know only the details of first action (addition)and 
    last action (last update) on an item. Items having date_published is
    ignored.
    @NOTE: Call only one time i.e. after running migrations for ``activity`` app.
    '''
    
    # Just to avoid the calling of this function accidently
    if code != ACCESS_CODE:
        print 'WARNING: wrong access code!'
        print 'WARNING: Call only one time i.e. after running migrations for ``activity`` app'
        print 'If you understand the risk, use', ACCESS_CODE, 'as access code.'
        return False
    
    item_classes = [Person, Poetry, Book]
    # Do for all item types
    for item_cls in item_classes:
        print 'Updating actions for', item_cls.item_type()
        obj_list = item_cls.objects.order_by('-date_added', '-date_modified')
        for obj in obj_list:
            # Create action for date_added
            act = Action()
            act.timestamp = obj.date_added
            act.actor = obj.added_by
            act.target_content_type = ContentType.objects.get_for_model(obj)
            act.target_object_id = obj.id
            act.target_object_repr = obj.name[:200]
            act.verb = VERBS['ADDITION']
            act.change_message = None
            act.public = True
            act.save()
            print obj.date_added, 'added'
            
            # Create action for date_modified, if it is different
            if obj.date_modified != obj.date_added:
                act = Action()
                act.timestamp = obj.date_modified
                act.actor = obj.modified_by
                act.target_content_type = ContentType.objects.get_for_model(obj)
                act.target_object_id = obj.id
                act.target_object_repr = obj.name[:200]
                act.verb = VERBS['CHANGE']
                act.change_message = None
                act.public = True
                act.save()
                print obj.date_modified, 'updated'