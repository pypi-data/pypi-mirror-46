from ..item import Item
from .json import load, dump, Writer


content_type = "application/json-l"


def reader(stream):
    """Read Items from a stream containing lines of JSON."""
    for line in stream:
        item = Item()
        item.json = line
        yield item


class Writer(Writer):
    """Write items to a JSON log stream"""

    def __init__(self, stream, start="", sep="", eol="\n", end=""):
        super().__init__(stream, start, sep, eol, end)


Item.jsonl = property(dump, load)
