from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import (
    Course, 
    Notification, 
    LiveClass, 
    Exam, 
    LibraryDocument, 
    Profile
)

User = get_user_model()

# ==========================================
# 1. STUDENT REGISTRATION FORM (WITH VALIDATION)
# ==========================================
class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password', 'stream', 'student_level']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose Username'}),
            'stream': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Science, Arts'}),
            'student_level': forms.Select(choices=[
                ('Beginner', 'Beginner'), 
                ('Intermediate', 'Intermediate'), 
                ('Advanced', 'Advanced')
            ], attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        """Logic: Check if email already exists."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please login.")
        return email

    def clean(self):
        """Logic: Check if passwords match."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# ==========================================
# 2. COURSE CREATION FORM (ADMIN)
# ==========================================
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'thumbnail', 'price', 'total_modules', 'difficulty_level', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Course Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed Course Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Course Price (0 for Free)'}),
            'total_modules': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Modules'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_price(self):
        """Logic: Price cannot be negative."""
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError("Price cannot be negative.")
        return price

    def clean_thumbnail(self):
        """Logic: Validate image size (Max 2MB)."""
        thumbnail = self.cleaned_data.get('thumbnail')
        if thumbnail:
            if thumbnail.size > 2 * 1024 * 1024: # 2MB limit
                raise ValidationError("Image file too large ( > 2mb ).")
        return thumbnail


# ==========================================
# 3. NOTIFICATION FORM
# ==========================================
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'message', 'is_global']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notice Headline'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Notice Content...'}),
            'is_global': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ==========================================
# 4. LIVE CLASS FORM (DATE LOGIC)
# ==========================================
class LiveClassForm(forms.ModelForm):
    class Meta:
        model = LiveClass
        fields = ['title', 'course', 'date_time', 'meeting_link', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Class Topic'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Zoom/Google Meet Link'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_date_time(self):
        """Logic: Class date cannot be in the past."""
        date_time = self.cleaned_data.get('date_time')
        if date_time < timezone.now():
            raise ValidationError("Meeting time cannot be in the past!")
        return date_time


# ==========================================
# 5. EXAM & QUIZ FORM
# ==========================================
class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'course', 'exam_link', 'description', 'deadline', 'duration_minutes', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exam Title'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'exam_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'External Link (e.g. Google Form)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration (mins)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ==========================================
# 6. LIBRARY UPLOAD FORM
# ==========================================
class LibraryDocumentForm(forms.ModelForm):
    class Meta:
        model = LibraryDocument
        fields = ['title', 'category', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Document Title'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category (e.g. Notes, Syllabus)'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        """Logic: Restrict file types (PDF, Docx only)."""
        file = self.cleaned_data.get('file')
        if file:
            ext = file.name.split('.')[-1].lower()
            valid_extensions = ['pdf', 'docx', 'doc', 'ppt', 'pptx', 'txt']
            if ext not in valid_extensions:
                raise ValidationError("Unsupported file extension. Please upload PDF or Office docs.")
        return file


# ==========================================
# 7. PROFILE PICTURE FORM (NEW ADDITION)
# ==========================================
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']
        widgets = {
           'profile_pic': forms.FileInput(attrs={'class': 'form-control', 'id': 'id_profile_pic'})
        }