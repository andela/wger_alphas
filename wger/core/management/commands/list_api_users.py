from django.core.management.base import BaseCommand, CommandError
from tabulate import tabulate
from wger.core.models import ApiUser

class Command(BaseCommand):
    '''
    Management command to list users created via API
    '''
    help = 'List users created via API'

    def handle(self, **options):
        all_users = ApiUser.objects.all()
        headers = ["USERNAME", "EMAIL"]
        table = []
        for user in all_users:
            table.append([user.user.username, user.user.email])

        self.stdout.write(tabulate(table, headers, tablefmt="fancy_grid"))
