# I'll be honest, a dict or some other data structure could've worked
# Though I made this class in part so that it would be obvious what the data structure's purpose is;
# that is to say, a dict wouldn't make it obvious that the data contained within it is for an embed field
# however the main reason I made this class was because so I could just copy paste most of
# the exiting page.add_field(name=..., value=..., etc...) headers
class EmbedField:

    def __init__(self, name: str, value):
        self.name = name
        self.value = value
