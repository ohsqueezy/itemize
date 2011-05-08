import os
import re
from optparse import OptionParser
from Album import *

class Itemizer:
    OPTIONS = [
        ("-d", "destination", "destination directory", "DIR", "./"),
        ("-i", "index", "item index", "INT"),
        ("-f", "delimiter", "field delimiter", "CHAR", "_"),
        ("-s", "silent", "suppress messages", None, False, "store_true"),
        ("-v", "verbose", "show details", None, False, "store_true"),
        ("--copy", "copy", "copy files", None, False, "store_true"),
        ("--deitemize", "deitemize", "deitemize", None, False, "store_true"),
        ("--sim", "simulate", "simulate itemization", None, False,
            "store_true"),
        ("--regroup", "regroup", "order items consecutively", None, False,
            "store_true"),
        ]
    USAGE_MESSAGE = "Usage: %prog [options] PATH_1..PATH_n*"
    def __init__(self):
        self.init_input()
        self.album = Album(
            self.options.destination, self.options.delimiter, self.options.copy,
            self.options.simulate, self.verbosity, self.options.regroup)
        self.album.add_items(self.item_paths, self.options.index)
        if self.options.deitemize:
            self.album.remove_items(self.options.index)
        self.album.commit()
    def init_input(self):
        self.parser = OptionParser(self.USAGE_MESSAGE)
        self.parse_arguments()
    def parse_arguments(self):
        for option in self.OPTIONS:
            default = option[4] if len(option) > 4 else None
            action = option[5] if len(option) > 5 else None
            self.parser.add_option(
                option[0], dest=option[1], help=option[2],
                metavar=option[3], default=default, action=action)
        self.options, self.item_paths = self.parser.parse_args()
        self.set_verbosity(self.options.silent, self.options.verbose)
    def set_verbosity(self, silent, verbose):
        if verbose:
            self.verbosity = 2
        elif silent:
            self.verbosity = 0
        else:
            self.verbosity = 1
    @staticmethod
    def is_item(path):
        if os.path.isfile(path):
            file_name = os.path.basename(path)
            if re.match("^[0-9]+.*", file_name):
                return True
        return False
    @staticmethod
    def extract_item_number(path):
        file_name = os.path.basename(path)
        match = re.match("^([0-9]+).*", file_name)
        if match:
            return int(match.group(1))
        return None
