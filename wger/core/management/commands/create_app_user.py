from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    '''
    Management command to create app Users - Applications to create users via API
    '''
    help = 'create users via API'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        # check if app exists
        # admin = User.objects.filter(username="admin")
        if User.objects.filter(username=options["username"]):
            raise CommandError('Username {} already in use.'.format(options["username"]))
        elif User.objects.filter(email=options["email"]):
            raise CommandError('Email {} already in use.'.format(options["email"]))
        else:
            # create APP user
            app_user = User.objects.create_user(username=options["username"],
                                                email=options["email"],
                                                password="password123"
                                                )
            app_user.save()
            # create profile
            self.stdout.write("New app user {} created successfully".format(options["username"]))

