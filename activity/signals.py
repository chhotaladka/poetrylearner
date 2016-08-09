from django.dispatch import Signal

sig_action = Signal(providing_args=['timestamp',
                                'verb',
                                'content_type',
                                'object_id',
                                'object_repr',
                                'change_message',
                                'public'])