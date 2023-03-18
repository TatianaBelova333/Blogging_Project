from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Post, Comment
from .permissions import IsUserAboveMinAge, IsAdminOrAuthor
from .serializers import (PostDetailSerializer, CommentDetailSerializer, PostCreateUpdateSerializer,
                          CommentUpdateSerializer, CommentCreateSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing Post instances."""
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""
        if self.action in ('retrieve', 'list'):
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsUserAboveMinAge]
        elif self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = [IsAuthenticated, IsAdminOrAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Returns the serializer class for each particular method"""
        if self.action in ('retrieve', 'list'):
            return PostDetailSerializer
        elif self.action in ("create", "partial_update", "update"):
            return PostCreateUpdateSerializer
        else:
            return PostDetailSerializer

    def get_queryset(self):
        if self.action == 'list':
            user = self.request.query_params.get('user')
            if user:
                return Post.objects.filter(author=user).all()
        return self.queryset


class CommentViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing Post instances."""
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""
        if self.action in ('retrieve', 'list'):
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = [IsAuthenticated, IsAdminOrAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Returns the serializer class for each particular method"""
        if self.action in ('retrieve', 'list'):
            return CommentDetailSerializer
        elif self.action in ("partial_update", "update"):
            return CommentUpdateSerializer
        elif self.action == "create":
            return CommentCreateSerializer
        else:
            return CommentDetailSerializer

    def get_queryset(self):
        if self.action == 'list':
            post = self.request.query_params.get('post')
            if post:
                return Comment.objects.filter(post=post).all()
        return self.queryset
