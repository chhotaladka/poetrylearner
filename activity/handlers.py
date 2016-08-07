from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.six import text_type
from django.dispatch import receiver

from activity import signals
from activity.models import Action

#@receiver(signals.sig_action)
def action_handler(sender, **kwargs):
    """
    Handler function to create Action instance upon action signal call.
    """
    kwargs.pop('signal', None)
    verb = kwargs.pop('verb')
    public = kwargs.pop('public', True)
    msg = kwargs.pop('change_message', None)

    content_type = kwargs.pop('content_type', None)
    object_id = kwargs.pop('object_id', None)
    object_repr = kwargs.pop('object_repr', None)

    Action.objects.log_action(
        user = sender,
        target_content_type = content_type,
        target_object_id = object_id,
        target_object_repr = object_repr,
        verb=verb,
        change_message=msg,
        public=public,
    )
