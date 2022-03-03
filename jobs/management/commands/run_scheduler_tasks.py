from django.core.management.base import BaseCommand

from jobs.views import scheduler


class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler.start()
