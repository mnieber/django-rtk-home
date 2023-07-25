import datetime

from django.core.management.base import BaseCommand
from django_rtk_later.models import ActivationToken


class Command(BaseCommand):
    help = "Deletes all activation tokens older than 30 days"

    def handle(self, *args, **options):
        today_30_days_ago = datetime.date.today() - datetime.timedelta(days=30)
        ActivationToken.objects.filter(created__lt=today_30_days_ago).delete()
