from django.contrib import admin
from .models import (
    Employee, Children, Discipline, JobTitle, Floor,
    Gender, WorkingType, EditHistory, MembershipTypeByAdmin
)

admin.site.register(Employee)
admin.site.register(Children)
admin.site.register(Discipline)
admin.site.register(JobTitle)
admin.site.register(Floor)
admin.site.register(Gender)
admin.site.register(WorkingType)
admin.site.register(EditHistory)
admin.site.register(MembershipTypeByAdmin)