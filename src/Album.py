import os
import Itemizer
from Item import *

class Album:
    def __init__(
        self, directory_path, delimiter, copy, simulate, verbosity, regroup):
        self.set_options(delimiter, copy, simulate, verbosity, regroup)
        self.set_directory_path(directory_path)
        self.initialize_item_list()
    def set_options(self, delimiter, copy, simulate, verbosity, regroup):
        self.delimiter = delimiter
        self.copy = copy
        self.simulate = simulate
        self.verbosity = verbosity
        self.regroup = regroup
    def set_directory_path(self, directory_path):
        if not os.path.isdir(directory_path):
            print "Directory not found:", directory_path
            directory_path = None
        else:
            directory_path = os.path.join(directory_path, "")
        self.directory_path = directory_path
    def initialize_item_list(self):
        self.items = None
        if self.directory_path != None:
            for file_name in os.listdir(self.directory_path):
                path = self.directory_path + file_name
                if Itemizer.Itemizer.is_item(path):
                    number = Itemizer.Itemizer.extract_item_number(path)
                    self.add_items(path, number)
    def add_items(self, paths, index=None):
        if type(paths) == str:
            paths = [paths]
        current_index = self.build_index(index)
        for path in paths:
            if not os.path.isfile(path):
                print "File not found:", path
            else:
                if self.items == None:
                    self.add_first_item(path, current_index)
                else:
                    self.items = self.items.remove_path(path)
                    if self.items == None:
                        self.add_first_item(path, current_index)
                    else:
                        self.items = self.items.insert(path, current_index)
                if current_index:
                    current_index += 1
                if self.verbosity > 1:
                    print "Added file to list:", path
    def build_index(self, index):
        if type(index) == str:
            index = int(index)
        return index
    def add_first_item(self, path, index):
        if index == None:
            index = 1
        self.items = Item(path, index)
    def remove(self, paths):
        current = self.items
        while current != None:
            path = self.find_path_in_list(current.path, paths)
            if path:
                outgoing = current
                self.items = self.items.remove_path(outgoing.path)
                outgoing.erase_index()
                outgoing.save(
                    self.directory_path, None, self.delimiter, self.copy,
                    self.simulate, self.verbosity)
                paths.remove(path)
            current = current.next
    def find_path_in_list(self, key, paths):
        for path in paths:
            if os.path.samefile(key, path):
                return path
    def commit(self):
        if self.directory_path != None and self.items != None:
            if self.regroup:
                self.items.bunch()
            current = self.items
            prefix_length = self.determine_prefix_length()
            while current != None:
                current.save(
                    self.directory_path, prefix_length, self.delimiter,
                    self.copy, self.simulate, self.verbosity)
                current = current.next
    def print_items(self):
        current = self.items
        while current != None:
            print current
            current = current.next
    def determine_prefix_length(self):
        largest_index = self.items.get_largest_index()
        return len(str(largest_index))
