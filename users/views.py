from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import User
from .permissions import IsAdminOrRequestUser
from .serializers import UserCreateUpdateSerializer, UserDetailSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing User instances.

    """
    serializer_class = UserCreateUpdateSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ('update', 'partial_update'):
            permission_classes = [IsAuthenticated, IsAdminOrRequestUser]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Returns the serializer class for each particular method"""
        if self.action in ('retrieve', 'list'):
            return UserDetailSerializer
        elif self.action == "create":
            return UserCreateUpdateSerializer
        elif self.action in ("partial_update", "update"):
            return UserCreateUpdateSerializer
        else:
            return UserDetailSerializer
