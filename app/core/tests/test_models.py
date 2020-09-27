from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_using_email(self):
        """Test creating a new user with an email"""
        test_email = 'praneet@firstapp.com'
        test_password = 'password123'
        user = get_user_model().objects.create_user(
            email_add=test_email,
            password=test_password
        )

        self.assertEqual(user.email_add, test_email)
        self.assertTrue(user.check_password(test_password))

    def test_normalised_email(self):
        """
           Test that email is stored in a normalised format
           irrespective of the case
        """
        test_email = 'praneet@FIRSTAPP.com'
        test_password = 'password123'
        user = get_user_model().objects.create_user(
            email_add=test_email,
            password=test_password
        )

        self.assertEqual(user.email_add, test_email.lower())

    def test_user_creation_without_email(self):
        """Test that user creation without a valid email should raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "dsd")

    def test_create_new_super_user(self):
        """Test creation of a super user"""
        test_email = 'praneet@firstapp.com'
        test_password = 'password123'
        user = get_user_model().objects.create_superuser(
            email_add=test_email,
            password=test_password
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
