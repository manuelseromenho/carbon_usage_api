from django.core.management import BaseCommand

from carbon_usage.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = "admin"
        email = ""
        password = "a"
        print("Creating account for %s " % username)
        admin = User.objects.create_superuser(
            email=email, username=username, password=password
        )
        admin.is_active = True
        admin.is_admin = True
        admin.save()
