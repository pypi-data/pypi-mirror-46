
import argparse
import logging.config
import sys

from colibris import settings
from colibris import utils


class BaseCommand:
    def __init__(self, args):
        self.args = args
        self.parser = argparse.ArgumentParser()
        self.add_arguments(self.parser)

    def initialize(self):
        pass

    def run(self):
        self.initialize()
        options = self.parser.parse_args(self.args)
        self.execute(options)

    def add_arguments(self, parser):
        pass

    def execute(self, options):
        raise NotImplementedError

    @classmethod
    def get_name(cls):
        return cls.__name__[0:-7].lower()


def gather_all_commands():
    global ALL_COMMANDS

    # import any project-specific commands
    utils.import_module_or_none('{}.commands'.format(settings.PROJECT_PACKAGE_NAME))

    ALL_COMMANDS = {c.get_name(): c for c in BaseCommand.__subclasses__()}


def show_commands_usage():
    cmds = '\n  '.join([c.get_name() for c in ALL_COMMANDS.values()])
    usage = '{prog} <command> [args]\n\n' \
            'available commands:\n  {cmds}\n\n' \
            'use {prog} <command> -h for help'

    usage = usage.format(cmds=cmds, prog='manage.py')

    print(usage)


def main():
    gather_all_commands()

    args = sys.argv
    if len(args) < 2 or args[1] not in ALL_COMMANDS:
        show_commands_usage()
        sys.exit(1)

    # configure logging
    logging_config = dict(settings.LOGGING)
    logging_config['disable_existing_loggers'] = False
    utils.dict_update_rec(logging_config, settings.LOGGING_OVERRIDES)

    logging.config.dictConfig(logging_config)

    command_class = ALL_COMMANDS[sys.argv[1]]
    command = command_class(args[2:])
    command.run()


from . import makemigrations
from . import migrate
from . import runserver
from . import runworker
from . import shell
