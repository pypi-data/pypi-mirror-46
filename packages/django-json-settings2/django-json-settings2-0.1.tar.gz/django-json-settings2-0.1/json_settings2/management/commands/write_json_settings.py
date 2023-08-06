from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from json_settings2 import write_settings_from_django


class Command(BaseCommand):
    help = 'Write specified django settings to file.'

    def add_arguments(self, parser):
        parser.add_argument(
            'django_settings',
            nargs='+',
            help='Django settings variables that should be written to file',
        )
        parser.add_argument(
            '-f',
            '--filename',
            action='store',
            default='.settings.json',
            dest='filename',
            help='Filename to save settings as. Defaults to .settings.json',
        )
        parser.add_argument(
            '-d',
            '--directory',
            action='store',
            default='.',
            dest='directory',
            help=(
                'Directory to save settings file in. '
                'Defaults to <current directory>'
            ),
        )
        parser.add_argument(
            '-i',
            '--indent',
            action='store',
            type=int,
            default=4,
            dest='indent',
            help='Indentation level for json output. Defaults to 4.',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            default=False,
            dest='force',
            help=(
                'If settings file already exists, overwrite it. '
                'Defaults to False'
            ),
        )

    def handle(self, *args, **options):
        write_settings_from_django(
            *options['django_settings'],
            filename=options['filename'],
            directory=options['directory'],
            indent=options['indent'],
            force=options['force'],
        )
