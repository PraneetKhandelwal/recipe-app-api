from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe.serializers import TagSerializer, IngredientSerializer

from core.models import Tag, Ingredient


class BaseRecipeAttributeView(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """View to list recipe attributes"""
    # serializer_class = TagSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Return the list of attributes for the authenticated user
        """
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """Create a new recipe attribute"""
        serializer.save(user=self.request.user)


class TagView(BaseRecipeAttributeView):
    """View to list tags"""
    serializer_class = TagSerializer
    # For ListModelMixin
    queryset = Tag.objects.all()


class IngredientView(BaseRecipeAttributeView):
    """View to list ingredients"""

    serializer_class = IngredientSerializer
    # For ListModelMixin
    queryset = Ingredient.objects.all()
