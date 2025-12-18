from rest_framework import serializers
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_field
from .models import Employee, Department, Position, EmployeeDocument, Attendance, LeaveRequest


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model"""
    manager_name = serializers.CharField(source='manager.full_name', read_only=True)
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'manager', 'manager_name', 
                  'employee_count', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    @extend_schema_field(serializers.IntegerField)
    def get_employee_count(self, obj) -> int:
        return obj.employees.filter(status='active').count()


class PositionSerializer(serializers.ModelSerializer):
    """Serializer for Position model"""
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Position
        fields = ['id', 'title', 'description', 'min_salary', 'max_salary', 
                  'employee_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    @extend_schema_field(serializers.IntegerField)
    def get_employee_count(self, obj) -> int:
        return obj.employees.filter(status='active').count()


class EmployeeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for employee lists"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    position_title = serializers.CharField(source='position.title', read_only=True)
    manager_name = serializers.CharField(source='manager.full_name', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'first_name', 'last_name', 'full_name', 
                  'email', 'phone', 'department_name', 'position_title', 
                  'employment_type', 'status', 'manager_name', 'date_joined']
        read_only_fields = ['id', 'full_name']


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for employee with all fields"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    position_title = serializers.CharField(source='position.title', read_only=True)
    manager_name = serializers.CharField(source='manager.full_name', read_only=True)
    age = serializers.IntegerField(read_only=True)
    years_of_service = serializers.IntegerField(read_only=True)
    subordinate_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'full_name', 'age', 'years_of_service']
    
    @extend_schema_field(serializers.IntegerField)
    def get_subordinate_count(self, obj) -> int:
        return obj.subordinates.filter(status='active').count()


class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating employees"""
    
    class Meta:
        model = Employee
        exclude = ['created_at', 'updated_at', 'created_by']
    
    def validate_email(self, value):
        """Ensure email is unique"""
        instance = self.instance
        if Employee.objects.filter(email=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("An employee with this email already exists.")
        return value
    
    def validate_employee_id(self, value):
        """Ensure employee_id is unique"""
        instance = self.instance
        if Employee.objects.filter(employee_id=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("An employee with this ID already exists.")
        return value
    
    def validate(self, data):
        """Cross-field validation"""
        if data.get('date_left') and data.get('date_joined'):
            if data['date_left'] < data['date_joined']:
                raise serializers.ValidationError("Date left cannot be before date joined.")
        
        if data.get('salary'):
            position = data.get('position', self.instance.position if self.instance else None)
            if position:
                if position.min_salary and data['salary'] < position.min_salary:
                    raise serializers.ValidationError(f"Salary cannot be less than position minimum: {position.min_salary}")
                if position.max_salary and data['salary'] > position.max_salary:
                    raise serializers.ValidationError(f"Salary cannot exceed position maximum: {position.max_salary}")
        
        return data


class EmployeeDocumentSerializer(serializers.ModelSerializer):
    """Serializer for employee documents"""
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    
    class Meta:
        model = EmployeeDocument
        fields = ['id', 'employee', 'employee_name', 'document_type', 'title', 
                  'file', 'uploaded_by', 'uploaded_by_name', 'uploaded_at', 'notes']
        read_only_fields = ['id', 'uploaded_at', 'uploaded_by']


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for attendance records"""
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'employee_name', 'employee_id', 'date', 
                  'check_in', 'check_out', 'status', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate attendance data"""
        if data.get('check_out') and data.get('check_in'):
            if data['check_out'] < data['check_in']:
                raise serializers.ValidationError("Check-out time cannot be before check-in time.")
        return data


class LeaveRequestSerializer(serializers.ModelSerializer):
    """Serializer for leave requests"""
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    total_days = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = LeaveRequest
        fields = ['id', 'employee', 'employee_name', 'employee_id', 'leave_type', 
                  'start_date', 'end_date', 'total_days', 'reason', 'status', 
                  'approved_by', 'approved_by_name', 'approval_date', 
                  'rejection_reason', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'approved_by', 'approval_date']
    
    def validate(self, data):
        """Validate leave request dates"""
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError("End date cannot be before start date.")
        return data


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    total_employees = serializers.IntegerField()
    active_employees = serializers.IntegerField()
    on_leave = serializers.IntegerField()
    total_departments = serializers.IntegerField()
    pending_leave_requests = serializers.IntegerField()
    employees_by_department = serializers.DictField()
    employees_by_employment_type = serializers.DictField()
    recent_hires = serializers.ListField()
