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
        item.increase_indicies()
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
    def increase_indicies(self):
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
    def save(
        self, directory_path, prefix_length, separator, copy, simulate,
        verbosity):
        name = self.extract_name()
        name = name.lstrip(separator)
        prefix = str(self.index).zfill(prefix_length)
        file_name = prefix + separator + name
        path = os.path.join(directory_path, file_name)
        if not simulate:
            if copy:
                shutil.copy(self.path, path)
            else:
                shutil.move(self.path, path)
        if verbosity > 0:
            print "Wrote:", self.path, "=>", path
    def extract_name(self):
        file_name = os.path.basename(self.path)
        match = re.match("^[0-9]*(.*)", file_name)
        return match.group(1)
