import os
import Itemizer
from Item import *

class Album:
    def __init__(self, directory_path=None):
        self.set_directory_path(directory_path)
        self.initialize_item_list()
    def set_directory_path(self, directory_path):
        if directory_path == None:
            directory_path = ".";
        directory_path = directory_path.rstrip("/") + "/"
        self.directory_path = directory_path
    def initialize_item_list(self):
        self.items = None
        for file_name in os.listdir(self.directory_path):
            if Itemizer.Itemizer.is_item(file_name):
                path = self.directory_path + file_name
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
        prefix_length = self.calculate_prefix_length()
        for item in self.items:
            new_path = Itemizer.Itemizer.build_file_path(
                item, self.directory_path, self.items.index(item),
                prefix_length)
            print item, "=>", new_path
    def calculate_prefix_length(self):
        return len(str(len(self.items)))
