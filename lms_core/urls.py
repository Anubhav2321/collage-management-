from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Importing all views from students app
from students.views import (
    # 1. Public
    home_view, 
    contact_developers_view,

    # 2. Auth
    register_view, 
    login_view, 
    logout_view,

    # 3. Student Features
    student_dashboard, 
    all_courses, 
    enroll_course, 
    course_watch,       
    live_classes, 
    library_view, 
    profile_view,       # <--- Profile View

    # 4. Payment System
    payment_page,
    process_payment,

    # 5. Quiz & AI
    student_exam_list,  # <--- Exam List View
    take_exam,          # <--- Take Exam View
    generate_quiz_view, 
    save_quiz_view, 
    submit_quiz_view,   
    ai_chat,

    # 6. Admin Panel (Dashboard)
    admin_dashboard, 
    
    # 7. Admin Management (Lists & Edits)
    admin_student_list, 
    admin_student_detail,
    admin_update_student_info,
    admin_toggle_block, 
    admin_delete_student, 
    admin_reset_password,

    admin_course_list,          
    admin_edit_course,          
    admin_delete_course,        

    admin_document_list,        
    admin_edit_document,        
    admin_delete_document,      

    admin_enrollment_list,      
    admin_delete_enrollment,    
    
    # 8. Admin Actions (Create Forms)
    admin_create_course,
    admin_create_notice,
    admin_create_live_class,
    admin_create_exam,
    add_library_view,
    admin_add_lesson # <--- Lesson View
)

urlpatterns = [

    # 1. Django Default Admin

    path('admin/', admin.site.urls),

    # 2. Public Pages

    path('', home_view, name='home'),
    path('contact/', contact_developers_view, name='contact_developers'),

    # 3. Authentication

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # 4. Student Dashboard & Features

    path('dashboard/', student_dashboard, name='dashboard'),
    path('profile/', profile_view, name='profile'), 

    # Courses
    path('courses/', all_courses, name='all_courses'),
    path('courses/enroll/<int:course_id>/', enroll_course, name='enroll_course'),
    
    # Payment Flow
    path('courses/payment/<int:course_id>/', payment_page, name='payment_page'),
    path('courses/payment/<int:course_id>/process/', process_payment, name='process_payment'),

    # Watch Course (FIXED HERE: Both names are now 'course_watch')
    path('courses/watch/<int:course_id>/', course_watch, name='course_watch'),
    path('courses/watch/<int:course_id>/<int:lesson_id>/', course_watch, name='course_watch'),

    # Core Features
    path('live-classes/', live_classes, name='live_classes'),
    path('library/', library_view, name='library'),
    
    # 5. Quiz & AI System
    
    # New Exam Logic (Course Linked)
    path('my-exams/', student_exam_list, name='student_exam_list'), 
    path('take-exam/<int:exam_id>/', take_exam, name='take_exam'), 
    
    # AI Quiz Generation
    path('quiz/generate/', generate_quiz_view, name='generate_quiz'),
    path('quiz/save/', save_quiz_view, name='save_quiz'),
    path('quiz/submit/<int:exam_id>/', submit_quiz_view, name='submit_quiz'), 
    
    # AI Chatbot Endpoint
    path('api/ai-chat/', ai_chat, name='ai_chat'),

    # 6. Admin Panel System
   
    path('admin-panel/', admin_dashboard, name='admin_dashboard'),
    
    # --- A. Student Management ---
    path('admin-panel/students/', admin_student_list, name='admin_student_list'),
    path('admin-panel/students/<int:user_id>/', admin_student_detail, name='admin_student_detail'),
    path('admin-panel/students/<int:user_id>/update/', admin_update_student_info, name='admin_update_student_info'),
    path('admin-panel/students/<int:user_id>/block/', admin_toggle_block, name='admin_toggle_block'),
    path('admin-panel/students/<int:user_id>/delete/', admin_delete_student, name='admin_delete_student'),
    path('admin-panel/students/<int:user_id>/reset-pass/', admin_reset_password, name='admin_reset_password'),

    # --- B. Course Management (List & Edit) ---
    path('admin-panel/courses/', admin_course_list, name='admin_course_list'),
    path('admin-panel/courses/edit/<int:course_id>/', admin_edit_course, name='admin_edit_course'),
    path('admin-panel/course/delete/<int:course_id>/', admin_delete_course, name='admin_delete_course'),

    # --- C. Library Management (List & Edit) ---
    path('admin-panel/documents/', admin_document_list, name='admin_document_list'),
    path('admin-panel/documents/edit/<int:doc_id>/', admin_edit_document, name='admin_edit_document'),
    path('admin-panel/documents/delete/<int:doc_id>/', admin_delete_document, name='admin_delete_document'),

    # --- D. Enrollment Management ---
    path('admin-panel/enrollments/', admin_enrollment_list, name='admin_enrollment_list'),
    path('admin-panel/enrollments/delete/<int:enroll_id>/', admin_delete_enrollment, name='admin_delete_enrollment'),

    # --- E. Content Creation (Forms) ---
    path('admin-panel/create-course/', admin_create_course, name='admin_create_course'),
    path('admin-panel/create-notice/', admin_create_notice, name='admin_create_notice'),
    path('admin-panel/create-class/', admin_create_live_class, name='admin_create_live_class'),
    path('admin-panel/create-exam/', admin_create_exam, name='admin_create_exam'),
    path('admin-panel/library/add/', add_library_view, name='add_library'),
    
    # --- F. Lesson Management ---
    path('admin-panel/course/<int:course_id>/add-lesson/', admin_add_lesson, name='admin_add_lesson'),
]

# Media & Static Files Configuration

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    else:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)