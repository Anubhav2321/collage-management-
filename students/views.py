import json
import datetime
import random
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Avg
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.paginator import Paginator

# Import AI Logic (From the new ai_utils.py file)
from .ai_utils import extract_text_from_file, generate_quiz_from_text

# Import Forms (Including the new ProfilePictureForm)
from .forms import (
    StudentRegistrationForm,
    CourseForm,
    NotificationForm,
    LibraryDocumentForm,
    LiveClassForm,
    ExamForm,
    ProfilePictureForm 
)

# Import Models
from .models import (
    Course,
    Enrollment,
    Notification,
    LiveClass,
    LibraryDocument,
    Exam,
    Profile,
    Lesson,
    Quiz,
    Question,
    QuizResult
)

User = get_user_model()

# ====================================================
# 1. PUBLIC VIEWS (LANDING, CONTACT)
# ====================================================

def home_view(request):
    """
    Renders the Landing Page with stats.
    """
    featured_courses = Course.objects.filter(is_published=True).order_by('-created_at')[:3]
    total_students = User.objects.filter(is_student=True).count()
    total_courses_count = Course.objects.count()
    
    context = {
        'featured_courses': featured_courses,
        'total_students': total_students,
        'total_courses_count': total_courses_count,
        'year': timezone.now().year
    }
    return render(request, 'landing.html', context)


