from django import forms
from django.utils.crypto import get_random_string
class EmployeeLoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True, label='Password')
from django.contrib.auth.models import User
from .models import Employee, Discipline, JobTitle, Floor, Gender, WorkingType

class EmployeeRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, help_text='Use to login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # ...existing code...

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username đã tồn tại. Vui lòng chọn username khác.')
        return username
    username = forms.CharField(max_length=150, required=True, help_text='Use to login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    email = forms.EmailField(required=True, help_text='Please fill Endava email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    full_name_en = forms.CharField(max_length=100, required=True, label='Full name (EN)', widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name_vn = forms.CharField(max_length=100, required=True, label='Full name (VI)', widget=forms.TextInput(attrs={'class': 'form-control'}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=True, label='Date of Birth')
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    job_title = forms.ModelChoiceField(queryset=JobTitle.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    floor = forms.ModelChoiceField(queryset=Floor.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    working_type = forms.ModelChoiceField(queryset=WorkingType.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    identity_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    native_place = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ethnicity = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    religion = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    education_level = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialization = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    TRADE_UNION_CHOICES = ((True, 'Yes'), (False, 'No'))
    trade_union_member = forms.ChoiceField(
        choices=TRADE_UNION_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True,
        label='Trade Union member'
    )

    class Meta:
        model = Employee
        fields = [
            'username', 'password', 'email', 'full_name_en', 'full_name_vn', 'dob', 'gender',
            'discipline', 'job_title', 'floor', 'working_type', 'identity_number', 'native_place', 'ethnicity',
            'religion', 'education_level', 'specialization', 'address', 'trade_union_member'
        ]

    def save(self, commit=True):
        
        # Nếu có trường username thì tạo User mới (đăng ký), nếu không thì chỉ cập nhật Employee
        if 'username' in self.cleaned_data:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password']
            )
            employee = super().save(commit=False)
            employee.user = user
        else:
            employee = super().save(commit=False)
        # Chuyển đổi giá trị từ radio sang boolean
        employee.trade_union_member = True if self.cleaned_data.get('trade_union_member', False) == 'True' else False
        # Ensure unique person_number
        if not employee.person_number:
            while True:
                rand_num = get_random_string(8)
                if not Employee.objects.filter(person_number=rand_num).exists():
                    employee.person_number = rand_num
                    break
        if commit:
            employee.save()
        return employee
