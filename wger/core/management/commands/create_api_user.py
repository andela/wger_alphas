from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from wger.core.models import ApiUser

class Command(BaseCommand):
    '''
    Management command to create users via API
    '''
    help = 'create users via API'

    def add_arguments(self, parser):
        # add commandline arguments
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('creator_username', type=str)

    def handle(self, *args, **options):
        # check if user exists
        creator = User.objects.filter(username=options["creator_username"])
        if User.objects.filter(username=options["username"]):
            raise CommandError('Username {} already in use.'.format(options["username"]))
        elif User.objects.filter(email=options["email"]):
            raise CommandError("Email {} already in use.".format(options["email"]))
        else:
            if creator:
                # create user with default password
                app_user = User.objects.create_user(username=options["username"],
                                                    email=options["email"],
                                                    password="password123"
                                                    )
                app_user.save()
                api_user = ApiUser(user=app_user, created_by=creator[0])
                api_user.save()
                self.stdout.write("API user created.")
            else:
                raise CommandError("There is no creator with username {}. Cannot create new API user.".format(
                    options["creator_username"]))