def contact_developers_view(request):
    """
    Renders Contact Page & Handles Form Submission.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Here you would integrate SendGrid or SMTP logic
        messages.success(request, f"Thank you {name}, we have received your message and will reply to {email} shortly.")
        return redirect('contact_developers')
        
    return render(request, 'contact.html')


# ====================================================
# 2. AUTHENTICATION (REGISTER, LOGIN, LOGOUT)
# ====================================================

def register_view(request):
    """
    Handles Student Registration.
    """
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}! Please login to continue.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """
    Handles User Login (Supports Username or Email).
    """
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('dashboard')

    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')

        # Try authenticating as Username first
        user = authenticate(request, username=identifier, password=password)
        
        # If failed, try finding user by Email
        if user is None:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid Credentials! Please check your username/email and password.")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


# ====================================================
# 3. STUDENT DASHBOARD & PROFILE FEATURES
# ====================================================

@login_required
def student_dashboard(request):
    """
    Main Student Dashboard.
    """
    user = request.user
    
    # Fetch Enrollments
    enrollments = Enrollment.objects.filter(student=user).select_related('course').order_by('-last_accessed')
    
    # Fetch Notifications
    notifications = Notification.objects.all().order_by('-created_at')[:5]
    
    # Calculate Stats
    total_enrolled = enrollments.count()
    completed_courses = enrollments.filter(progress=100).count()
    certificate_eligible = completed_courses
    
    context = {
        'enrollments': enrollments,
        'notifications': notifications,
        'total_enrolled': total_enrolled,
        'completed_courses': completed_courses,
        'certificate_eligible': certificate_eligible,
        'user': user
    }
    return render(request, 'student_dashboard.html', context)


@login_required
def profile_view(request):
    """
    Student Profile View (Updated).
    Features: Profile Picture Upload, View Enrolled Courses, Removed Phone.
    """
    user = request.user
    
    # Ensure profile object exists
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    
    # Handle Profile Picture Upload
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile picture updated successfully!")
            return redirect('profile')
    else:
        form = ProfilePictureForm(instance=user.profile)

    # Fetch Enrolled Courses for display
    enrollments = Enrollment.objects.filter(student=user).select_related('course').order_by('-enrolled_at')

    context = {
        'user': user,
        'form': form,
        'enrollments': enrollments,
    }
    return render(request, 'student_profile.html', context)


# ====================================================
# 4. COURSE & LEARNING LOGIC
# ====================================================

@login_required
def all_courses(request):
    """
    Course Catalog with Search and Pagination.
    """
    query = request.GET.get('search')
    courses_list = Course.objects.filter(is_published=True).order_by('-created_at')
    
    if query:
        courses_list = courses_list.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(difficulty_level__icontains=query)
        )
        messages.info(request, f"Found {courses_list.count()} results for '{query}'")

    paginator = Paginator(courses_list, 6) 
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)

    context = {
        'courses': courses,
        'search_query': query
    }
    return render(request, 'student_courses.html', context)


@login_required
def enroll_course(request, course_id):
    """
    Handles Course Enrollment logic.
    """
    course = get_object_or_404(Course, id=course_id)
    student = request.user
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=student, course=course).exists():
        messages.info(request, "You are already enrolled!")
        return redirect('dashboard')

    # Payment Check
    if course.price > 0:
        return redirect('payment_page', course_id=course.id)
    
    # Free Course Enrollment
    Enrollment.objects.create(student=student, course=course)
    messages.success(request, f"Successfully enrolled in {course.title}!")
    return redirect('dashboard')


@login_required
def payment_page(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'payment.html', {'course': course})


@login_required
def process_payment(request, course_id):
    if request.method == "POST":
        course = get_object_or_404(Course, id=course_id)
        
        # Create Enrollment after successful payment
        Enrollment.objects.get_or_create(student=request.user, course=course)
        
        messages.success(request, f"Payment Successful! Welcome to {course.title}.")
        return redirect('dashboard')
        
    return redirect('all_courses')


@login_required
def course_watch(request, course_id, lesson_id=None):
    """
    Course Player / Video Watcher logic with Progress Tracking.
    """
    course = get_object_or_404(Course, id=course_id)
    
    # Security Check
    try:
        enrollment = Enrollment.objects.get(student=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.warning(request, "You must enroll in this course to access the content.")
        return redirect('all_courses')

    # Update Last Accessed Time
    enrollment.last_accessed = timezone.now()
    enrollment.save()

    lessons = course.lessons.all().order_by('order')
    
    current_lesson = None
    next_lesson = None
    prev_lesson = None

    if lessons.exists():
        if lesson_id:
            current_lesson = get_object_or_404(Lesson, id=lesson_id)
        else:
            current_lesson = lessons.first()
            
        # Logic for Next/Prev buttons
        lesson_list = list(lessons)
        try:
            idx = lesson_list.index(current_lesson)
            if idx > 0:
                prev_lesson = lesson_list[idx - 1]
            if idx < len(lesson_list) - 1:
                next_lesson = lesson_list[idx + 1]
            
            # Progress Calculation
            new_progress = ((idx + 1) / len(lesson_list)) * 100
            if new_progress > enrollment.progress:
                enrollment.update_progress(new_progress)

        except ValueError:
            pass

    context = {
        'course': course,
        'lessons': lessons,
        'current_lesson': current_lesson,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson,
        'progress': enrollment.progress
    }
    return render(request, 'course_watch.html', context)


@login_required
def live_classes(request):
    now = timezone.now()
    classes = LiveClass.objects.filter(date_time__gte=now - datetime.timedelta(hours=1)).order_by('date_time')
    return render(request, 'student_classes.html', {'classes': classes})


@login_required
def library_view(request):
    documents = LibraryDocument.objects.all().order_by('-uploaded_at')
    
    query = request.GET.get('search')
    if query:
        documents = documents.filter(title__icontains=query)

    return render(request, 'student_library.html', {'documents': documents})


# ====================================================
# 5. QUIZ & EXAMS (AI GENERATION + LOGIC)
# ====================================================

@login_required
def exams_view(request):
    """
    Exams List with Tabs Logic (Active vs History).
    """
    # 1. Fetch all active exams
    all_active_exams = Exam.objects.filter(is_active=True).order_by('-created_at')
    
    # 2. Fetch History (Results for this student)
    attempted_results = QuizResult.objects.filter(student=request.user).select_related('exam').order_by('-taken_at')
    
    # 3. Get IDs of exams already attempted
    attempted_exam_ids = attempted_results.values_list('exam_id', flat=True)
    
    # 4. Filter Available Exams (Active - Attempted)
    available_exams = all_active_exams.exclude(id__in=attempted_exam_ids)

    context = {
        'available_exams': available_exams,   # Tab 1: Active
        'attempted_results': attempted_results, # Tab 2: History
        'total_attempted': attempted_results.count(),
        'total_pending': available_exams.count()
    }
    return render(request, 'student_exams.html', context)


@login_required
def generate_quiz_view(request):
    """
    AI Quiz Generator (Real Logic).
    Reads the selected Library Document and generates questions from it.
    """
    if request.method == "POST":
        try:
            # 1. Capture doc_id
            doc_id = request.POST.get('doc_id')
            if not doc_id:
                return JsonResponse({'status': 'error', 'message': 'No document selected!'}, status=400)

            # 2. Find document
            document = get_object_or_404(LibraryDocument, id=doc_id)
            if not document.file:
                return JsonResponse({'status': 'error', 'message': 'File not found on server.'}, status=404)

            # 3. Extract text
            file_path = document.file.path
            extracted_text = extract_text_from_file(file_path)
            
            if len(extracted_text) < 50:
                return JsonResponse({'status': 'error', 'message': 'File is empty or unreadable.'}, status=400)

            # 4. Generate 10-15 Questions
            generated_questions = generate_quiz_from_text(extracted_text, num_questions=15)
            
            time.sleep(1) # Simulation delay
            
            return JsonResponse({'status': 'success', 'quiz': generated_questions})

        except Exception as e:
            print(f"Error generating quiz: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid Request'}, status=400)


@login_required
def save_quiz_view(request):
    """
    Saves the AI Generated Quiz to the Database.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get('title', 'AI Generated Quiz')
            questions = data.get('questions', [])
            
            # 1. Create Exam Object
            exam = Exam.objects.create(
                title=title,
                description="Generated by AI Assistant",
                duration_minutes=20, 
                is_active=True,
                total_marks=len(questions) # Set total marks based on question count
            )
            
            # 2. Create Questions
            for q in questions:
                opts = q.get('options', [])
                correct_idx = q.get('answer', 0)
                
                Question.objects.create(
                    exam=exam,
                    question_text=q.get('question'),
                    option1=opts[0] if len(opts) > 0 else "-",
                    option2=opts[1] if len(opts) > 1 else "-",
                    option3=opts[2] if len(opts) > 2 else "-",
                    option4=opts[3] if len(opts) > 3 else "-",
                    correct_option=opts[correct_idx] 
                )
                
            return JsonResponse({'status': 'success', 'message': 'Quiz Saved Successfully!'})
            
        except Exception as e:
            print(f"Error saving quiz: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def take_quiz_view(request, exam_id):
    """
    Renders the Quiz Taking Interface.
    """
    exam = get_object_or_404(Exam, id=exam_id)
    return render(request, 'take_quiz.html', {'exam': exam})


@login_required
def submit_quiz_view(request, exam_id):
    """
    Handles Quiz Submission, Grading, and Result Storage.
    """
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == "POST":
        score = 0
        total_questions = exam.questions.count()
        user_answers = {}
        
        for question in exam.questions.all():
            selected_option = request.POST.get(f'q_{question.id}')
            
            if selected_option == question.correct_option:
                score += 1
            
            user_answers[question.id] = {
                'question': question.question_text,
                'selected': selected_option,
                'correct': question.correct_option,
                'is_correct': (selected_option == question.correct_option)
            }

        # Save Result
        try:
            QuizResult.objects.create(
                student=request.user,
                exam=exam,
                score=score,
                total_marks=total_questions
            )
        except TypeError:
             # Fallback if total_marks is removed from model
             QuizResult.objects.create(
                student=request.user,
                exam=exam,
                score=score
            )
        
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        context = {
            'exam': exam,
            'score': score,
            'total': total_questions,
            'percentage': round(percentage, 2),
            'user_answers': user_answers
        }
        return render(request, 'quiz_result.html', context)
        
    return redirect('dashboard')


@csrf_exempt
def ai_chat(request):
    """
    AI Chatbot Logic.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('question', '').lower()
            
            response_text = "I'm not sure about that."

            if 'hello' in user_message:
                response_text = "Hello! How can I help you with your studies today?"
            elif 'course' in user_message:
                response_text = "You can browse courses in the Course Catalog section."
            elif 'python' in user_message:
                response_text = "Python is a great language! We have courses on it."
            elif 'exam' in user_message:
                response_text = "Check the Exams tab for upcoming schedules."
            elif 'library' in user_message:
                response_text = "You can download notes from the Digital Library."
            else:
                response_text = "I am an AI assistant for this LMS. Ask me about courses or exams!"

            return JsonResponse({'answer': response_text})
        except Exception:
            return JsonResponse({'answer': "Error processing request."}, status=500)
    return JsonResponse({'error': "Invalid request"}, status=400)


# ====================================================
# 6. ADMIN PANEL SYSTEM (FULL CREATE/DELETE LOGIC)
# ====================================================

@staff_member_required
def admin_dashboard(request):
    """
    Admin Dashboard Logic.
    """
    total_students = User.objects.filter(is_student=True).count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.count()
    total_docs = LibraryDocument.objects.count()

    courses = Course.objects.all().order_by('-created_at')
    documents = LibraryDocument.objects.all().order_by('-uploaded_at')
    
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'total_docs': total_docs,
        'courses': courses,
        'documents': documents,
        'course_form': CourseForm(),
        'notice_form': NotificationForm(),
        'class_form': LiveClassForm(),
        'exam_form': ExamForm(),
        'library_form': LibraryDocumentForm()
    }
    return render(request, 'custom_admin/dashboard.html', context)

# --- Admin Action Views (Create) ---

@staff_member_required
def admin_create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            messages.success(request, f"Course '{course.title}' created successfully!")
        else:
            messages.error(request, "Error creating course. Please check inputs.")
    return redirect('admin_dashboard')

@staff_member_required
def admin_create_notice(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Notification posted to all students.")
        else:
            messages.error(request, "Failed to post notice.")
    return redirect('admin_dashboard')

@staff_member_required
def admin_create_live_class(request):
    if request.method == 'POST':
        form = LiveClassForm(request.POST)
        if form.is_valid():
            live_class = form.save()
            messages.success(request, f"Live class '{live_class.title}' scheduled.")
        else:
            messages.error(request, "Invalid class details. Date cannot be in past.")
    return redirect('admin_dashboard')

@staff_member_required
def admin_create_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
            messages.success(request, f"Exam '{exam.title}' created.")
        else:
            messages.error(request, "Failed to create exam.")
    return redirect('admin_dashboard')

@staff_member_required
def add_library_view(request):
    if request.method == 'POST':
        form = LibraryDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.save()
            messages.success(request, f"Document '{doc.title}' uploaded to library.")
        else:
            messages.error(request, "Upload failed. Check file type (PDF/Doc only).")
    return redirect('admin_dashboard')

# --- Admin Student Management Views ---

@staff_member_required
def admin_student_list(request):
    query = request.GET.get('search', '')
    if query:
        students = User.objects.filter(is_student=True).filter(
            Q(first_name__icontains=query) | Q(email__icontains=query) | Q(username__icontains=query)
        )
    else:
        students = User.objects.filter(is_student=True).order_by('-date_joined')

    return render(request, 'custom_admin/student_list.html', {'students': students, 'search_query': query})

@staff_member_required
def admin_student_detail(request, user_id):
    student = get_object_or_404(User, id=user_id)
    enrollments = Enrollment.objects.filter(student=student).order_by('-enrolled_at')
    completed_courses = enrollments.filter(progress=100).count()
    quiz_results = QuizResult.objects.filter(student=student).order_by('-taken_at')
    avg_score = quiz_results.aggregate(Avg('score'))['score__avg']
    avg_score = round(avg_score, 1) if avg_score else 0
    
    context = {
        'student': student,
        'enrollments': enrollments,
        'completed_courses': completed_courses,
        'quiz_results': quiz_results,
        'avg_score': avg_score,
        'total_quizzes': quiz_results.count()
    }
    return render(request, 'custom_admin/student_detail.html', context)

@staff_member_required
def admin_update_student_info(request, user_id):
    student = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.email = request.POST.get('email')
        student.stream = request.POST.get('stream')
        student.student_level = request.POST.get('student_level')
        student.save()
        
        phone = request.POST.get('phone')
        if phone:
            student.profile.phone = phone
            student.profile.save()
            
        messages.success(request, "Student information updated successfully.")
    return redirect('admin_student_detail', user_id=user_id)

@staff_member_required
def admin_toggle_block(request, user_id):
    student = get_object_or_404(User, id=user_id)
    student.is_active = not student.is_active
    student.save()
    status = "Active" if student.is_active else "Blocked"
    messages.warning(request, f"User {student.username} is now {status}.")
    return redirect('admin_student_detail', user_id=user_id)

@staff_member_required
def admin_delete_student(request, user_id):
    student = get_object_or_404(User, id=user_id)
    email = student.email
    student.delete()
    messages.error(request, f"Student {email} permanently deleted.")
    return redirect('admin_student_list')

@staff_member_required
def admin_reset_password(request, user_id):
    if request.method == "POST":
        new_pass = request.POST.get('new_password')
        if new_pass:
            student = get_object_or_404(User, id=user_id)
            student.set_password(new_pass)
            student.save()
            messages.success(request, f"Password reset for {student.username}.")
    return redirect('admin_student_detail', user_id=user_id)

# --- Admin Management (Courses, Docs, Enrollments) ---

@staff_member_required
def admin_course_list(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'custom_admin/course_list.html', {'courses': courses})

@staff_member_required
def admin_edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course '{course.title}' updated successfully!")
            return redirect('admin_course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'custom_admin/course_edit.html', {'form': form, 'course': course})

@staff_member_required
def admin_delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, "Course deleted successfully.")
    return redirect('admin_dashboard')

@staff_member_required
def admin_document_list(request):
    documents = LibraryDocument.objects.all().order_by('-uploaded_at')
    return render(request, 'custom_admin/document_list.html', {'documents': documents})

@staff_member_required
def admin_edit_document(request, doc_id):
    doc = get_object_or_404(LibraryDocument, id=doc_id)
    if request.method == 'POST':
        form = LibraryDocumentForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            form.save()
            messages.success(request, "Document updated successfully!")
            return redirect('admin_document_list')
    else:
        form = LibraryDocumentForm(instance=doc)
    return render(request, 'custom_admin/document_edit.html', {'form': form, 'doc': doc})

@staff_member_required
def admin_delete_document(request, doc_id):
    doc = get_object_or_404(LibraryDocument, id=doc_id)
    doc.delete()
    messages.success(request, "Document deleted.")
    return redirect('admin_document_list')

@staff_member_required
def admin_enrollment_list(request):
    enrollments = Enrollment.objects.all().select_related('student', 'course').order_by('-enrolled_at')
    return render(request, 'custom_admin/enrollment_list.html', {'enrollments': enrollments})

@staff_member_required
def admin_delete_enrollment(request, enroll_id):
    enroll = get_object_or_404(Enrollment, id=enroll_id)
    enroll.delete()
    messages.success(request, "Enrollment removed.")
    return redirect('admin_enrollment_list')