from .exceptions import AlreadyRegisteredError


class FeatureList(object):
    def __init__(self):
        self._features = {}

    def list(self):
        return list(self._features.keys())

    def register(self, name, kls, *groups, cache_context=None):
        if name in self._features:
            raise AlreadyRegisteredError(
                '%s is already registered.' % name
            )

        self._features[name] = (
            kls,
            groups,
            cache_context
        )
