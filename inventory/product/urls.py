from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from .views import InventoryViewSet

router = DefaultRouter()
router.register('inventory', InventoryViewSet)

urlpatterns = [
    
    path('login', views.LoginAPIView.as_view(), name='api_login'),
    path('protected', views.MyProtectedView.as_view(), name='protected_view'),
    path('', include(router.urls)),
]