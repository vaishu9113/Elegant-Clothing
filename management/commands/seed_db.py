import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import UserLogin
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seeds the database with initial superusers, updates existing users to superuser status, and generates mock user login history.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Starting database seeding...'))

        # 1. Update or create Gagankumar@gmail.com as superuser
        gagan_email = 'Gagankumar@gmail.com'
        gagan_user = User.objects.filter(email=gagan_email).first()
        if gagan_user:
            gagan_user.is_superuser = True
            gagan_user.is_staff = True
            gagan_user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated existing user {gagan_email} to Superuser & Staff!'))
        else:
            gagan_user = User.objects.create_superuser(
                username=gagan_email,
                email=gagan_email,
                password='adminpassword123',
                first_name='Gagan',
                last_name='Kumar'
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created new superuser {gagan_email} (password: adminpassword123)'))

        # 2. Ensure standard admin superuser exists
        admin_email = 'admin@elegant.com'
        admin_user = User.objects.filter(username='admin').first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username='admin',
                email=admin_email,
                password='adminpassword123',
                first_name='System',
                last_name='Administrator'
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created default superuser admin (password: adminpassword123)'))
        else:
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Default superuser admin is active.'))

        # 3. Ensure other users exist for demo purposes
        demo_users = [
            {'username': 'testuser@example.com', 'email': 'testuser@example.com', 'first_name': 'Test', 'last_name': 'User'},
            {'username': 'gagan@gmail.com', 'email': 'gagan@gmail.com', 'first_name': 'Gagan', 'last_name': 'Normal'},
        ]
        for u_data in demo_users:
            if not User.objects.filter(username=u_data['username']).exists():
                User.objects.create_user(
                    username=u_data['username'],
                    email=u_data['email'],
                    password='password123',
                    first_name=u_data['first_name'],
                    last_name=u_data['last_name']
                )
                self.stdout.write(self.style.SUCCESS(f"Created demo user {u_data['username']}"))

        # 4. Generate mock UserLogin records
        self.stdout.write(self.style.WARNING('Generating mock login history...'))
        
        # Clear existing login history to start fresh (optional, but good for clean seed)
        UserLogin.objects.all().delete()
        
        all_users = User.objects.all()
        now = timezone.now()
        
        mock_logins = []
        for i in range(15):
            user = random.choice(all_users)
            # Create a mock login at a random time in the past 7 days
            random_days = random.randint(0, 7)
            random_hours = random.randint(0, 23)
            random_minutes = random.randint(0, 59)
            login_time = now - timedelta(days=random_days, hours=random_hours, minutes=random_minutes)
            
            mock_logins.append(
                UserLogin(
                    username=user.username,
                    email=user.email,
                    login_at=login_time
                )
            )
            
        # Bulk create for efficiency
        UserLogin.objects.bulk_create(mock_logins)
        
        # Let's override the auto_now_add dynamic date so it reflects the random dates in DB
        # Note: bulk_create doesn't trigger signals, but it does respect auto_now_add upon creation.
        # To make dates look realistic, we can update them individually or just let bulk_create use current date.
        # Let's update the login_at values directly since SQLite allows direct updates.
        for ul in UserLogin.objects.all():
            random_days = random.randint(0, 7)
            random_hours = random.randint(0, 23)
            ul.login_at = now - timedelta(days=random_days, hours=random_hours)
            ul.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {UserLogin.objects.count()} user login history records!'))
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
