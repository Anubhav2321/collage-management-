import os
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_core.settings')
django.setup()

from students.models import User

def fix_admin_accounts():
    # Emails you want to make admin
    target_emails = ['admin@gmail.com', 'anubhva@l365.com']

    print("🚀 Starting Admin Fix Process...")
    print("-" * 50)

    for email in target_emails:
        # I am using filter() so that there is no problem even if there are multiple users.
        users = User.objects.filter(email=email)
        
        if users.exists():
            for user in users:
                try:
                    # 1. Granting admin roles and permissions
                    user.role = 'admin'
                    user.is_staff = True
                    user.is_superuser = True
                    
                    # 2. Reset the password to 'admin' (so you can login)
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