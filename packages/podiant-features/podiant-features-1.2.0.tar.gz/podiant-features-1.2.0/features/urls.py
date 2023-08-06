from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import ActivateFeatureView, DeactivateFeatureView


urlpatterns = (
    url(
        r'^activate/$',
        login_required(ActivateFeatureView.as_view()),
        name='activate_feature'
    ),
    url(
        r'^deactivate/$',
        login_required(DeactivateFeatureView.as_view()),
        name='deactivate_feature'
    )
)
