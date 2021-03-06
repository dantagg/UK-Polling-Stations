from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection
from councils.models import Council
from data_collection.models import DataQuality
from pollingstations.models import PollingStation, PollingDistrict, ResidentialAddress

"""
Clear PollingDistrict, PollingStation and ResidentialAddress models
Clear report, num_addresses, num_districts and num_stations
fields in DataQuality model
"""


class Command(BaseCommand):

    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'data_collection' and 'pollingstations' apps
    """

    requires_system_checks = False

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)

        group.add_argument(
            "-c",
            "--council",
            nargs=1,
            help="Council ID to clear in the format X01000001",
        )

        group.add_argument(
            "-a",
            "--all",
            help="Clear data for all councils (will completely ruin your database)",
            action="store_true",
            default=False,
        )

    def handle(self, *args, **kwargs):
        """
        Manually run system checks for the
        'data_collection' and 'pollingstations' apps
        Management commands can ignore checks that only apply to
        the apps supporting the website part of the project
        """
        self.check(
            [
                apps.get_app_config("data_collection"),
                apps.get_app_config("pollingstations"),
            ]
        )

        if kwargs["council"]:
            council_id = kwargs["council"][0]
            print("Deleting data for council %s..." % (council_id))
            # check this council exists
            Council.objects.get(pk=council_id)

            PollingStation.objects.filter(council=council_id).delete()
            PollingDistrict.objects.filter(council=council_id).delete()
            ResidentialAddress.objects.filter(council=council_id).delete()

            dq = DataQuality.objects.get(council_id=council_id)
            dq.report = ""
            dq.num_addresses = 0
            dq.num_districts = 0
            dq.num_stations = 0
            dq.save()
            print("..done")

        elif kwargs.get("all"):
            print("Deleting ALL data...")
            PollingDistrict.objects.all().delete()
            PollingStation.objects.all().delete()
            ResidentialAddress.objects.all().delete()
            # use raw SQL so we don't have to loop over every single record one-by-one
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE data_collection_dataquality SET report='', num_addresses=0, num_districts=0, num_stations=0"
            )
            print("..done")
