import os
import django
import random

# Django Environment Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_core.settings') 
django.setup()

from students.models import Course, Lesson

def add_hindi_content():
    print("🚀 Adding Hindi Content (CodeWithHarry, Apna College, PW, CA)...")
    
    # 1. Clean up old lessons to avoid mixing English/Broken videos
    print("🧹 Cleaning old lessons...")
    Lesson.objects.all().delete()

    courses = Course.objects.all()
    if not courses.exists():
        print("⚠️ No courses found! Create courses first.")
        return

    # --- HINDI VIDEO DATABASE (Embed Links) ---
    
    # 1. Tech & Coding (CodeWithHarry, Apna College)
    tech_videos = [
        {"url": "https://www.youtube.com/embed/7wnove7K-ZQ", "title": "Python One Shot (CodeWithHarry)"},
        {"url": "https://www.youtube.com/embed/l1EssrLxt7E", "title": "HTML/CSS Course (Apna College)"},
        {"url": "https://www.youtube.com/embed/BGTx91t8q50", "title": "Java Course in Hindi (Apna College)"},
        {"url": "https://www.youtube.com/embed/z9bZkj2M1Sk", "title": "JavaScript Tutorial (CodeWithHarry)"},
        {"url": "https://www.youtube.com/embed/6i_tt5kH9Co", "title": "Django Course (CodeWithHarry)"},
    ]

    # 2. CA & Commerce (CA Parag Gupta, Neeraj Arora)
    ca_videos = [
        {"url": "https://www.youtube.com/embed/8C7q8e1vQxk", "title": "CA Foundation Accounts (Parag Gupta)"},
        {"url": "https://www.youtube.com/embed/t83ZkC-G6vU", "title": "Company Law Revision (Neeraj Arora)"},
        {"url": "https://www.youtube.com/embed/Xq-K9yQ1x4Q", "title": "GST Basics for CA (Hindi)"},
        {"url": "https://www.youtube.com/embed/V6g4a1f5vQk", "title": "Cost Accounting Introduction"},
    ]

    # 3. Science (Physics Wallah, Unacademy JEE)
    science_videos = [
        {"url": "https://www.youtube.com/embed/9Wq-H6q1iKQ", "title": "Electric Charges (Physics Wallah)"},
        {"url": "https://www.youtube.com/embed/0sXq79q5_pI", "title": "Thermodynamics (PW - Alakh Pandey)"},
        {"url": "https://www.youtube.com/embed/yW7i5v1qK_c", "title": "Organic Chemistry Basics"},
        {"url": "https://www.youtube.com/embed/3f8H2k2z1kE", "title": "Integration Math (Hindi)"},
    ]

    # 4. Video Editing & Creative (GFXMentor - Hindi/Urdu)
    creative_videos = [
        {"url": "https://www.youtube.com/embed/sF6r34s7qE", "title": "Premiere Pro Class 1 (GFXMentor)"},
        {"url": "https://www.youtube.com/embed/WJz8LZ9b2Zk", "title": "Photoshop for Beginners (Hindi)"},
        {"url": "https://www.youtube.com/embed/5F_X1t8e3_w", "title": "After Effects Tutorial (Hindi)"},
    ]

    count = 0

    for course in courses:
        title_lower = course.title.lower()
        selected_pool = []

        # Intelligent Matching
        if "ca" in title_lower or "account" in title_lower or "tax" in title_lower or "bba" in title_lower:
            selected_pool = ca_videos
            category = "CA/Commerce"
        elif "physics" in title_lower or "chem" in title_lower or "math" in title_lower or "science" in title_lower:
            selected_pool = science_videos
            category = "Science (PW)"
        elif "edit" in title_lower or "design" in title_lower or "photo" in title_lower:
            selected_pool = creative_videos
            category = "Creative"
        else:
            # Default to Tech (Harry/Apna College) for Python, Web, AI etc.
            selected_pool = tech_videos
            category = "Tech (Harry/Apna College)"

        print(f"🔹 Adding {category} videos to: {course.title}")

        # Add 3 to 6 lessons per course
        for i in range(1, random.randint(4, 7)):
            vid = random.choice(selected_pool)
            Lesson.objects.create(
                course=course,
                title=f"L{i}: {vid['title']} - Part {i}",
                video_url=vid['url'],
                duration=f"{random.randint(15, 60)}:00",
                order=i
            )
            count += 1

    print(f"\n🎉 Success! Added {count} Hindi Videos.")
    print("Now only enrolled users can watch these specific videos!")

if __name__ == '__main__':
    add_hindi_content()