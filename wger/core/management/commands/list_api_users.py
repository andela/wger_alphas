from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from wger.core.models import ApiUser

class Command(BaseCommand):
    '''
    Management command to create users via API
    '''
    help = 'create users via API'

    def handle(self, *args, **options):
        all_users = ApiUser.objects.all()
        for user in all_users:
            self.stdout.write("{} {}".format(user.user.username, user.user.email))

