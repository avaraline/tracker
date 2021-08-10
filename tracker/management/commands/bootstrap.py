from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Bootstraps the site with a default "admin" user'

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.count() == 0:
            print(
                'Creating default "admin" account with password "letmein" '
                "-- change this immediately!"
            )
            User.objects.create_superuser(
                "admin",
                "admin@example.com",
                "letmein",
                first_name="Admin",
                last_name="User",
            )
