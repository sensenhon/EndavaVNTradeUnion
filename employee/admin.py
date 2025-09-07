from django.contrib import admin
from .models import (
    Employee, Children, Discipline, JobTitle, Floor,
    Gender, WorkingType, EditHistory, MembershipTypeByAdmin, TUCommittee, EmployeeGiftYear
)
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
# admin.site.register(EmployeeGiftYear)
@admin.register(EmployeeGiftYear)
class EmployeeGiftYearAdmin(admin.ModelAdmin):
    list_display = ('employee', 'year', 'gift_type', 'received', 'june_gift_checked_count', 'autumn_gift_checked_count')

# Register Employee with EmployeeImportAdmin for Excel import
admin.site.register(Employee, EmployeeImportAdmin)