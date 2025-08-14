from django.urls import path

from smcfx_admin.views.adminDashView import adminDashView

urlpatterns = [
    path('dashboard',adminDashView.as_view(), name='admin_dashboard'),
    

]
