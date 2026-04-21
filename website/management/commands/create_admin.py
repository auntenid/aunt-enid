import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser if none exists, using environment variables"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.getenv("DJANGO_ADMIN_USER", "admin")
        password = os.getenv("DJANGO_ADMIN_PASSWORD", "AuntEnid2024!")
        email = os.getenv("DJANGO_ADMIN_EMAIL", "admin@twiinarides.com")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Superuser '{username}' created successfully.")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Superuser '{username}' already exists. Skipped.")
            )
