from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from authentication.models import User
from django.contrib.auth.hashers import make_password

class UserRegistrationTests(APITestCase):
    def test_user_registration_success(self):
        data = {
            "username": "testuser",
            "password": "StrongPass123",
            "email": "testuser@example.com",
            "phone": "+1234567890",
            "firstname": "Test",
            "lastname": "User",
            "role": "Tenant",
            "is_verified": True
        }
        response = self.client.post(reverse('register_user'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_registration_existing_username(self):
        User.objects.create(username="testuser", email="existing@example.com", password=make_password("123"))
        data = {
            "username": "testuser",
            "password": "AnotherPass123",
            "email": "newemail@example.com"
        }
        response = self.client.post(reverse('register_user'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_user_registration_existing_email(self):
        User.objects.create(username="anotheruser", email="duplicate@example.com", password=make_password("123"))
        data = {
            "username": "newuser",
            "password": "AnotherPass123",
            "email": "duplicate@example.com"
        }
        response = self.client.post(reverse('register_user'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

class UserLoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="loginuser",
            email="login@example.com",
            password=make_password("LoginPass123"),
            role="Tenant",
            is_verified=True
        )

    def test_login_success(self):
        data = {
            "username": "loginuser",
            "password": "LoginPass123"
        }
        response = self.client.post(reverse('userlogin'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_login_wrong_password(self):
        data = {
            "username": "loginuser",
            "password": "WrongPass"
        }
        response = self.client.post(reverse('userlogin'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_unverified_user(self):
        self.user.is_verified = False
        self.user.save()
        data = {
            "username": "loginuser",
            "password": "LoginPass123"
        }
        response = self.client.post(reverse('userlogin'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

class PasswordResetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="resetme",
            email="reset@example.com",
            password=make_password("OldPassword123"),
            is_verified=True
        )

    def test_password_reset_success(self):
        data = {
            "username": "resetme",
            "new_password": "NewStrongPass123"
        }
        response = self.client.post(reverse('reset_user'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password reset successfully.")

    def test_password_reset_invalid_username(self):
        data = {
            "username": "nonexistent",
            "new_password": "NewPass123"
        }
        response = self.client.post(reverse('reset_user'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ProfileViewTests(APITestCase):
    def setUp(self):
        User.objects.create(username="tenant1", role="Tenant", email="t1@example.com", password="123")
        User.objects.create(username="tenant2", role="Tenant", email="t2@example.com", password="123")
        User.objects.create(username="admin", role="Admin", email="a@example.com", password="123")

    def test_get_tenant_profiles(self):
        response = self.client.get(reverse('tenant_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
