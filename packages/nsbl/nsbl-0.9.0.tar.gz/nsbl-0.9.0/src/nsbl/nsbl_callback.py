# -*- coding: utf-8 -*-

import logging
import sys

import click
from six import string_types

log = logging.getLogger("nsbl")

ENCODING = sys.stdout.encoding
if not ENCODING:
    ENCODING = "utf-8"

#
# def get_terminal_width():
#     command = ["tput", "cols"]
#     try:
#         width = int(subprocess.check_output(command))
#     except OSError:
#         return -1
#     except subprocess.CalledProcessError:
#         return -1
#     else:
#         return width


class NsblPrintCallbackAdapter(object):
    def __init__(self):

        self.environment_parameters = None

    def set_environment_parameters(self, parameters):

        self.environment_parameters = parameters

    def add_error_message(self, line):

        click.echo(line.strip())

    def add_log_message(self, line):

        click.echo(line)

    def write(self, line):

        if line.strip():
            # self.current_lines.append(line)
            self.add_log_message(line)

    def flush(self):

        pass

    def finish_up(self):
        pass


def translate_item_to_task_name(action, item):

    name = None
    if action == "install":
        if isinstance(item, string_types):
            return item

        name = item.get("name", None)
        if name is None:
            name = item.get("requirements", None)
        if name is None:
            name = item.get("repo", None)
        if name is None:
            name = item.get("url", None)
        if name is None:
            name = item.get("src", None)

    if name is None:
        name = item

    return name
