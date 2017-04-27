import json
import requests

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from wger.core.models import ApiUser
from wger import settings

class Command(BaseCommand):
    '''
    Management command to create users via API
    '''
    help = 'create users via API'

    def add_arguments(self, parser):
        '''
        Define commandline arguments to:-
            authenticate and validate app credentials
            create new API user
        '''
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('creator_username', type=str)
        parser.add_argument('creator_password', type=str)

    def handle(self, *args, **options):
        # validate APP credentials
        creator_username = options["creator_username"]
        creator_password = options["creator_password"]
        creator = User.objects.filter(username=creator_username)
        # define default user password
        if creator:
            # if the creator credentials are valid authenticate
            response = requests.post(settings.SITE_URL+reverse("rest_auth:rest_login"),
                                     {"username": creator_username, "password": creator_password})
            if response.status_code == 200:
                # get auth token from the response
                auth_token = json.loads(response.content)["key"]

                self.stdout.write("response {}".format(auth_token))
                # register new user via api endpoint
                payload = {
                    "user": {
                        "username": options["username"],
                        "email": options["email"],
                        "password": "password123"
                    },
                    "created_by": creator[0].id
                }
                # jsonify the data
                data = json.dumps(payload)
                new_api_user = requests.post(settings.SITE_URL+'/api/v2/user/',
                                             headers={
                                                 'Authorization': 'Token '+auth_token,
                                                 'content-type': 'application/json'
                                             },
                                             data=data
                                             )
                self.stdout.write("User successfully created")
            else:
                raise CommandError("Incorrect password.")
        else:
            raise CommandError("Username not known.")
