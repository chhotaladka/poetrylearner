from django.apps import AppConfig

class ActivityConfig(AppConfig):
    name = 'activity'

    def ready(self):
        from activity.signals import sig_action
        from activity.handlers import action_handler
        sig_action.connect(action_handler, dispatch_uid='activity.models')
