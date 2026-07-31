import json
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from openpyxl import Workbook

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


class EmployeeImportViewTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')
        self.client.force_login(self.superuser)

    def _build_excel_bytes(self):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = 'Employees'
        sheet.append([
            'username', 'password', 'email', 'person_number', 'full_name_en', 'full_name_vn', 'dob',
            'gender', 'discipline', 'job_title', 'floor', 'working_type', 'identity_number',
            'native_place', 'ethnicity', 'religion', 'education_level', 'specialization', 'address',
            'trade_union_member', 'membership_type_by_admin', 'membership_since'
        ])
        sheet.append([
            'alice', 'secret123', 'alice@example.com', 'P001', 'Alice Updated', 'Alice Updated', '2000-01-01',
            'Male', 'IT', 'Engineer', '1', 'Full Time', '123456789', 'Hanoi', 'Kinh', 'None', 'Bachelor', 'Software',
            'Address 1', 'True', 'Yes', '2024-01-01'
        ])
        sheet.append([
            'bob', 'secret123', 'bob@example.com', 'P002', 'Bob', 'Bob', '1999-02-02',
            'Male', 'IT', 'Engineer', '1', 'Full Time', '987654321', 'Hanoi', 'Kinh', 'None', 'Bachelor', 'Software',
            'Address 2', 'True', 'Yes', '2024-01-01'
        ])
        buffer = BytesIO()
        workbook.save(buffer)
        return buffer.getvalue()

    def test_import_view_creates_and_updates_employees(self):
        existing = Employee.objects.create(
            user=User.objects.create_user(username='alice', password='secret123'),
            person_number='P001',
            full_name_en='Old Name',
            full_name_vn='Old Name',
            email='alice@example.com',
            dob='2000-01-01',
            identity_number='123456789',
            trade_union_member=True,
        )

        excel_bytes = self._build_excel_bytes()
        uploaded_file = SimpleUploadedFile('employees.xlsx', excel_bytes, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response = self.client.post(
            reverse('import_employees'),
            {'excel_file': uploaded_file, 'mode': 'create_or_update'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        existing.refresh_from_db()
        self.assertEqual(existing.full_name_en, 'Alice Updated')
        self.assertTrue(Employee.objects.filter(user__username='bob').exists())
        self.assertContains(response, 'Imported')
