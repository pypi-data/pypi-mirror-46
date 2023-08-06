from django.db.models import Q


class FeatureBase(object):
    group_names = []

    def __init__(self, name, group_names):
        self.name = name
        self.group_names = group_names

    def enabled(self, request):
        def a():
            u = request.user.is_authenticated
            return u() if callable(u) else u

        if a():
            return self.user_in_group(request.user)

        return False

    def user_in_group(self, user):
        if any(self.group_names):
            q = Q()
            for group in self.group_names:
                q |= Q(name__iexact=group)

            return user.groups.filter(q).exists()

        return True


def functional_handler_factory(function):
    class FunctionalHandler(FeatureBase):
        def enabled(self, request):
            return function(request)

    return FunctionalHandler
