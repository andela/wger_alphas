from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from wger.core.models import ApiUser

class Command(BaseCommand):
    '''
    Management command to create users via API
    '''
    help = 'create users via API'
    #     create APP - creator
    # use APP to create user

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('creator_username', type=str)

    def handle(self, *args, **options):
        # check if user exists
        creator = User.objects.filter(username=options["creator_username"])
        if User.objects.filter(username=options["username"]):
            self.stdout.write("Username already used".format(options["username"], options["username"]))
            return ""
        elif User.objects.filter(email=options["email"]):
            self.stdout.write("Email already used".format(options["username"], options["email"]))
            return ""
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
                self.stdout.write("Creator username does not exist. Cannot create new API user.")
                return ""

