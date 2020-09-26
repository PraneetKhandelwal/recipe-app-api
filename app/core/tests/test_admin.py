from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@firstapp.com',
            password='admin123'
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='nonadmin@firstapp.com',
            password='nonadmin123',
            name='Non Admin'
        )

    def test_users_listing_by_admin(self):
        """Test that users are listed on users page"""
        url = reverse("admin:core_user_changelist")
        resp = self.client.get(url)

        self.assertContains(resp, self.user.name)
        self.assertContains(resp, self.user.email_add)

    def test_user_edit_page(self):
        """Test that user edit page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_user_create_page(self):
        """Test that user create page works"""
        url = reverse("admin:core_user_add")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
