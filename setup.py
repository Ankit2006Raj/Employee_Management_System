#!/usr/bin/env python
"""
Setup script for Employee Management System
Run this after initial installation to set up the database and create sample data
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.settings')
django.setup()

from django.contrib.auth.models import User, Group
from employee.models import Department, Position, Employee
from django.utils import timezone
from datetime import timedelta


def create_groups():
    """Create user groups"""
    print("Creating user groups...")
    hr_group, created = Group.objects.get_or_create(name='HR')
    manager_group, created = Group.objects.get_or_create(name='Manager')
    employee_group, created = Group.objects.get_or_create(name='Employee')
    print("✓ Groups created")


def create_departments():
    """Create sample departments"""
    print("\nCreating departments...")
    departments = [
        {'name': 'Engineering', 'code': 'ENG', 'description': 'Software Development and Engineering'},
        {'name': 'Human Resources', 'code': 'HR', 'description': 'Human Resources and Talent Management'},
        {'name': 'Sales', 'code': 'SALES', 'description': 'Sales and Business Development'},
        {'name': 'Marketing', 'code': 'MKT', 'description': 'Marketing and Communications'},
        {'name': 'Finance', 'code': 'FIN', 'description': 'Finance and Accounting'},
        {'name': 'Operations', 'code': 'OPS', 'description': 'Operations and Logistics'},
    ]
    
    for dept_data in departments:
        dept, created = Department.objects.get_or_create(
            code=dept_data['code'],
            defaults=dept_data
        )
        if created:
            print(f"  ✓ Created department: {dept.name}")
    
    print("✓ Departments created")


def create_positions():
    """Create sample positions"""
    print("\nCreating positions...")
    positions = [
        {'title': 'Software Engineer', 'min_salary': 60000, 'max_salary': 120000, 
         'description': 'Develops and maintains software applications'},
        {'title': 'Senior Software Engineer', 'min_salary': 90000, 'max_salary': 150000,
         'description': 'Senior level software development role'},
        {'title': 'Engineering Manager', 'min_salary': 110000, 'max_salary': 180000,
         'description': 'Manages engineering team and projects'},
        {'title': 'HR Manager', 'min_salary': 70000, 'max_salary': 110000,
         'description': 'Manages HR operations and team'},
        {'title': 'HR Specialist', 'min_salary': 50000, 'max_salary': 80000,
         'description': 'Handles recruitment and employee relations'},
        {'title': 'Sales Representative', 'min_salary': 40000, 'max_salary': 80000,
         'description': 'Sells products and services to customers'},
        {'title': 'Sales Manager', 'min_salary': 70000, 'max_salary': 120000,
         'description': 'Manages sales team and strategy'},
        {'title': 'Marketing Manager', 'min_salary': 70000, 'max_salary': 120000,
         'description': 'Manages marketing campaigns and team'},
        {'title': 'Financial Analyst', 'min_salary': 60000, 'max_salary': 100000,
         'description': 'Analyzes financial data and reports'},
        {'title': 'Operations Manager', 'min_salary': 70000, 'max_salary': 110000,
         'description': 'Manages daily operations'},
    ]
    
    for pos_data in positions:
        pos, created = Position.objects.get_or_create(
            title=pos_data['title'],
            defaults=pos_data
        )
        if created:
            print(f"  ✓ Created position: {pos.title}")
    
    print("✓ Positions created")


def create_sample_employees():
    """Create sample employees"""
    print("\nCreating sample employees...")
    
    # Get departments and positions
    eng_dept = Department.objects.get(code='ENG')
    hr_dept = Department.objects.get(code='HR')
    sales_dept = Department.objects.get(code='SALES')
    
    eng_manager_pos = Position.objects.get(title='Engineering Manager')
    senior_eng_pos = Position.objects.get(title='Senior Software Engineer')
    eng_pos = Position.objects.get(title='Software Engineer')
    hr_manager_pos = Position.objects.get(title='HR Manager')
    sales_rep_pos = Position.objects.get(title='Sales Representative')
    
    # Create sample employees
    employees = [
        {
            'employee_id': 'EMP001',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@company.com',
            'phone': '+1234567890',
            'department': eng_dept,
            'position': eng_manager_pos,
            'employment_type': 'FT',
            'status': 'active',
            'salary': 120000,
            'date_joined': timezone.now().date() - timedelta(days=730),
        },
        {
            'employee_id': 'EMP002',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@company.com',
            'phone': '+1234567891',
            'department': eng_dept,
            'position': senior_eng_pos,
            'employment_type': 'FT',
            'status': 'active',
            'salary': 95000,
            'date_joined': timezone.now().date() - timedelta(days=500),
        },
        {
            'employee_id': 'EMP003',
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'email': 'bob.johnson@company.com',
            'phone': '+1234567892',
            'department': hr_dept,
            'position': hr_manager_pos,
            'employment_type': 'FT',
            'status': 'active',
            'salary': 85000,
            'date_joined': timezone.now().date() - timedelta(days=600),
        },
        {
            'employee_id': 'EMP004',
            'first_name': 'Alice',
            'last_name': 'Williams',
            'email': 'alice.williams@company.com',
            'phone': '+1234567893',
            'department': sales_dept,
            'position': sales_rep_pos,
            'employment_type': 'FT',
            'status': 'active',
            'salary': 55000,
            'date_joined': timezone.now().date() - timedelta(days=200),
        },
        {
            'employee_id': 'EMP005',
            'first_name': 'Charlie',
            'last_name': 'Brown',
            'email': 'charlie.brown@company.com',
            'phone': '+1234567894',
            'department': eng_dept,
            'position': eng_pos,
            'employment_type': 'FT',
            'status': 'active',
            'salary': 70000,
            'date_joined': timezone.now().date() - timedelta(days=100),
        },
    ]
    
    for emp_data in employees:
        emp, created = Employee.objects.get_or_create(
            employee_id=emp_data['employee_id'],
            defaults=emp_data
        )
        if created:
            print(f"  ✓ Created employee: {emp.full_name}")
    
    # Set manager relationships
    john = Employee.objects.get(employee_id='EMP001')
    jane = Employee.objects.get(employee_id='EMP002')
    charlie = Employee.objects.get(employee_id='EMP005')
    
    jane.manager = john
    jane.save()
    charlie.manager = john
    charlie.save()
    
    print("✓ Sample employees created")


def main():
    """Main setup function"""
    print("=" * 60)
    print("Employee Management System - Setup")
    print("=" * 60)
    
    try:
        create_groups()
        create_departments()
        create_positions()
        
        # Ask if user wants sample data
        response = input("\nDo you want to create sample employees? (y/n): ")
        if response.lower() == 'y':
            create_sample_employees()
        
        print("\n" + "=" * 60)
        print("✓ Setup completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Create a superuser: python manage.py createsuperuser")
        print("2. Run the server: python manage.py runserver")
        print("3. Access the application at: http://localhost:8000")
        print("4. Access the admin panel at: http://localhost:8000/admin")
        print("\n")
        
    except Exception as e:
        print(f"\n✗ Error during setup: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
