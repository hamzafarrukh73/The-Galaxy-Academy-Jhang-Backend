from typing import Any

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .permissions import UserPermissions
from .serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet[User]):
    """
    ViewSet for viewing and editing the current user's profile.
    """

    serializer_class = UserSerializer
    permission_classes = [UserPermissions]

    @action(detail=False, methods=["get", "put", "patch"], url_path="me")
    def me(self, request: Any) -> Response:
        """
        Retrieve or update the authenticated user's profile.
        """
        if request.method in ["PUT", "PATCH"]:
            user = request.user
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        user = User.objects.prefetch_related("groups").get(pk=request.user.pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
