import pandas as pd
from django.contrib import admin
from django import forms
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Employee, Children, Discipline, Floor, Gender, JobTitle, WorkingType, MembershipTypeByAdmin

class EmployeeImportForm(forms.Form):
    excel_file = forms.FileField()

class EmployeeImportAdmin(admin.ModelAdmin):
    change_list_template = "admin/employee_change_list.html"

    # Remove change_list_template to restore default list view

    # Add import button to changelist view
    def changelist_view(self, request, extra_context=None):
        if not extra_context:
            extra_context = {}
        extra_context['import_excel_url'] = '/admin/employee/import-excel/'
        return super().changelist_view(request, extra_context=extra_context)

    list_display = [field.name for field in Employee._meta.fields if field.name != 'id']
    fields = [field.name for field in Employee._meta.fields if field.name != 'id']

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel), name='employee-import-excel'),
        ]
        return custom_urls + urls

    def import_excel(self, request):
        if request.method == "POST":
            form = EmployeeImportForm(request.POST, request.FILES)
            if form.is_valid():
                df = pd.read_excel(request.FILES['excel_file'])
                imported, errors = 0, []
                for idx, row in df.iterrows():
                    try:
                        username = str(row.get('username')).strip()
                        password = str(row.get('password')).strip()
                        email = str(row.get('email')).strip()
                        # Create user if not exists
                        user, created = User.objects.get_or_create(username=username, defaults={
                            'email': email
                        })
                        if created:
                            user.set_password(password)
                            user.save()
                        # Get or create Employee
                        emp, _ = Employee.objects.get_or_create(user=user, defaults={
                            'person_number': row.get('person_number'),
                            'full_name_en': row.get('full_name_en'),
                            'full_name_vn': row.get('full_name_vn'),
                            'email': email,
                            'dob': row.get('dob'),
                            'gender': Gender.objects.filter(name=row.get('gender')).first(),
                            'discipline': Discipline.objects.filter(name=row.get('discipline')).first(),
                            'job_title': JobTitle.objects.filter(name=row.get('job_title')).first(),
                            'floor': Floor.objects.filter(name=row.get('floor')).first(),
                            'working_type': WorkingType.objects.filter(name=row.get('working_type')).first(),
                            'identity_number': row.get('identity_number'),
                            'native_place': row.get('native_place'),
                            'ethnicity': row.get('ethnicity'),
                            'religion': row.get('religion'),
                            'education_level': row.get('education_level'),
                            'specialization': row.get('specialization'),
                            'address': row.get('address'),
                            'trade_union_member': bool(row.get('trade_union_member')),
                            'membership_type_by_admin': MembershipTypeByAdmin.objects.filter(name=row.get('membership_type_by_admin')).first(),
                            'membership_since': row.get('membership_since'),
                        })
                        # Children: expects a column 'children' as JSON or comma-separated list
                        children_data = row.get('children')
                        if children_data:
                            import json
                            try:
                                children_list = json.loads(children_data)
                            except Exception:
                                children_list = [c.strip() for c in str(children_data).split(',') if c.strip()]
                            for child in children_list:
                                name = child.get('name') if isinstance(child, dict) else child
                                dob = child.get('dob') if isinstance(child, dict) else None
                                Children.objects.get_or_create(employee=emp, name=name, dob=dob)
                        imported += 1
                    except Exception as e:
                        errors.append(f"Row {idx+2}: {e}")
                msg = f"Imported {imported} employees. Errors: {len(errors)}"
                if errors:
                    msg += "\n" + "\n".join(errors)
                self.message_user(request, msg)
        else:
            form = EmployeeImportForm()
        return render(request, "admin/employee_import.html", {"form": form})
