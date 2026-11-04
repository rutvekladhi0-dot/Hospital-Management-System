import os
import sys
import time
import subprocess


def run(cmd):
    print(f"--> Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=True)
    return result


def main():
    print("=== Starting Medcare Vercel Build ===")

    # 1. Collect static assets
    print("--> Collecting static files...")
    run([sys.executable, "manage.py", "collectstatic", "--noinput"])

    # 2. Check Database URL
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("--> DATABASE_URL not set in build environment. Skipping database migrations.")
        print("=== Build finished successfully ===")
        return

    print("--> DATABASE_URL detected. Running database migrations...")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medcare.settings")
    import django
    django.setup()

    from django.db import connection
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            print(f"--> Testing database connection (attempt {attempt}/{max_retries})...")
            connection.ensure_connection()
            print("--> Database connection established!")
            break
        except Exception as e:
            print(f"--> Connection attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(2)
            else:
                print("--> Warning: Database unreachable during build. Proceeding with caution.")

    try:
        run([sys.executable, "manage.py", "migrate", "--noinput"])
        print("--> Database migrations completed successfully!")

        # 3. Ensure default roles & initial admin if database has no superuser
        try:
            from accounts.models import Role, User
            default_roles = [
                'Super Admin',
                'Hospital Admin',
                'Doctor',
                'Nurse',
                'Receptionist',
                'Pharmacist',
                'Lab Technician',
                'Accountant',
                'HR Manager',
                'Patient',
            ]
            for role_name in default_roles:
                Role.objects.get_or_create(name=role_name, defaults={'description': f'{role_name} role'})

            if not User.objects.filter(is_superuser=True).exists():
                admin_user = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
                admin_pass = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')
                admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@medcare.com')
                user = User.objects.create_superuser(
                    username=admin_user,
                    email=admin_email,
                    password=admin_pass,
                    first_name='Admin',
                    last_name='User'
                )
                admin_role = Role.objects.filter(name='Super Admin').first()
                if admin_role:
                    user.roles.add(admin_role)
                print(f"--> Default superuser '{admin_user}' verified/created.")
        except Exception as seed_err:
            print(f"--> Role/Admin setup notice: {seed_err}")

    except Exception as mig_err:
        print(f"--> Migration error: {mig_err}")
        sys.exit(1)

    print("=== Medcare Vercel Build Complete ===")


if __name__ == "__main__":
    main()
