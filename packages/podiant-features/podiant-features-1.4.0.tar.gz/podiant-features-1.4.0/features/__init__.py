from django.core.cache import cache
from .manager import FeatureList
from .base import FeatureBase, functional_handler_factory
from .signals import (
    feature_activated as fa_signal,
    feature_deactivated as fd_signal
)

import types


__version__ = '1.4.0'


handlers = FeatureList()


__all__ = [
    'handlers',
    'feature_enabled',
    'autodiscover',
    'FeatureBase',
    'register'
]


def get_cache_key(feature, key, request):
    feature = handlers._features.get(feature)
    if feature is None:
        return key

    klass, groups, cache_context = feature

    if callable(cache_context):
        cache_context = cache_context(request)

    if key and cache_context:
        key = '%s[%s]' % (cache_context, key)

    return 'feature.%s' % key


def feature_enabled(name, request):
    if not getattr(request, 'user', None):
        return False

    def a():
        u = request.user.is_authenticated
        return u() if callable(u) else u

    if a():
        cachekey = get_cache_key(
            name,
            '%s.enabled.%s' % (
                name,
                request.user.username
            ),
            request
        )
    else:
        cachekey = None

    if name not in handlers._features:
        return False

    if cachekey and cachekey in cache:
        return cache.get(cachekey)

    klass, groups, cache_context = handlers._features.get(name)
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
        cachekey = get_cache_key(
            name,
            '%s.activated.%s' % (
                name,
                request.user.username
            ),
            request
        )
    else:
        return False

    if name not in handlers._features:
        return False

    if cachekey and cachekey in cache:
        return cache.get(cachekey)

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

    cachekey = get_cache_key(
        name,
        '%s.activated.%s' % (
            name,
            request.user.username
        ),
        request
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

    cachekey = get_cache_key(
        name,
        '%s.activated.%s' % (
            name,
            request.user.username
        ),
        request
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


def clear_feature_cache(request, *features):
    if not getattr(request, 'user', None):
        return False

    def a():
        u = request.user.is_authenticated
        return u() if callable(u) else u

    if not a():
        return

    for feature in handlers.list():
        if any(features) and feature not in features:
            continue

        cachekey = get_cache_key(
            feature,
            '%s.enabled.%s' % (
                feature,
                request.user.username
            ),
            request
        )

        if cachekey in cache:
            cache.delete(cachekey)

        cachekey = get_cache_key(
            feature,
            '%s.activated.%s' % (
                feature,
                request.user.username
            ),
            request
        )

        if cachekey in cache:
            cache.delete(cachekey)


def register(name, *groups, cache_context=None):
    def wrapper(kls):
        if isinstance(kls, types.FunctionType):
            handlers.register(
                name,
                functional_handler_factory(kls),
                *groups,
                cache_context=cache_context
            )
        else:
            handlers.register(
                name,
                kls,
                *groups,
                cache_context=cache_context
            )

        return kls

    return wrapper
