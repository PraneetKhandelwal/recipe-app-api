from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse("recipe:ingredient-list")


class Public_Ingredients_API_test(TestCase):
    """Test publically available ingredients api"""
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_ingredients_unauthorized(self):
        """
        Test that the list of ingredients
        cant be accessed without authentication
        """
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class Private_Ingredients_API_Test(TestCase):
    """Test for private Ingredient API endpoints"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email_add="user1@firstapp.com",
            password="awesome1"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredients_authorized(self):
        """
        Test that ingredients can be retrieved after authentication
        """
        Ingredient.objects.create(
            user=self.user,
            name="Carrot"
        )
        Ingredient.objects.create(
            user=self.user,
            name="Salt"
        )
        res = self.client.get(INGREDIENTS_URL)
        ingredients_model = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients_model, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_ingredients_user_authenticated(self):
        """
        Test that only the ingredients for the logged in users are returned
        """
        ingredient1 = Ingredient.objects.create(
            user=self.user,
            name="Salt"
        )
        ingredient2 = Ingredient.objects.create(
            user=self.user,
            name="Milk"
        )
        user2 = get_user_model().objects.create_user(
            email_add="user2@firstapp.com",
            password="testuser2"
        )
        Ingredient.objects.create(
            user=user2,
            name="Sugar"
        )
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['name'], ingredient1.name)
        self.assertEqual(res.data[1]['name'], ingredient2.name)

    def test_create_ingredient_success(self):
        """Test if the ingredient is created successfully by the API"""
        payload = {
            "name": "Raddish"
        }
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_invalid_ingredient_fail(self):
        """Test the ingredient name is validated before creation"""
        payload = {
            "name": ""
        }
        res = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
