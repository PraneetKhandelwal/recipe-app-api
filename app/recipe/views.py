from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe.serializers import TagSerializer, IngredientSerializer

from core.models import Tag, Ingredient


class TagView(viewsets.GenericViewSet,
              mixins.ListModelMixin,
              mixins.CreateModelMixin):
    """View to list tags"""
    serializer_class = TagSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # For ListModelMixin
    queryset = Tag.objects.all()

    def get_queryset(self):
        """
        Return the list of tags for the authenticated user
        """
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)


class IngredientView(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """View to list ingredients"""
    serializer_class = IngredientSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # For ListModelMixin
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        """
        Return the list of ingredients for the authenticated user
        """
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """Create a new ingredient"""
        serializer.save(user=self.request.user)
