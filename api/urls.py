from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    SignupAPIView,
    TitleViewSet,
    TokenAPIView,
    UserAPIView,
    UserViewSet,
)

router = DefaultRouter()

router.register(prefix="categories", viewset=CategoryViewSet)
router.register(prefix="genres", viewset=GenreViewSet)
router.register(prefix="titles", viewset=TitleViewSet)
router.register(prefix="users", viewset=UserViewSet)

titles_router = NestedDefaultRouter(parent_router=router, parent_prefix="titles", lookup="title")
titles_router.register(prefix="reviews", viewset=ReviewViewSet, basename="review")

reviews_router = NestedDefaultRouter(
    parent_router=titles_router, parent_prefix="reviews", lookup="review"
)
reviews_router.register(prefix="comments", viewset=CommentViewSet, basename="comment")


urlpatterns = [
    path(route="v1/auth/signup/", view=SignupAPIView.as_view()),
    path(route="v1/auth/token/", view=TokenAPIView.as_view()),
    path(route="v1/users/me/", view=UserAPIView.as_view()),
    path("v1/", include(arg=router.urls)),
    path("v1/", include(arg=titles_router.urls)),
    path("v1/", include(arg=reviews_router.urls)),
]
