from django.views.generic.base import View
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from . import activate_feature, deactivate_feature


class ActivateFeatureView(View):
    def post(self, request):
        feature = request.POST.get('feature')
        next = request.POST.get('next') or '/'

        if activate_feature(feature, request):
            return HttpResponseRedirect(next)

        return HttpResponseBadRequest('Feature could not be activated.')


class DeactivateFeatureView(View):
    def post(self, request):
        feature = request.POST.get('feature')
        next = request.POST.get('next') or '/'

        if deactivate_feature(feature, request):
            return HttpResponseRedirect(next)

        return HttpResponseBadRequest('Feature could not be deactivated.')
