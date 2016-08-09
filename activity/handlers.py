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
    timestamp = kwargs.pop('timestamp', None)
    public = kwargs.pop('public', True)
    msg = kwargs.pop('change_message', None)

    content_type = kwargs.pop('content_type', None)
    object_id = kwargs.pop('object_id', None)
    object_repr = kwargs.pop('object_repr', None)

    act = Action(
        actor = sender,
        target_content_type = content_type,
        target_object_id = object_id,
        target_object_repr = object_repr[:200],
        verb = verb,
        change_message = msg,
        public = bool(public),
    )
    if timestamp:
        act.timestamp = timestamp
    act.save()
