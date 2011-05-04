class Item:
    def __init__(self, path, index):
        self.path = file_name
        self.index = index
        self.next = None
    def insert_item(self, path, index=None):
        previous = self.advance_to_index_predecessor(index)
        previous.next = Item(path, index)
        previous.increase_indicies()
    def advance_to_index_predecessor(self, index=None):
        current = self
        while current.next:
            if index != None and current.next.index >= index:
                break
            current = current.next
        return current
    def increase_indicies(self):
        current = self.next
        previous_index = self.index
        while current.index == previous_index:
            current.index += 1
            previous_index += 1
            current = current.next
    def print_items(self):
        current = self
        while current:
            print self.index, self.path
            current = current.next

