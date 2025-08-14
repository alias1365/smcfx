from django.urls import path

from smcfx_admin.views.adminDashView import adminDashView
from smcfx_admin.views.adminStudentManager import ManageStudentListView, StudentCreateView, StudentUpdateView, \
    StudentDeleteView

urlpatterns = [
    path('dashboard', adminDashView.as_view(), name='admin_dashboard'),

    path("manage_student/", ManageStudentListView.as_view(), name="manage_student"),
    path("manage_student/create/", StudentCreateView.as_view(), name="student_create"),
    path("manage_student/<int:user_id>/edit/", StudentUpdateView.as_view(), name="student_edit"),
    path("manage_student/<int:user_id>/delete/", StudentDeleteView.as_view(), name="student_delete"),
]
