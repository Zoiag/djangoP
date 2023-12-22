"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

import view
from test_django import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', view.test_link),
    path('info/', views.show_info, name='info'),
    path('info/<int:teacher_id>/schools', views.schools_info, name='schools_info'),
    path('info/<int:teacher_id>/addsub', views.create_subject, name='create_subject'),
    path('info/<int:teacher_id>/schools/create', views.create_school, name='create_school'),
    path('sign/', views.show_sign),
    path('', views.show_sign, name='sign'),
    path('showstudent/<int:id_user>/', views.show_student),
    path('showstudent/<int:id_user>/edit', views.edit_profile, name='edit_profile'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('sign')), name='logout'),
    path('info/<int:subject_id>/delete', views.delete_subject, name='delete_subject'),
    path('ajax/validate_mark', views.validate_mark, name='validate_mark'),
    path('ajax/validate_name_mail', views.validate_name_mail, name='validate_name_mail'),
]