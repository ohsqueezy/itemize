import os
import re
from optparse import OptionParser
from Album import *

class Itemizer:
    OPTIONS = [
        ("-d", "destination", "destination directory", "DIR", "./"),
        ("-i", "index", "item index", "INT"),
        ("-f", "separator", "field separator", "CHAR", "_"),
        ("--copy", "copy", "copy files", None, False, "store_true"),
        ("--sim", "simulate", "simulate itemization", None, False, "store_true")
        ]
    USAGE_MESSAGE = "Usage: %prog [options] PATH_1..PATH_n*"
    def __init__(self):
        self.init_input()
        self.album = Album(
            self.options.destination, self.options.separator,
            self.options.copy, self.options.simulate)
        self.album.add_items(self.item_paths, self.options.index)
        self.album.commit()
    def init_input(self):
        self.parser = OptionParser(self.USAGE_MESSAGE)
        self.parse_arguments()
#         self.validate_args()
    def parse_arguments(self):
        for option in self.OPTIONS:
            default = option[4] if len(option) > 4 else None
            action = option[5] if len(option) > 5 else None
            self.parser.add_option(
                option[0], dest=option[1], help=option[2],
                metavar=option[3], default=default, action=action)
        self.options, self.item_paths = self.parser.parse_args()
#     def validate_args(self):
#         self.validate_arg_paths()
#     def validate_arg_paths(self):
#         for path in reversed(self.item_paths):
#             if not os.path.isfile(path):
#                 print "File not found:", path
#                 self.item_paths.pop(self.item_paths.index(path))
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
