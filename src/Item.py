import os
import re
import shutil

class Item:
    def __init__(self, path, index):
        self.path = path
        self.index = index
        self.next = None
    def __str__(self):
        return str(self.index) + "\t" + self.path
    def __len__(self):
        ii = 0
        current = self
        while current != None:
            ii += 1
            current = current.next
        return ii
    def insert(self, path, index=None):
        head = self
        previous = head.advance_to_index_predecessor(index)
        if index == None:
            index = previous.index + 1
        item = Item(path, index)
        if previous != None:
            item.next = previous.next
            previous.next = item
        else:
            item.next = head
            head = item
        item.increase_indices()
        return head
    def advance_to_index_predecessor(self, index=None):
        previous = None
        current = self
        while current != None:
            if index != None and current.index >= index:
                break
            previous = current
            current = current.next
        return previous
    def increase_indices(self):
        current = self.next
        previous_index = self.index
        while current != None and current.index == previous_index:
            current.index += 1
            previous_index += 1
            current = current.next
    def remove_path(self, path):
        head = self
        current = head
        previous = None
        while current != None:
            if os.path.samefile(path, current.path):
                if previous != None:
                    previous.next = current.next
                else:
                    head = current.next
                break
            previous = current
            current = current.next
        return head
    def bunch(self):
        index = 1
        current = self
        while current != None:
            current.index = index
            index += 1
            current = current.next
    def erase_index(self):
        self.index = None
    def save(
        self, directory_path, prefix_length, delimiter, copy, simulate,
        verbosity):
        name = self.extract_name()
        name = name.lstrip(delimiter)
        prefix = self.build_prefix(prefix_length, delimiter)
        file_name = prefix + name
        path = os.path.join(directory_path, file_name)
        self.write_path(path, copy, simulate, verbosity)
    def build_prefix(self, prefix_length, delimiter):
        prefix = ""
        if self.index != None:
            prefix = str(self.index).zfill(prefix_length) + delimiter
        return prefix
    def write_path(self, path, copy, simulate, verbosity):
        if not os.path.isfile(path) or not os.path.samefile(self.path, path):
            if not simulate:
                if copy:
                    shutil.copy(self.path, path)
                else:
                    shutil.move(self.path, path)
            if verbosity > 0:
                print "Wrote:", self.path, "=>", path
    def get_largest_index(self):
        current = self
        while current.next:
            current = current.next
        return current.index
    def extract_name(self):
        file_name = os.path.basename(self.path)
        match = re.match("^[0-9]*(.*)", file_name)
        return match.group(1)
