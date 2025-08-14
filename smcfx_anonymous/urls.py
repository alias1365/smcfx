from django.urls import path

from smcfx_anonymous.views.homeVw import home_view

urlpatterns = [
    path('', home_view.as_view(), name='home'),


]
