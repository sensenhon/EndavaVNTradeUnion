import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Employee


class SecurityAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='secret123')
        self.employee = Employee.objects.create(
            user=self.user,
            person_number='P001',
            full_name_en='Alice',
            full_name_vn='Alice',
            email='alice@example.com',
            dob='2000-01-01',
            identity_number='123456789',
            trade_union_member=True,
        )

    def test_gift_update_endpoint_requires_login(self):
        response = self.client.post(
            reverse('update_birthday_gift'),
            data=json.dumps({'id': self.employee.id, 'value': True}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_financial_edit_requires_login(self):
        response = self.client.get(reverse('edit_financial_transaction', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_club_financial_delete_requires_login(self):
        response = self.client.post(reverse('delete_club_financial_transaction', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])
