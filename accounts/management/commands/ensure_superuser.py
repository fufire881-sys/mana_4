"""
Idempotent superuser creation command.
Reads DJANGO_SUPERUSER_PHONE and DJANGO_SUPERUSER_PASSWORD from env.
Skips silently if a superuser with that phone already exists.
Use this instead of `createsuperuser --noinput` in deploy commands.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create a superuser if one does not already exist (idempotent)."

    def handle(self, *args, **options):
        User = get_user_model()
        phone = os.environ.get("DJANGO_SUPERUSER_PHONE")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not phone or not password:
            self.stdout.write(
                self.style.WARNING(
                    "DJANGO_SUPERUSER_PHONE or DJANGO_SUPERUSER_PASSWORD not set — skipping."
                )
            )
            return

        if User.objects.filter(phone=phone).exists():
            self.stdout.write(
                self.style.SUCCESS(f"Superuser '{phone}' already exists — skipping.")
            )
            return

        User.objects.create_superuser(phone=phone, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{phone}' created."))
