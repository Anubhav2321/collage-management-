from django.urls import path
from . import views

urlpatterns = [
    # ==========================
    # Authentication
    # ==========================
    path('', views.login_view, name='login'),  # Default to login page
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # ==========================
    # Student Panel Features
    # ==========================
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('courses/', views.all_courses, name='all_courses'),
    path('courses/watch/<int:course_id>/', views.course_watch, name='course_watch'),
    path('courses/enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    
    path('live-classes/', views.live_classes, name='live_classes'),
    path('library/', views.library_view, name='library'),
    path('exams/', views.exams_view, name='exams'),
    path('profile/', views.profile_view, name='profile'),

    # ==========================
    # API (Chatbot)
    # ==========================
    path('api/ai-chat/', views.ai_chat, name='ai_chat'),

    # ==========================
    # Admin Panel System (New)
    # ==========================
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    
    # Student Management List
    path('admin-panel/students/', views.admin_student_list, name='admin_student_list'),
    
    # Student Details & Actions
    path('admin-panel/students/<int:user_id>/', views.admin_student_detail, name='admin_student_detail'),
    path('admin-panel/students/<int:user_id>/block/', views.admin_toggle_block, name='admin_toggle_block'),
    path('admin-panel/students/<int:user_id>/delete/', views.admin_delete_student, name='admin_delete_student'),
    path('admin-panel/students/<int:user_id>/reset-pass/', views.admin_reset_password, name='admin_reset_password'),
]