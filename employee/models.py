from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Các model động cho lựa chọn
class Discipline(models.Model):
	name = models.CharField(max_length=50, unique=True)
	def __str__(self):
		return self.name

class JobTitle(models.Model):
	name = models.CharField(max_length=50, unique=True)
	def __str__(self):
		return self.name

class Floor(models.Model):
	name = models.CharField(max_length=20, unique=True)
	def __str__(self):
		return self.name

class Gender(models.Model):
	name = models.CharField(max_length=10, unique=True)
	def __str__(self):
		return self.name

class WorkingType(models.Model):
	name = models.CharField(max_length=30, unique=True)
	def __str__(self):
		return self.name

class Employee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	person_number = models.CharField(max_length=20, unique=True)
	full_name_en = models.CharField(max_length=100)
	full_name_vn = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	dob = models.DateField()
	gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
	discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True)
	job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
	floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True)
	working_type = models.ForeignKey(WorkingType, on_delete=models.SET_NULL, null=True)
	identity_number = models.CharField(max_length=20, unique=True)
	native_place = models.CharField(max_length=100, blank=True)
	ethnicity = models.CharField(max_length=50, blank=True)
	religion = models.CharField(max_length=50, blank=True)
	education_level = models.CharField(max_length=100, blank=True)
	specialization = models.CharField(max_length=100, blank=True)
	address = models.CharField(max_length=200, blank=True)
	trade_union_member = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.person_number} - {self.full_name_en}"

class Children(models.Model):
	employee = models.ForeignKey(Employee, related_name='children', on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	dob = models.DateField()

	def __str__(self):
		return f"{self.name} ({self.dob})"

class EditHistory(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	edit_time = models.DateTimeField(auto_now_add=True)
	changes = models.TextField()

	def __str__(self):
		return f"Edit by {self.edited_by} on {self.edit_time}"