from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
import os


def employee_photo_path(instance, filename):
    """Generate file path for employee photo"""
    ext = filename.split('.')[-1]
    filename = f'employee_{instance.employee_id}.{ext}'
    return os.path.join('employee_photos', filename)


class Department(models.Model):
    """Department model for organizing employees"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    manager = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_departments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Departments'


class Position(models.Model):
    """Job position/title model"""
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    min_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']


class Employee(models.Model):
    """Enhanced Employee model with comprehensive fields"""
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('CT', 'Contract'),
        ('IN', 'Intern'),
        ('FR', 'Freelance'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('terminated', 'Terminated'),
        ('resigned', 'Resigned'),
    ]
    
    # Basic Information
    employee_id = models.CharField(max_length=20, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, db_index=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N')
    photo = models.ImageField(upload_to=employee_photo_path, null=True, blank=True)
    
    # Address Information
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='USA')
    
    # Employment Information
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employees')
    position = models.ForeignKey(Position, on_delete=models.PROTECT, related_name='employees')
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPE_CHOICES, default='FT')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)
    date_joined = models.DateField(default=timezone.now)
    date_left = models.DateField(null=True, blank=True)
    
    # Compensation
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Reporting Structure
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=17, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    
    # System Fields
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_profile')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_employees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional Information
    notes = models.TextField(blank=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    @property
    def years_of_service(self):
        if self.date_joined:
            end_date = self.date_left if self.date_left else timezone.now().date()
            return (end_date - self.date_joined).days // 365
        return 0
    
    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"
    
    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        indexes = [
            models.Index(fields=['employee_id', 'email']),
            models.Index(fields=['status', 'department']),
        ]


class EmployeeDocument(models.Model):
    """Model for storing employee documents"""
    
    DOCUMENT_TYPE_CHOICES = [
        ('resume', 'Resume/CV'),
        ('contract', 'Employment Contract'),
        ('id_proof', 'ID Proof'),
        ('certificate', 'Certificate'),
        ('other', 'Other'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='employee_documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.title}"
    
    class Meta:
        ordering = ['-uploaded_at']


class Attendance(models.Model):
    """Track employee attendance"""
    
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('late', 'Late'),
        ('on_leave', 'On Leave'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(db_index=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.date}"
    
    class Meta:
        ordering = ['-date']
        unique_together = ['employee', 'date']
        verbose_name_plural = 'Attendance Records'


class LeaveRequest(models.Model):
    """Employee leave request management"""
    
    LEAVE_TYPE_CHOICES = [
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('annual', 'Annual Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('unpaid', 'Unpaid Leave'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type} ({self.start_date} to {self.end_date})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Leave Request'
        verbose_name_plural = 'Leave Requests'
