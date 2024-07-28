from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Create or update a superuser with a predefined password'

    def handle(self, *args, **kwargs):
        User = get_user_model()  # Get the custom user model
        username = "test"
        email = "testadmin@gmail.com"
        password = "test@1234"

        try:
            # Check if the superuser already exists
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )

            if created:
                user.set_password(password)  # Hash the password
                user.is_superuser = True
                user.is_staff = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Superuser {username} created'))
            else:
                # Update the user if it already exists
                user.email = email
                user.set_password(password)  # Hash the password
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Superuser {username} already exists. Updated password.'))

        except IntegrityError:
            self.stdout.write(self.style.ERROR(f'Error creating superuser {username}.'))
