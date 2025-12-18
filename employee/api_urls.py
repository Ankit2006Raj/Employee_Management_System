from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    EmployeeViewSet, DepartmentViewSet, PositionViewSet,
    EmployeeDocumentViewSet, AttendanceViewSet, LeaveRequestViewSet
)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'positions', PositionViewSet, basename='position')
router.register(r'documents', EmployeeDocumentViewSet, basename='document')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'leave-requests', LeaveRequestViewSet, basename='leave-request')

urlpatterns = [
    path('', include(router.urls)),
]
