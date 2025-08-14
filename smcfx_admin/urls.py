from django.urls import path

from smcfx_admin.views.adminDashView import adminDashView
from smcfx_admin.views.adminStudentManager import ManageStudentListView, StudentCreateView, StudentUpdateView, \
    StudentDeleteView

urlpatterns = [
    path('dashboard', adminDashView.as_view(), name='admin_dashboard'),

    path("student/manage/", ManageStudentListView.as_view(), name="admin_student_manage"),
    path("student/create/", StudentCreateView.as_view(), name="admin_student_create"),
    path("student/<int:user_id>/edit/", StudentUpdateView.as_view(), name="admin_student_edit"),
    path("student/<int:user_id>/delete/", StudentDeleteView.as_view(), name="admin_student_delete"),
]
