from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home, name='home'),
    path('topics/<int:subject_id>/', views.topics, name='topics'),
    path('test/<str:test_id>/', views.test, name='test'),
    path('result/', views.result, name='result'),
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('student-performance/<int:student_id>/', views.student_performance, name='student_performance'),
]