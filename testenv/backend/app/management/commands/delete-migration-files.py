import glob
import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Deletes all migration Python files for all local apps"

    def add_arguments(self, parser):
        parser.add_argument(
            "--list", action="store_true", help="List files but do not delete them"
        )

    def handle(self, *args, **options):
        local_app_names = [x.split(".")[0] for x in settings.LOCAL_APPS]
        for name, app in apps.app_configs.items():
            if name in local_app_names:
                for migration_fn in glob.glob(app.path + "/migrations/*.py"):
                    if not migration_fn.endswith("__init__.py"):
                        if options["list"]:
                            print(migration_fn)
                        else:
                            os.unlink(migration_fn)
