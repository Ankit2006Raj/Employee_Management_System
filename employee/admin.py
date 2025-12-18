from django.contrib import admin
from django.utils.html import format_html
from .models import Employee, Department, Position, EmployeeDocument, Attendance, LeaveRequest


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'manager', 'employee_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def employee_count(self, obj):
        return obj.employees.filter(status='active').count()
    employee_count.short_description = 'Active Employees'


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'min_salary', 'max_salary', 'employee_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def employee_count(self, obj):
        return obj.employees.filter(status='active').count()
    employee_count.short_description = 'Active Employees'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'email', 'department', 'position', 'status_badge', 'date_joined']
    list_filter = ['status', 'employment_type', 'department', 'position', 'gender', 'date_joined']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'age', 'years_of_service']
    date_hierarchy = 'date_joined'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee_id', 'first_name', 'last_name', 'email', 'phone', 
                      'date_of_birth', 'gender', 'photo')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country'),
            'classes': ('collapse',)
        }),
        ('Employment Details', {
            'fields': ('department', 'position', 'employment_type', 'status', 
                      'date_joined', 'date_left', 'salary', 'manager')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('user', 'created_by', 'created_at', 'updated_at', 'age', 'years_of_service', 'notes'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'active': 'green',
            'on_leave': 'orange',
            'terminated': 'red',
            'resigned': 'gray'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'employee', 'document_type', 'uploaded_by', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['title', 'employee__first_name', 'employee__last_name']
    readonly_fields = ['uploaded_at']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'check_in', 'check_out', 'status', 'created_at']
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'total_days', 'status_badge', 'created_at']
    list_filter = ['status', 'leave_type', 'start_date', 'created_at']
    search_fields = ['employee__first_name', 'employee__last_name', 'reason']
    readonly_fields = ['created_at', 'updated_at', 'total_days']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Leave Information', {
            'fields': ('employee', 'leave_type', 'start_date', 'end_date', 'total_days', 'reason')
        }),
        ('Approval', {
            'fields': ('status', 'approved_by', 'approval_date', 'rejection_reason')
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red',
            'cancelled': 'gray'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def save_model(self, request, obj, form, change):
        if obj.status in ['approved', 'rejected'] and not obj.approved_by:
            obj.approved_by = request.user
            from django.utils import timezone
            obj.approval_date = timezone.now()
        super().save_model(request, obj, form, change)
