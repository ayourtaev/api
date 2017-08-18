from django.core.management.base import BaseCommand
from api.models import AuthToken

class Command(BaseCommand):
    help = 'Command to create a public key'

    def handle(self, *args, **options):
        at = AuthToken.objects.create()
        self.stdout.write(self.style.SUCCESS('New auth token: {at}'.format(
            at=at.token
        )))