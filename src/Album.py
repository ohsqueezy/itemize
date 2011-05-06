import os
import Itemizer
from Item import *

class Album:
    def __init__(self, directory_path, separator, copy, simulate):
        self.separator = separator
        self.copy = copy
        self.simulate = simulate
        self.set_directory_path(directory_path)
        self.initialize_item_list()
    def set_directory_path(self, directory_path):
        directory_path = directory_path.rstrip("/") + "/"
        self.directory_path = directory_path
    def initialize_item_list(self):
        self.items = None
        for file_name in os.listdir(self.directory_path):
            path = self.directory_path + file_name
            if Itemizer.Itemizer.is_item(path):
                number = Itemizer.Itemizer.extract_item_number(path)
                if self.items == None:
                    self.items = Item(path, number)
                else:
                    self.items = self.items.insert(path, number)
    def add_items(self, paths, index=None):
        if type(index) == str:
            index = int(index)
        for path in paths:
            self.items = self.items.remove_path(path)
            self.items = self.items.insert(path, index)
            if index:
                index += 1
    def commit(self):
        current = self.items
        prefix_length = self.calculate_prefix_length()
        while current != None:
            current.save(
                self.directory_path, prefix_length, self.separator, self.copy,
                self.simulate)
            current = current.next
    def print_items(self):
        current = self.items
        while current != None:
            print current
            current = current.next
    def calculate_prefix_length(self):
        if self.items != None:
            return len(str(len(self.items)))
