class Transaction:

    def __init__(self):
        self.date = None
        self.time = None
        self.action = None
        self.given = []
        self.taken = []

    def add_item(self, item):
        self.given.append(item)

    def sub_item(self, item):
        self.taken.append(item)

    def __repr__(self):
        return f'{self.date} {self.time} | {self.action}'

class Item:
    def __init__(self):
        self.name = None
        self.type = None
        self.iconUrl = None
        self.nameColor = None