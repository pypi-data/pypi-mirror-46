from django.core.cache import cache
from .manager import FeatureList
from .base import FeatureBase, functional_handler_factory
from .signals import (
    feature_activated as fa_signal,
    feature_deactivated as fd_signal
)

import types


__version__ = '1.2.0'


handlers = FeatureList()


__all__ = [
    'handlers',
    'feature_enabled',
    'autodiscover',
    'FeatureBase',
    'register'
]


def feature_enabled(name, request):
    if not getattr(request, 'user', None):
        return False

    def a():
        u = request.user.is_authenticated
        return u() if callable(u) else u

    if a():
        cachekey = 'feature.%s.enabled.%s' % (
            name,
            request.user.username
        )

        if cachekey in cache:
            return cache.get(cachekey)
    else:
        cachekey = None

    if name not in handlers._features:
        return False

    klass, groups = handlers._features.get(name)
    feature = klass(name, groups)
    value = feature.enabled(request)

    if cachekey:
        cache.set(cachekey, value)

    return value


def feature_activated(name, request):
    if not getattr(request, 'user', None):
        return False

    def a():
        u = request.user.is_authenticated
        return u() if callable(u) else u

    if a():
        cachekey = 'feature.%s.activated.%s' % (
            name,
            request.user.username
        )

        if cachekey in cache:
            return cache.get(cachekey)
    else:
        return False

    if name not in handlers._features:
        return False

    from .models import FeatureSwitch

    value = FeatureSwitch.objects.filter(
        user=request.user,
        feature=name
    ).exists()

    cache.set(cachekey, value)
    return value


def activate_feature(name, request):
    if not getattr(request, 'user', None):
        return False

    def a():
        u = request.user.is_authenticated
        return u() if callable(u) else u

    if not a():
        return False

    cachekey = 'feature.%s.activated.%s' % (
        name,
        request.user.username
    )

    if name not in handlers._features:
        return False

    from .models import FeatureSwitch

    if not FeatureSwitch.objects.filter(
        user=request.user,
        feature=name
    ).exists():
        FeatureSwitch.objects.create(
            user=request.user,
            feature=name
        )

        fa_signal.send(activate_feature, feature=name, request=request)
        cache.set(cachekey, True)

    return True


def deactivate_feature(name, request):
    if not getattr(request, 'user', None):
        return False

    def a():
        u = request.user.is_authenticated
        return u() if callable(u) else u

    if not a():
        return False

    cachekey = 'feature.%s.activated.%s' % (
        name,
        request.user.username
    )

    if name not in handlers._features:
        return False

    from .models import FeatureSwitch

    if FeatureSwitch.objects.filter(
        user=request.user,
        feature=name
    ).exists():
        FeatureSwitch.objects.filter(
            user=request.user,
            feature=name
        ).delete()

        fd_signal.send(deactivate_feature, feature=name, request=request)
        cache.set(cachekey, False)

    return True


def register(name, *groups):
    def wrapper(kls):
        if isinstance(kls, types.FunctionType):
            handlers.register(
                name,
                functional_handler_factory(kls),
                *groups
            )
        else:
            handlers.register(name, kls, *groups)

        return kls

    return wrapper
