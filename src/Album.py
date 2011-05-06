import os
import Itemizer
from Item import *

class Album:
    def __init__(self, directory_path, separator, copy, simulate, verbosity):
        self.separator = separator
        self.copy = copy
        self.simulate = simulate
        self.verbosity = verbosity
        self.set_directory_path(directory_path)
        self.initialize_item_list()
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
        if type(index) == str:
            index = int(index)
        if type(paths) == str:
            paths = [paths]
        for path in paths:
            if not os.path.isfile(path):
                print "File not found:", path
            else:
                if self.items == None:
                    self.add_first_item(path, index)
                else:
                    self.items = self.items.remove_path(path)
                    self.items = self.items.insert(path, index)
                if index:
                    index += 1
                if self.verbosity > 1:
                    print "Added file to list:", path
    def add_first_item(self, path, index):
        if index == None:
            index = 1
        self.items = Item(path, index)
    def commit(self):
        current = self.items
        prefix_length = self.calculate_prefix_length()
        if self.directory_path != None:
            while current != None:
                current.save(
                    self.directory_path, prefix_length, self.separator, self.copy,
                    self.simulate, self.verbosity)
                current = current.next
    def print_items(self):
        current = self.items
        while current != None:
            print current
            current = current.next
    def calculate_prefix_length(self):
        if self.items != None:
            return len(str(len(self.items)))
