from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import timedelta

from .models import Employee, Department, Position, LeaveRequest, Attendance
from .forms import EmployeeForm, EmployeeSearchForm, DepartmentForm, PositionForm, LeaveRequestForm


@login_required
def dashboard(request):
    """Dashboard with statistics and overview"""
    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(status='active').count()
    on_leave = Employee.objects.filter(status='on_leave').count()
    total_departments = Department.objects.filter(is_active=True).count()
    pending_leave_requests = LeaveRequest.objects.filter(status='pending').count()
    
    # Employees by department
    employees_by_dept = Department.objects.filter(is_active=True).annotate(
        count=Count('employees', filter=Q(employees__status='active'))
    ).values('name', 'count')[:5]
    
    # Recent hires (last 30 days)
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    recent_hires = Employee.objects.filter(
        date_joined__gte=thirty_days_ago
    ).select_related('department', 'position')[:5]
    
    # Pending leave requests
    pending_leaves = LeaveRequest.objects.filter(
        status='pending'
    ).select_related('employee')[:5]
    
    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'on_leave': on_leave,
        'total_departments': total_departments,
        'pending_leave_requests': pending_leave_requests,
        'employees_by_dept': employees_by_dept,
        'recent_hires': recent_hires,
        'pending_leaves': pending_leaves,
    }
    
    return render(request, 'employee/dashboard.html', context)


@login_required
def employee_list(request):
    """Display all employees with search and filter"""
    form = EmployeeSearchForm(request.GET)
    employees = Employee.objects.select_related('department', 'position', 'manager').all()
    
    # Apply filters
    if form.is_valid():
        search = form.cleaned_data.get('search')
        if search:
            employees = employees.filter(
                Q(employee_id__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        department = form.cleaned_data.get('department')
        if department:
            employees = employees.filter(department=department)
        
        position = form.cleaned_data.get('position')
        if position:
            employees = employees.filter(position=position)
        
        status = form.cleaned_data.get('status')
        if status:
            employees = employees.filter(status=status)
        
        employment_type = form.cleaned_data.get('employment_type')
        if employment_type:
            employees = employees.filter(employment_type=employment_type)
    
    # Pagination
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'employees': page_obj.object_list,
    }
    
    return render(request, 'employee/employee_list.html', context)


@login_required
def employee_detail(request, pk):
    """Display detailed employee information"""
    employee = get_object_or_404(
        Employee.objects.select_related('department', 'position', 'manager'),
        pk=pk
    )
    
    # Get subordinates
    subordinates = employee.subordinates.filter(status='active')
    
    # Get recent attendance
    recent_attendance = employee.attendance_records.all()[:10]
    
    # Get leave requests
    leave_requests = employee.leave_requests.all()[:10]
    
    context = {
        'employee': employee,
        'subordinates': subordinates,
        'recent_attendance': recent_attendance,
        'leave_requests': leave_requests,
    }
    
    return render(request, 'employee/employee_detail.html', context)


@login_required
def employee_add(request):
    """Add a new employee"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.created_by = request.user
            employee.save()
            messages.success(request, f'Employee {employee.full_name} added successfully!')
            return redirect('employee_detail', pk=employee.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeForm()
    
    return render(request, 'employee/employee_form.html', {
        'form': form,
        'title': 'Add New Employee',
        'button_text': 'Add Employee'
    })


@login_required
def employee_update(request, pk):
    """Update an existing employee"""
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f'Employee {employee.full_name} updated successfully!')
            return redirect('employee_detail', pk=employee.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'employee/employee_form.html', {
        'form': form,
        'employee': employee,
        'title': f'Edit Employee: {employee.full_name}',
        'button_text': 'Update Employee'
    })


@login_required
def employee_delete(request, pk):
    """Delete an employee"""
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        employee_name = employee.full_name
        employee.delete()
        messages.success(request, f'Employee {employee_name} deleted successfully!')
        return redirect('employee_list')
    
    return render(request, 'employee/employee_delete.html', {'employee': employee})


# Department Views
@login_required
def department_list(request):
    """List all departments"""
    departments = Department.objects.annotate(
        employee_count=Count('employees', filter=Q(employees__status='active'))
    ).all()
    
    return render(request, 'employee/department_list.html', {'departments': departments})


@login_required
def department_add(request):
    """Add a new department"""
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            messages.success(request, f'Department {department.name} added successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    
    return render(request, 'employee/department_form.html', {
        'form': form,
        'title': 'Add New Department',
        'button_text': 'Add Department'
    })


@login_required
def department_update(request, pk):
    """Update a department"""
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, f'Department {department.name} updated successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'employee/department_form.html', {
        'form': form,
        'department': department,
        'title': f'Edit Department: {department.name}',
        'button_text': 'Update Department'
    })


# Position Views
@login_required
def position_list(request):
    """List all positions"""
    positions = Position.objects.annotate(
        employee_count=Count('employees', filter=Q(employees__status='active'))
    ).all()
    
    return render(request, 'employee/position_list.html', {'positions': positions})


@login_required
def position_add(request):
    """Add a new position"""
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            position = form.save()
            messages.success(request, f'Position {position.title} added successfully!')
            return redirect('position_list')
    else:
        form = PositionForm()
    
    return render(request, 'employee/position_form.html', {
        'form': form,
        'title': 'Add New Position',
        'button_text': 'Add Position'
    })


@login_required
def position_update(request, pk):
    """Update a position"""
    position = get_object_or_404(Position, pk=pk)
    
    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            messages.success(request, f'Position {position.title} updated successfully!')
            return redirect('position_list')
    else:
        form = PositionForm(instance=position)
    
    return render(request, 'employee/position_form.html', {
        'form': form,
        'position': position,
        'title': f'Edit Position: {position.title}',
        'button_text': 'Update Position'
    })


# Leave Request Views
@login_required
def leave_request_list(request):
    """List all leave requests"""
    leave_requests = LeaveRequest.objects.select_related('employee', 'approved_by').all()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        leave_requests = leave_requests.filter(status=status_filter)
    
    paginator = Paginator(leave_requests, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'employee/leave_request_list.html', {
        'page_obj': page_obj,
        'leave_requests': page_obj.object_list,
    })


@login_required
@require_http_methods(["POST"])
def leave_request_approve(request, pk):
    """Approve a leave request"""
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    
    if leave_request.status == 'pending':
        leave_request.status = 'approved'
        leave_request.approved_by = request.user
        leave_request.approval_date = timezone.now()
        leave_request.save()
        messages.success(request, 'Leave request approved successfully!')
    else:
        messages.error(request, 'Only pending requests can be approved.')
    
    return redirect('leave_request_list')


@login_required
@require_http_methods(["POST"])
def leave_request_reject(request, pk):
    """Reject a leave request"""
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    
    if leave_request.status == 'pending':
        leave_request.status = 'rejected'
        leave_request.approved_by = request.user
        leave_request.approval_date = timezone.now()
        leave_request.rejection_reason = request.POST.get('rejection_reason', '')
        leave_request.save()
        messages.success(request, 'Leave request rejected.')
    else:
        messages.error(request, 'Only pending requests can be rejected.')
    
    return redirect('leave_request_list')


# AJAX Views
@login_required
def get_employee_data(request, pk):
    """Get employee data as JSON"""
    employee = get_object_or_404(Employee, pk=pk)
    data = {
        'id': employee.id,
        'employee_id': employee.employee_id,
        'full_name': employee.full_name,
        'email': employee.email,
        'phone': employee.phone,
        'department': employee.department.name,
        'position': employee.position.title,
        'status': employee.get_status_display(),
    }
    return JsonResponse(data)
