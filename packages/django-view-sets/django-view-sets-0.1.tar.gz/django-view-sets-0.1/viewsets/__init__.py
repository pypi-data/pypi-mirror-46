# flake8: noqa
from .serializers import ViewSetSerializer
from .views import (
    ViewSetCreateView, ViewSetDeleteView, ViewSetDetailView, ViewSetIndexView,
    ViewSetListView, ViewSetUpdateView
)
from .viewsets import ModelViewSet, ViewSet


__version__ = '0.1'
default_app_config = 'viewsets.apps.ViewsetsConfig'
