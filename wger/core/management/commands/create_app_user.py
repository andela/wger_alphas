from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    '''
    Management command to create users via API
    '''
    help = 'create users via API'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        # check if app exists
        if User.objects.filter(username=options["username"]):
            self.stdout.write("Username already used".format(options["username"], options["username"]))
            return ""
        elif User.objects.filter(email=options["email"]):
            self.stdout.write("Email already used".format(options["username"], options["email"]))
            return ""
        else:
            # create APP user
            app_user = User.objects.create_user(username=options["username"],
                                                email=options["email"],
                                                password="password123"
                                                )
            app_user.save()
            self.stdout.write("New app user {} created successfully".format(options["username"]))

