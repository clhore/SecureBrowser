# encoding: utf-8

# library
import json


# class JSON
class JSON:

    def __init__(self, file):
        self.file = file

    def read(self):
        # open and read file
        with open(self.file, 'r') as read_file:
            # read file
            _content_file = json.load(read_file)
        # return content file
        return _content_file

    def write(self, ctx=None):
        # open and write file
        with open(self.file, 'w') as write_file:
            # write ctx to file
            json.dump(ctx, write_file, indent=3)