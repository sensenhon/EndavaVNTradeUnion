from django.conf import settings
from django.db import models
from django.utils import timezone
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
	birthday_gift_received = models.BooleanField(default=False, help_text='Had received birthday gift for the current year')
	tet_gift_received = models.BooleanField(default=False, help_text='Had received Tet gift for the current year')
	mooncake_gift_received = models.BooleanField(default=False, help_text='Had received Moon Cake gift for the current year')
	luckymoney_gift_received = models.BooleanField(default=False, help_text='Had received Lucky Money gift for the current year')

	def __str__(self):
		return f"{self.person_number} - {self.full_name_en}"

class Children(models.Model):
	employee = models.ForeignKey(Employee, related_name='children', on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	dob = models.DateField()
	june_gift_received = models.BooleanField(default=False, help_text='Received June Children gift for the current year')
	autumn_gift_received = models.BooleanField(default=False, help_text='Received Autumn Children gift for the current year')

	def __str__(self):
		return f"{self.name} ({self.dob})"

class EditHistory(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	edit_time = models.DateTimeField(auto_now_add=True)
	changes = models.TextField()

	def __str__(self):
		return f"Edit by {self.edited_by} on {self.edit_time}"

class EmployeeGiftYear(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	year = models.IntegerField()
	gift_type = models.CharField(max_length=50)
	received = models.BooleanField(default=False)

	def june_gift_checked_count(self):
		if self.gift_type == 'june':
			return self.employee.children.filter(june_gift_received=True).count()
		return ''
	june_gift_checked_count.short_description = 'June Gift Checked'

	def autumn_gift_checked_count(self):
		if self.gift_type == 'autumn':
			return self.employee.children.filter(autumn_gift_received=True).count()
		return ''
	autumn_gift_checked_count.short_description = 'Autumn Gift Checked'

	class Meta:
		unique_together = ('employee', 'year', 'gift_type')
		
	def __str__(self):
		return f"{self.employee} - {self.year} - {self.gift_type}"

class FinancialCategory(models.Model):
	TYPE_CHOICES = (
		('income', 'Thu'),
		('expense', 'Chi'),
	)
	code = models.CharField(max_length=20, unique=True)
	name = models.CharField(max_length=100)
	type = models.CharField(max_length=10, choices=TYPE_CHOICES)
	estimated_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text='Estimated expense/income for this category')

	def __str__(self):
		return f"{self.code} - {self.name}"


class FinancialDescription(models.Model):
	TYPE_CHOICES = (
		('income', 'Thu'),
		('expense', 'Chi'),
	)
	category = models.ForeignKey(FinancialCategory, on_delete=models.CASCADE, related_name='descriptions')
	description = models.CharField(max_length=255, unique=True)
	type = models.CharField(max_length=10, choices=TYPE_CHOICES)
	estimated_expense = models.DecimalField(default=0, max_digits=15, decimal_places=2, help_text='Estimated budget for this description')

	def __str__(self):
		return f"{self.description}"

class TUFinancialTransaction(models.Model):
    FINANCIAL_TYPE_CHOICES = (
        ('income', 'Thu'),
        ('expense', 'Chi'),
    )
    category = models.ForeignKey(FinancialCategory, on_delete=models.PROTECT)
    date = models.DateField()
    payment_id = models.CharField(max_length=255)
    description = models.ForeignKey(FinancialDescription, on_delete=models.PROTECT)
    details = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    financial_type = models.CharField(max_length=10, choices=FINANCIAL_TYPE_CHOICES)
    payment_evidence = models.ImageField(upload_to='financial_evidence/', null=True, blank=True)
    created_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"TU {self.get_financial_type_display()} - {self.category} - {self.amount} VND on {self.date}"

class FloorFinancialTransaction(models.Model):
    FINANCIAL_TYPE_CHOICES = (
        ('income', 'Thu'),
        ('expense', 'Chi'),
    )
    floor = models.ForeignKey('Floor', on_delete=models.CASCADE)
    category = models.ForeignKey(FinancialCategory, on_delete=models.PROTECT)
    date = models.DateField()
    payment_id = models.CharField(max_length=255)
    description = models.ForeignKey(FinancialDescription, on_delete=models.PROTECT)
    details = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    financial_type = models.CharField(max_length=10, choices=FINANCIAL_TYPE_CHOICES)
    payment_evidence = models.ImageField(upload_to='financial_evidence/', null=True, blank=True)
    created_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Floor {self.floor} {self.get_financial_type_display()} - {self.category} - {self.amount} VND on {self.date}"

class ClubFinancialTransaction(models.Model):
    FINANCIAL_TYPE_CHOICES = (
        ('income', 'Thu'),
        ('expense', 'Chi'),
    )
    club_name = models.CharField(max_length=100)
    category = models.ForeignKey(FinancialCategory, on_delete=models.PROTECT)
    date = models.DateField()
    payment_id = models.CharField(max_length=255)
    description = models.ForeignKey(FinancialDescription, on_delete=models.PROTECT)
    details = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    financial_type = models.CharField(max_length=10, choices=FINANCIAL_TYPE_CHOICES)
    payment_evidence = models.ImageField(upload_to='financial_evidence/', null=True, blank=True)
    created_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Club {self.club_name} {self.get_financial_type_display()} - {self.category} - {self.amount} VND on {self.date}"

class FinancialOpeningBalance(models.Model):
    TYPE_CHOICES = (
        ('tu', 'TU'),
        ('floor', 'Floor'),
        ('club', 'Club'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField(null=True, blank=True)
    opening_balance = models.DecimalField(max_digits=15, decimal_places=0)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('type', 'year', 'month')

    def __str__(self):
        if self.month:
            return f"Opening Balance {self.get_type_display()} {self.month}/{self.year}: {self.opening_balance} VND"
        return f"Opening Balance {self.get_type_display()} {self.year}: {self.opening_balance} VND"

class TUFinancialReport(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField(null=True, blank=True)
    opening_balance = models.DecimalField(max_digits=15, decimal_places=0)
    closing_balance = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        if self.month:
            return f"TU Report {self.month}/{self.year}"
        return f"TU Report {self.year}"

class FloorFinancialReport(models.Model):
    floor = models.ForeignKey('Floor', on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField(null=True, blank=True)
    opening_balance = models.DecimalField(max_digits=15, decimal_places=0)
    closing_balance = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        if self.month:
            return f"Floor {self.floor} Report {self.month}/{self.year}"
        return f"Floor {self.floor} Report {self.year}"

class ClubFinancialReport(models.Model):
    club_name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField(null=True, blank=True)
    opening_balance = models.DecimalField(max_digits=15, decimal_places=0)
    closing_balance = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        if self.month:
            return f"Club {self.club_name} Report {self.month}/{self.year}"
        return f"Club {self.club_name} Report {self.year}"