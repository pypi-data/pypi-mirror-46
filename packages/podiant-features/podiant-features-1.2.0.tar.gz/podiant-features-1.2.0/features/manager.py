from .exceptions import AlreadyRegisteredError


class FeatureList(object):
    def __init__(self):
        self._features = {}

    def register(self, name, kls, *groups):
        if name in self._features:
            raise AlreadyRegisteredError(
                '%s is already registered.' % name
            )

        self._features[name] = (
            kls,
            groups
        )
