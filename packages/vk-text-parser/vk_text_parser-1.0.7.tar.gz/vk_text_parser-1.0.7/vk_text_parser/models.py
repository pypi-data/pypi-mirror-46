import datetime


class ParsedElement:
    def __init__(self, attr_id, text):
        self.attr_id = attr_id
        self.text = text
        self.parsed = datetime.datetime.now()
