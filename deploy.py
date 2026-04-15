#!/usr/bin/env python
"""
Deployment script for Aunt Enid Campaign Django Application
Run this script to prepare the application for production deployment
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Main deployment function"""
    print("🚀 Aunt Enid Campaign - Deployment Script")
    print("=" * 50)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aunt_enid_campaign.settings')
    django.setup()
    
    print("📋 Running deployment checks...")
    
    # Check if database exists and is migrated
    try:
        print("✓ Checking database migrations...")
        execute_from_command_line(['manage.py', 'showmigrations'])
        print("✓ Database migrations are up to date")
    except Exception as e:
        print(f"❌ Database migration error: {e}")
        return False
    
    # Collect static files
    try:
        print("✓ Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✓ Static files collected successfully")
    except Exception as e:
        print(f"❌ Static files collection error: {e}")
        return False
    
    # Check for admin user
    try:
        from django.contrib.auth.models import User
        admin_exists = User.objects.filter(username='admin').exists()
        if admin_exists:
            print("✓ Admin user exists")
        else:
            print("⚠️  Admin user not found - creating...")
            execute_from_command_line(['manage.py', 'createsuperuser', '--username', 'admin', '--email', 'admin@auntenid.com', '--noinput'])
            # Set password
            admin = User.objects.get(username='admin')
            admin.set_password('admin123')
            admin.save()
            print("✓ Admin user created (username: admin, password: admin123)")
    except Exception as e:
        print(f"❌ Admin user check error: {e}")
        return False
    
    # Check for initial data
    try:
        from website.models import SiteConfiguration
        config_exists = SiteConfiguration.objects.exists()
        if config_exists:
            print("✓ Initial data exists")
        else:
            print("⚠️  Initial data not found - populating...")
            execute_from_command_line(['manage.py', 'populate_data'])
            print("✓ Initial data populated")
    except Exception as e:
        print(f"❌ Initial data check error: {e}")
        return False
    
    print("\n🎉 Deployment preparation completed successfully!")
    print("\n📝 Next steps:")
    print("1. Set DEBUG = False in settings.py")
    print("2. Update SECRET_KEY for production")
    print("3. Configure ALLOWED_HOSTS")
    print("4. Set up production database")
    print("5. Configure static/media file serving")
    print("6. Set up SSL certificate")
    print("\n🔗 Access URLs:")
    print("- Website: http://127.0.0.1:8000/")
    print("- Admin: http://127.0.0.1:8000/admin/")
    print("- Admin credentials: admin / admin123")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
