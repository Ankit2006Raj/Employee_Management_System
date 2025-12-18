from django.urls import path, include
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Employee URLs
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:pk>/edit/', views.employee_update, name='employee_update'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('employees/<int:pk>/data/', views.get_employee_data, name='get_employee_data'),
    
    # Department URLs
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_add, name='department_add'),
    path('departments/<int:pk>/edit/', views.department_update, name='department_update'),
    
    # Position URLs
    path('positions/', views.position_list, name='position_list'),
    path('positions/add/', views.position_add, name='position_add'),
    path('positions/<int:pk>/edit/', views.position_update, name='position_update'),
    
    # Leave Request URLs
    path('leave-requests/', views.leave_request_list, name='leave_request_list'),
    path('leave-requests/<int:pk>/approve/', views.leave_request_approve, name='leave_request_approve'),
    path('leave-requests/<int:pk>/reject/', views.leave_request_reject, name='leave_request_reject'),
    
    # API URLs
    path('api/', include('employee.api_urls')),
]
