import os
import django

# Django সেটআপ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_core.settings')
django.setup()

from students.models import User

def fix_admin_accounts():
    # যে ইমেইলগুলোকে অ্যাডমিন বানাতে চান
    target_emails = ['admin@gmail.com', 'anubhva@l365.com']

    print("🚀 Starting Admin Fix Process...")
    print("-" * 50)

    for email in target_emails:
        # filter() ব্যবহার করছি যাতে একাধিক ইউজার থাকলেও সমস্যা না হয়
        users = User.objects.filter(email=email)
        
        if users.exists():
            for user in users:
                try:
                    # ১. অ্যাডমিন রোল ও পারমিশন দেওয়া
                    user.role = 'admin'
                    user.is_staff = True
                    user.is_superuser = True
                    
                    # ২. পাসওয়ার্ড রিসেট করে 'admin' করা (যাতে আপনি লগইন করতে পারেন)
                    user.set_password('admin')
                    user.save()
                    
                    print(f"✅ FIXED: User '{user.username}' ({user.email}) is now ADMIN.")
                    print(f"   🔑 New Password: admin")
                    
                except Exception as e:
                    print(f"⚠️ Error updating {user.username}: {e}")
        else:
            print(f"❌ Not Found: No user exists with email '{email}'")

    print("-" * 50)
    print("🎉 Done! Now try logging in.")

if __name__ == '__main__':
    fix_admin_accounts()