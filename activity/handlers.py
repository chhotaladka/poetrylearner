from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.six import text_type
from django.dispatch import receiver

from activity import signals
from activity.models import Action

@receiver(signals.action)
def action_handler(sender, **kwargs):
    """
    Handler function to create Action instance upon action signal call.
    """
    print "DBG: action_handler called"
    kwargs.pop('signal', None)
    verb = kwargs.pop('verb', True)
    public = kwargs.pop('public', True)
    msg = kwargs.pop('change_message', '')
    t = kwargs.pop('timestamp', None)

    content_type_id = kwargs.pop('content_type_id', None)
    object_id = kwargs.pop('object_id', None)
    object_repr = kwargs.pop('object_repr', None)

    Action.objects.log_action(
        timestamp=t,
        user_id = sender.pk,
        target_content_type_id = content_type_id,
        target_object_id = object_id,
        target_object_repr = object_repr,
        verb=verb,
        change_message=msg,
        public=public,
    )
