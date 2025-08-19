from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, LoginView,SignupView   # 👈 add LoginView here

router = DefaultRouter()
router.register(r'devices', DeviceViewSet)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path('', include(router.urls)),
]