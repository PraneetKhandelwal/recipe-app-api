from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class Public_User_API_Test(TestCase):
    """Test Public user API endpoint"""
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test if the user is created successfully by the API"""
        payload = {
            "email_add": "test@firstapp.com",
            "password": "test123",
            "name": "Test Full Name"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # this step is to check the user that got created in the DB
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))

        # this is to check the password is not
        # returned as part of the api response
        self.assertNotIn('password', res.data)

    def test_create_user_already_exists(self):
        """Test creating a user which already exists fails"""
        payload = {
            "email_add": "test@firstapp.com",
            "password": "test123"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test the password must be more than 5 characters"""
        payload = {
            "email_add": "test@firstapp.com",
            "password": "test",
            "name": "Test Full Name"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # this step is to check the user never got created in the DB
        user_exists = get_user_model().objects.filter(
            email_add=payload['email_add']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_user(self):
        """Test that a token was created for a user correctly"""
        payload = {
            "email_add": "test@firstapp.com",
            "password": "test",
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # this is to check the token is returned as part of the api response
        # We wont be checking the authenticity of the token created as
        # we will be using Django's internal authentication system
        self.assertIn('token', res.data)

    def test_token_not_created_invalid_cred(self):
        """Test that a token was not created for invalid credentials"""
        payload = {
            "email_add": "test@firstapp.com",
            "password": "bad_pass",
        }
        create_user(email_add="test@firstapp.com", password="test")
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_not_created_unknown_user(self):
        """Test that a token was not created for unknown user"""
        payload = {
            "email_add": "test@firstapp.com",
            "password": "test",
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_not_created_no_password_for_existing_user(self):
        """
        Test that a token was not created
        for no password in payload for exisiting user
        """
        payload = {
            "email_add": "test@firstapp.com"
        }
        create_user(email_add="test@firstapp.com", password="test")
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_not_created_empty_password_for_existing_user(self):
        """
        Test that a token was not created
        for empty password provided for exisiting user
        """
        payload = {
            "email_add": "test@firstapp.com",
            "password": ""
        }
        create_user(email_add="test@firstapp.com", password="test")
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
