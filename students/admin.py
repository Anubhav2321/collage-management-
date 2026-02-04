from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Profile, Course, Lesson, Enrollment, 
    Notification, LiveClass, LibraryDocument, 
    Exam, Question, QuizResult, Quiz
)

# ==========================================
# 1. Custom User Admin (Student/Teacher Info)
# ==========================================
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'is_student', 'is_teacher', 'student_level')
    list_filter = ('is_student', 'is_teacher', 'student_level')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Academic Info', {'fields': ('is_student', 'is_teacher', 'student_level', 'stream')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Academic Info', {'fields': ('is_student', 'is_teacher', 'student_level', 'stream')}),
    )

admin.site.register(User, CustomUserAdmin)
# Profile is registered inline, but you can register it separately if needed
# admin.site.register(Profile) 


# ==========================================
# 2. Course & Lesson Admin
# ==========================================
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('title', 'price', 'total_modules', 'is_published', 'created_at')
    list_filter = ('is_published', 'difficulty_level')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'is_preview')
    list_filter = ('course',)


# ==========================================
# 3. Exam & Question Admin (Updated Logic)
# ==========================================
# Inline for Questions within Exam
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1  # Default will show 1 question.

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'course', 'duration_minutes', 'total_marks', 'is_active')
    list_filter = ('is_active', 'course')
    search_fields = ('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'exam', 'correct_option')
    list_filter = ('exam',)


# ==========================================
# 4. Other Features Admin
# ==========================================
admin.site.register(Enrollment)
admin.site.register(Notification)
admin.site.register(LiveClass)
admin.site.register(LibraryDocument)
admin.site.register(QuizResult)
admin.site.register(Quiz) # Dummy Quiz model registered if needed