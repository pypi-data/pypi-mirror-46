from django.conf import settings
from django.db import models
from imp import find_module
from importlib import import_module


class FeatureSwitch(models.Model):
    user = models.ForeignKey(
        'auth.User',
        related_name='activated_features',
        on_delete=models.CASCADE
    )

    feature = models.CharField(max_length=100)

    class Meta:
        db_table = 'features_user'
        unique_together = ('feature', 'user')


def autodiscover():
    for app in settings.INSTALLED_APPS:
        import_module(app)
        name = '%s.features' % app

        try:
            import_module(name)
        except ImportError as ex:
            try:
                find_module(name)
            except ImportError:
                continue

            raise ex  # pragma: no cover


autodiscover()
