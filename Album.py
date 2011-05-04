import os
import Itemizer
from Item import *

class Album:
    def __init__(self, directory_path=None):
        self.set_directory_path(directory_path)
        self.initialize_item_list()
        if self.items != None:
            self.items.print_family()
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
                    self.items = self.items.insert_item(path, number)
    def find_blanks(self):
        ii = 0
        while True:
            if ii >= len(self.items):
                break
            number = Itemizer.Itemizer.extract_item_number(self.items[ii])
            expected_index = number
            if expected_index > ii:
                self.insert_blanks(expected_index - ii, ii)
            ii = expected_index + 1
    def insert_blanks(self, count, index):
        for ii in range(0, count):
            self.items.insert(index, None)
    def add_items(self, paths, index=None):
        index = self.convert_index(index)
        for path in paths:
            existing_index = self.find_path_in_items(path)
            if existing_index != None:
                self.items[existing_item] = None
            self.insert_item(path, index)
            index += 1
    def insert_item(self, path, index):
        self.items.insert(index, path)
        self.remove_first_blank(index)
    def remove_first_blank(self, start_index):
        for ii in range(start_index, len(self.items)):
            if self.items[ii] == None:
                self.items.pop(ii)
                break
    def convert_index(self, index):
        if index == None:
            index = len(self.items) + 1
        elif type(index) == str:
            index = int(index)
        return index
    def find_path_in_items(self, path):
        for item in self.items:
            if item != None and os.path.samefile(item, path):
                return self.items.index(item)
        return None
    def commit(self):
        prefix_length = self.calculate_prefix_length()
        for item in self.items:
            new_path = Itemizer.Itemizer.build_file_path(
                item, self.directory_path, self.items.index(item),
                prefix_length)
            print item, "=>", new_path
    def calculate_prefix_length(self):
        return len(str(len(self.items)))
