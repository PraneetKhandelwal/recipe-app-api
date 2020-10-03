from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tag
from recipe.serializers import TagSerializer

TAG_URL = reverse("recipe:tag-list")


class Public_Tag_API_test(TestCase):
    """Test publically available tags api"""
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_tags_unauthorized(self):
        """
        Test that the list of tags cant be accessed without authentication
        """
        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class Private_Tag_API_Test(TestCase):
    """Test for Tag API endpoints that require authentication"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email_add="user1@firstapp.com",
            password="awesome1"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags_authorized(self):
        """
        Test that tags can be retrieved after authentication
        """
        Tag.objects.create(
            user=self.user,
            name="Vegan"
        )
        Tag.objects.create(
            user=self.user,
            name="NonVeg"
        )
        res = self.client.get(TAG_URL)
        tags_model = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags_model, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_tags_user_authenticated(self):
        """
        Test that only the tags for the logged in users are returned
        """
        tag1 = Tag.objects.create(
            user=self.user,
            name="Vegan"
        )
        tag2 = Tag.objects.create(
            user=self.user,
            name="NonVeg"
        )
        user2 = get_user_model().objects.create_user(
            email_add="user2@firstapp.com",
            password="testuser2"
        )
        Tag.objects.create(
            user=user2,
            name="Dessert"
        )
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['name'], tag1.name)
        self.assertEqual(res.data[1]['name'], tag2.name)

    def test_create_tag_success(self):
        """Test if the tag is created successfully by the API"""
        payload = {
            "name": "Vegan"
        }
        res = self.client.post(TAG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_invalid_tag_fail(self):
        """Test the tagname is validated before creation"""
        payload = {
            "name": ""
        }
        res = self.client.post(TAG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
