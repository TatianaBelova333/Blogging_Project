from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import PostViewSet, CommentViewSet

app_name = 'posts'

post_router = SimpleRouter()
post_router.register(r'posts', PostViewSet, basename="posts")

comment_router = SimpleRouter()
comment_router.register(r'comments', CommentViewSet, basename="comments")

urlpatterns = [
    path("", include(post_router.urls)),
    path("", include(comment_router.urls)),
]