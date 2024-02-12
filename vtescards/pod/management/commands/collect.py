from django.core.management.base import BaseCommand, CommandError
from pod.collectors.drivethrucards import DTCCollector
from pod.collectors.gamepod import GamepodCollector


class Command(BaseCommand):
    help = "Collects PoD data from DriveThruCards"

    def add_arguments(self, parser):
        parser.add_argument("platform", type=str)

    def handle(self, *args, **options):
        if options['platform'] == "dtc":
            DTCCollector().collect_cards()
        elif options['platform'] == "gamepod":
            GamepodCollector().collect_cards()
        else:
            raise CommandError('Platform "%s" not supported' % options['platform'])
