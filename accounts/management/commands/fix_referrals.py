import uuid
from django.core.management.base import BaseCommand
from accounts.models import Account

class Command(BaseCommand):
    help = 'Generate referral codes for users who do not have one or have placeholder code'

    def handle(self, *args, **kwargs):
        users = Account.objects.filter(referral_code__in=['', None, 'tempcode'])
        for user in users:
            user.referral_code = str(uuid.uuid4()).replace('-', '')[:10]
            user.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {users.count()} users.'))
