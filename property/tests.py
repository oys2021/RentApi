from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from authentication.models import User
from property.models import Property, Lease
from django.contrib.auth.hashers import make_password
from datetime import date, timedelta

class PropertyLeaseTests(APITestCase):
    def setUp(self):
        self.landlord = User.objects.create(
            username="landlord1",
            email="landlord@example.com",
            password=make_password("Pass12345"),
            role="Landlord",
            is_verified=True
        )

        self.tenant = User.objects.create(
            username="tenant1",
            email="tenant@example.com",
            password=make_password("Pass12345"),
            role="Tenant",
            is_verified=True
        )

        self.client.force_authenticate(user=self.landlord)

        self.property = Property.objects.create(
            name="Luxury Apartment",
            address="123 Main Street",
            landlord=self.landlord,
            rent_price=1200.00
        )


    def test_create_property(self):
        """Landlord can create a property"""
        data = {
            "name": "New Property",
            "address": "456 Second Street",
            "rent_price": 1500.00
        }
        response = self.client.post(reverse('property', args=[self.landlord.username]), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 2)

    def test_get_landlord_properties(self):
        """Landlord can view their properties"""
        response = self.client.get(reverse('property', args=[self.landlord.username]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_update_property(self):
        """Landlord can update their property"""
        url = reverse('property_detail', args=[self.property.id])
        data = {"name": "Updated Property Name"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.property.refresh_from_db()
        self.assertEqual(self.property.name, "Updated Property Name")


    def test_create_lease(self):
        self.client.force_authenticate(user=self.tenant)
        data = {
            "property": self.property.id,
            "tenant": self.tenant.id,
            "start_date": date.today(),
            "end_date": date.today() + timedelta(days=365),
            "rent_amount": 1200.00,
            "status": "Active"
        }
        response = self.client.post(reverse('lease'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lease.objects.count(), 1)

    def test_prevent_duplicate_lease(self):
        Lease.objects.create(
            tenant=self.tenant,
            property=self.property,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            rent_amount=1200.00,
            status="Active"
        )
        self.client.force_authenticate(user=self.tenant)
        data = {
            "property": self.property.id,
            "tenant": self.tenant.id,
            "start_date": date.today(),
            "end_date": date.today() + timedelta(days=365),
            "rent_amount": 1200.00,
            "status": "Active"
        }
        response = self.client.post(reverse('lease'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_leases_public(self):
        Lease.objects.create(
            tenant=self.tenant,
            property=self.property,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            rent_amount=1200.00,
            status="Active"
        )
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('leases'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
