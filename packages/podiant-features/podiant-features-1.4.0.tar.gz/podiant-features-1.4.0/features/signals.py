from django.dispatch import Signal


feature_activated = Signal(providing_args=('feature', 'request'))
feature_deactivated = Signal(providing_args=('feature', 'request'))
