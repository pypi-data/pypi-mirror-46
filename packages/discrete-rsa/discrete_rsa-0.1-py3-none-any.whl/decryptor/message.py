class Message:
    def __init__(self, content):
        self.content = list(content)

    def to_ascii(self):
        return list(map(ord, self.content))

    def to_char(self):
        return list(map(chr, self.content))

    def turn_string(self):
        self.content = list(map(str, self.content))

    def turn_int(self):
        self.content = list(map(int, self.content))

    def __repr__(self):
        return ''.join(self.to_char())
