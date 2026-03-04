from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignupAPIView, TokenAPIView, UserAPIView, UserViewSet

router = DefaultRouter()
router.register(prefix="users", viewset=UserViewSet)


urlpatterns = [
    path(route="v1/auth/signup/", view=SignupAPIView.as_view()),
    path(route="v1/auth/token/", view=TokenAPIView.as_view()),
    path(route="v1/users/me/", view=UserAPIView.as_view()),
    path("v1/", include(arg=router.urls)),
]
