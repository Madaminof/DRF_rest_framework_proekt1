from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DataViewsets


router = DefaultRouter()
router.register('data', DataViewsets, basename='data')
urlpatterns = router.urls