from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta

from .models import Employee, Department, Position, EmployeeDocument, Attendance, LeaveRequest
from .serializers import (
    EmployeeListSerializer, EmployeeDetailSerializer, EmployeeCreateUpdateSerializer,
    DepartmentSerializer, PositionSerializer, EmployeeDocumentSerializer,
    AttendanceSerializer, LeaveRequestSerializer, DashboardStatsSerializer
)
from .permissions import IsHROrReadOnly, IsManagerOrHR


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Department CRUD operations
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsHROrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get all employees in a department"""
        department = self.get_object()
        employees = department.employees.filter(status='active')
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)


class PositionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Position CRUD operations
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated, IsHROrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'min_salary', 'max_salary']
    ordering = ['title']


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Employee CRUD operations with advanced filtering
    """
    queryset = Employee.objects.select_related('department', 'position', 'manager').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'position', 'status', 'employment_type', 'gender']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['employee_id', 'first_name', 'last_name', 'date_joined', 'salary']
    ordering = ['employee_id']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return EmployeeListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EmployeeCreateUpdateSerializer
        return EmployeeDetailSerializer
    
    def perform_create(self, serializer):
        """Set created_by when creating employee"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get dashboard statistics"""
        total_employees = Employee.objects.count()
        active_employees = Employee.objects.filter(status='active').count()
        on_leave = Employee.objects.filter(status='on_leave').count()
        total_departments = Department.objects.filter(is_active=True).count()
        pending_leave_requests = LeaveRequest.objects.filter(status='pending').count()
        
        # Employees by department
        employees_by_dept = dict(
            Department.objects.filter(is_active=True).annotate(
                count=Count('employees', filter=Q(employees__status='active'))
            ).values_list('name', 'count')
        )
        
        # Employees by employment type
        employees_by_type = dict(
            Employee.objects.filter(status='active').values('employment_type').annotate(
                count=Count('id')
            ).values_list('employment_type', 'count')
        )
        
        # Recent hires (last 30 days)
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        recent_hires = Employee.objects.filter(
            date_joined__gte=thirty_days_ago
        ).values('employee_id', 'first_name', 'last_name', 'date_joined')[:10]
        
        stats = {
            'total_employees': total_employees,
            'active_employees': active_employees,
            'on_leave': on_leave,
            'total_departments': total_departments,
            'pending_leave_requests': pending_leave_requests,
            'employees_by_department': employees_by_dept,
            'employees_by_employment_type': employees_by_type,
            'recent_hires': list(recent_hires),
        }
        
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def subordinates(self, request, pk=None):
        """Get all subordinates of an employee"""
        employee = self.get_object()
        subordinates = employee.subordinates.filter(status='active')
        serializer = EmployeeListSerializer(subordinates, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def terminate(self, request, pk=None):
        """Terminate an employee"""
        employee = self.get_object()
        date_left = request.data.get('date_left', timezone.now().date())
        reason = request.data.get('reason', '')
        
        employee.status = 'terminated'
        employee.date_left = date_left
        employee.notes = f"{employee.notes}\n\nTermination Date: {date_left}\nReason: {reason}"
        employee.save()
        
        serializer = self.get_serializer(employee)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export employees to Excel"""
        from openpyxl import Workbook
        from django.http import HttpResponse
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Employees"
        
        # Headers
        headers = ['Employee ID', 'First Name', 'Last Name', 'Email', 'Phone', 
                   'Department', 'Position', 'Status', 'Date Joined']
        ws.append(headers)
        
        # Data
        employees = self.filter_queryset(self.get_queryset())
        for emp in employees:
            ws.append([
                emp.employee_id,
                emp.first_name,
                emp.last_name,
                emp.email,
                emp.phone,
                emp.department.name,
                emp.position.title,
                emp.get_status_display(),
                emp.date_joined.strftime('%Y-%m-%d') if emp.date_joined else ''
            ])
        
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=employees.xlsx'
        wb.save(response)
        return response


class EmployeeDocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Employee Documents
    """
    queryset = EmployeeDocument.objects.select_related('employee', 'uploaded_by').all()
    serializer_class = EmployeeDocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['employee', 'document_type']
    search_fields = ['title', 'employee__first_name', 'employee__last_name']
    
    def perform_create(self, serializer):
        """Set uploaded_by when creating document"""
        serializer.save(uploaded_by=self.request.user)


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Attendance records
    """
    queryset = Attendance.objects.select_related('employee').all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['employee', 'date', 'status']
    ordering_fields = ['date', 'check_in', 'check_out']
    ordering = ['-date']
    
    @action(detail=False, methods=['post'])
    def bulk_mark(self, request):
        """Bulk mark attendance for multiple employees"""
        date = request.data.get('date')
        employee_ids = request.data.get('employee_ids', [])
        status_value = request.data.get('status', 'present')
        
        if not date or not employee_ids:
            return Response(
                {'error': 'Date and employee_ids are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attendance_records = []
        for emp_id in employee_ids:
            attendance, created = Attendance.objects.update_or_create(
                employee_id=emp_id,
                date=date,
                defaults={'status': status_value}
            )
            attendance_records.append(attendance)
        
        serializer = self.get_serializer(attendance_records, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LeaveRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Leave Requests
    """
    queryset = LeaveRequest.objects.select_related('employee', 'approved_by').all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['employee', 'leave_type', 'status']
    ordering_fields = ['start_date', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter leave requests based on user role"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user has employee profile, show their requests
        if hasattr(user, 'employee_profile'):
            return queryset.filter(employee=user.employee_profile)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a leave request"""
        leave_request = self.get_object()
        
        if leave_request.status != 'pending':
            return Response(
                {'error': 'Only pending requests can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leave_request.status = 'approved'
        leave_request.approved_by = request.user
        leave_request.approval_date = timezone.now()
        leave_request.save()
        
        serializer = self.get_serializer(leave_request)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a leave request"""
        leave_request = self.get_object()
        
        if leave_request.status != 'pending':
            return Response(
                {'error': 'Only pending requests can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        rejection_reason = request.data.get('rejection_reason', '')
        leave_request.status = 'rejected'
        leave_request.approved_by = request.user
        leave_request.approval_date = timezone.now()
        leave_request.rejection_reason = rejection_reason
        leave_request.save()
        
        serializer = self.get_serializer(leave_request)
        return Response(serializer.data)
