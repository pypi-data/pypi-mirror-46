import unittest

from django.core.management import BaseCommand


def print_suite(suite, stdout):
    if hasattr(suite, "__iter__"):
        for x in suite:
            print_suite(x, stdout)
    else:
        stdout.write(
            "{mod}.{klass}.{method}".format(
                mod=suite.__module__, klass=suite.__class__.__name__, method=suite._testMethodName
            )
        )


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("app_name", default=".", nargs="?")

    def handle(self, *args, **kwargs):
        app_name = kwargs.get("app_name", ".")
        print_suite(unittest.defaultTestLoader.discover(app_name), self.stdout)
