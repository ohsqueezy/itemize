import os
import re
from optparse import OptionParser
from Item_List import *
from Album import *

class Itemizer:
    OPTIONS = [
        ("-d", "--dest", "destination", "destination directory", "DIR"),
        ("-i", "--index", "index", "item index", "INT")]
    USAGE_MESSAGE = "Usage: %prog [options] PATH_1..PATH_n*"
    FIELD_SEPARATOR = "_"
    MINIMUM_ARGUMENT_COUNT = 0
    def __init__(self):
        self.init_input()
        self.album = Album(self.options.destination)
        print self.album.items
        self.album.add_items(self.item_paths, self.options.index)
        print self.album.items
#         self.album.commit()
    def init_input(self):
        self.parser = OptionParser(self.USAGE_MESSAGE)
        self.parse_arguments()
        self.validate_args()
    def parse_arguments(self):
        for option in self.OPTIONS:
            self.parser.add_option(
                option[0], option[1], dest=option[2], help=option[3],
                metavar=option[4])
        self.options, self.item_paths = self.parser.parse_args()
    def validate_args(self):
        self.validate_arg_count()
        self.validate_arg_paths()
    def validate_arg_count(self):
        if len(self.item_paths) < self.MINIMUM_ARGUMENT_COUNT:
            self.parser.print_help()
    def validate_arg_paths(self):
        for path in reversed(self.item_paths):
            if not os.path.isfile(path):
                print "File not found:", path
                self.item_paths.pop(self.item_paths.index(path))
    @staticmethod
    def is_item(path):
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
    @classmethod
    def build_file_path(self, item, directory_path, index, prefix_length):
        item_name = self.extract_item_name(item)
        prefix = str(index).zfill(prefix_length)
        path = directory_path + prefix + self.FIELD_SEPARATOR + item_name
        return path
    @staticmethod
    def extract_item_name(path):
        file_name = os.path.basename(path)
        match = re.match("^[0-9]+(.*)", file_name)
        if match:
            return match.group(1)
        return None
    
