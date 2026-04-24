from django.urls import path
from students import community_views
from . import views
from . import compiler_service  # NEW: Import the compiler service for Docker Execution

urlpatterns = [

    # Authentication
    path('', views.login_view, name='login'),  # Default to login page
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Student Panel Features
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('courses/', views.all_courses, name='all_courses'),
    path('courses/watch/<int:course_id>/', views.course_watch, name='course_watch'),
    path('courses/enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    
    path('live-classes/', views.live_classes, name='live_classes'),
    path('library/', views.library_view, name='library'),
    path('exams/', views.exams_view, name='exams'),
    path('profile/', views.profile_view, name='profile'),

    # API (Chatbot)
    path('api/ai-chat/', views.ai_chat, name='ai_chat'),

    # Admin Panel System
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    
    # Student Management List
    path('admin-panel/students/', views.admin_student_list, name='admin_student_list'),
    
    # Student Details & Actions
    path('admin-panel/students/<int:user_id>/', views.admin_student_detail, name='admin_student_detail'),
    path('admin-panel/students/<int:user_id>/block/', views.admin_toggle_block, name='admin_toggle_block'),
    path('admin-panel/students/<int:user_id>/delete/', views.admin_delete_student, name='admin_delete_student'),
    path('admin-panel/students/<int:user_id>/reset-pass/', views.admin_reset_password, name='admin_reset_password'),

    #  COMMUNITY CHAT & API URLS 

    path('community/<slug:slug>/', community_views.course_community_chat, name='course_community_chat'),
    path('api/chat/pin/<int:message_id>/', community_views.toggle_pin_message, name='toggle_pin_message'),
    path('api/chat/react/<int:message_id>/', community_views.add_message_reaction, name='add_message_reaction'),
    path('api/chat/user-info/<int:user_id>/', community_views.get_student_info, name='get_student_info'),
    
    # Delete & Edit Messages API
    path('api/chat/delete/<int:message_id>/', community_views.delete_message, name='delete_message'),
    path('api/chat/edit/<int:message_id>/', community_views.edit_message, name='edit_message'),
    
    # 👉 🚀 NEW: Local Docker Code Execution API
    path('api/chat/execute-local-code/', compiler_service.run_code_in_docker, name='run_code_in_docker'),
    
    # 🚀 NEW: BOUNTY ARENA API ENDPOINTS
    # Route to render the main page (404 Error Fix)
    path('bounty-arena/', views.bounty_arena_view, name='bounty_arena'),
    
    # API routing for bounty arena
    path('api/bounty/generate/', views.generate_bounty_problem, name='generate_bounty_problem'),
    path('api/bounty/submit/', views.submit_bounty_code, name='submit_bounty_code'),
]