class Item:

    def __init__(self):
        self.name = None
        self.classId = None
        self.type = None
        self.iconUrl = None
        self.iconUrlLarge = None
        self.nameColor = None
        self.added = False
        self.date = None
        self.time = None
        self.action = None

    def __repr__(self):
        return f'{self.date} {self.time} - {self.name} | {self.action} | {self.type}'
