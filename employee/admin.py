from django.contrib import admin
from .models import (
    Employee, Children, Discipline, JobTitle, Floor,
    Gender, WorkingType, EditHistory, MembershipTypeByAdmin, TUCommittee
)

# Import EmployeeImportAdmin for Excel import
from .admin_import import EmployeeImportAdmin

# admin.site.register(Employee)
admin.site.register(TUCommittee)
admin.site.register(Children)
admin.site.register(Discipline)
admin.site.register(JobTitle)
admin.site.register(Floor)
admin.site.register(Gender)
admin.site.register(WorkingType)
admin.site.register(EditHistory)
admin.site.register(MembershipTypeByAdmin)

# Register Employee with EmployeeImportAdmin for Excel import
admin.site.register(Employee, EmployeeImportAdmin)