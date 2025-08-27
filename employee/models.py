# Model quản lý danh sách TU committee
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Các model động cho lựa chọn
class TUCommittee(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tu_committees')

	FLOOR_CHOICES = [
		('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
		('6', '6'), ('7', '7'), ('9', '9'), ('10', '10'), ('11', '11'),
		('Hanoi', 'Hanoi'), ('Club Administrator', 'Club Administrator'), ('Overall', 'Overall')
	]
	POSITION_CHOICES = [
		('President', 'President'),
		('Vice President', 'Vice President'),
		('Standing Committee Member', 'Standing Committee Member'),
		('Executive Committee Member', 'Executive Committee Member'),
		('Head of the Inspection Committee', 'Head of the Inspection Committee'),
		('Member of the Inspection Committee', 'Member of the Inspection Committee'),
		('Trade Union Accountant', 'Trade Union Accountant'),
		('Trade Union Treasurer', 'Trade Union Treasurer'),
	]
	position = models.CharField(max_length=50, choices=POSITION_CHOICES, blank=True)
	email = models.EmailField(blank=True)
	joined_at = models.DateField(null=True, blank=True)
	responsible_floor = models.CharField(max_length=30, choices=FLOOR_CHOICES, blank=True)

	def __str__(self):
		return f"{self.user.username} - {self.position}"
	
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

class MembershipTypeByAdmin(models.Model):
	name = models.CharField(max_length=50, unique=True)
	def __str__(self):
		return self.name
class Employee(models.Model):
	def save(self, *args, **kwargs):
		# Nếu trade_union_member là True thì gán MembershipTypeByAdmin là 'Yes', False thì là 'No'
		if self.membership_type_by_admin is None:
			if self.trade_union_member:
				default_type = MembershipTypeByAdmin.objects.filter(name__iexact='Yes').first()
			else:
				default_type = MembershipTypeByAdmin.objects.filter(name__iexact='No').first()
			if default_type:
				self.membership_type_by_admin = default_type
		# Tự động set membership_since nếu chưa có
		if not self.membership_since:
			from django.utils import timezone
			self.membership_since = timezone.now()
		super().save(*args, **kwargs)

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
	membership_type_by_admin = models.ForeignKey(MembershipTypeByAdmin, on_delete=models.SET_NULL, null=True, blank=True)
	membership_since = models.DateTimeField(null=True, blank=True)

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