from django import forms
from django.core.exceptions import ValidationError
from .models import Employee, Department, Position, LeaveRequest, Attendance


class EmployeeForm(forms.ModelForm):
    """Enhanced form for Employee model"""
    
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'photo',
            'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country',
            'department', 'position', 'employment_type', 'status',
            'date_joined', 'date_left', 'salary', 'manager',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
            'notes'
        ]
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'EMP001'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apt, Suite, etc.'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'date_joined': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_left': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '50000.00'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Contact Name'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Phone'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes...'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Employee.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError("An employee with this email already exists.")
        return email
    
    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        if Employee.objects.filter(employee_id=employee_id).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError("An employee with this ID already exists.")
        return employee_id
    
    def clean(self):
        cleaned_data = super().clean()
        date_joined = cleaned_data.get('date_joined')
        date_left = cleaned_data.get('date_left')
        
        if date_left and date_joined and date_left < date_joined:
            raise ValidationError("Date left cannot be before date joined.")
        
        return cleaned_data


class DepartmentForm(forms.ModelForm):
    """Form for Department model"""
    
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'manager', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DEPT'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PositionForm(forms.ModelForm):
    """Form for Position model"""
    
    class Meta:
        model = Position
        fields = ['title', 'description', 'min_salary', 'max_salary']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'min_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum Salary'}),
            'max_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maximum Salary'}),
        }


class LeaveRequestForm(forms.ModelForm):
    """Form for Leave Request"""
    
    class Meta:
        model = LeaveRequest
        fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for leave...'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if end_date and start_date and end_date < start_date:
            raise ValidationError("End date cannot be before start date.")
        
        return cleaned_data


class AttendanceForm(forms.ModelForm):
    """Form for Attendance"""
    
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'check_in', 'check_out', 'status', 'notes']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_in': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'check_out': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class EmployeeSearchForm(forms.Form):
    """Form for searching employees"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, email, or employee ID...'
        })
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='All Departments'
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='All Positions'
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Employee.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    employment_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Employee.EMPLOYMENT_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
