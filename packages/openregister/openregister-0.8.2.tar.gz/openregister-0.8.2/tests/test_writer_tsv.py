import io
from openregister import Item
from openregister.representations.tsv import Writer


def test_writer_zero_items():
    out = io.StringIO()
    writer = Writer(out, fieldnames=[])
    writer.close()

    string = out.getvalue()
    assert string == "\n"


def test_writer_zero_items_titles():
    out = io.StringIO()
    writer = Writer(out, fieldnames=["one", "two", "three"])
    writer.close()

    string = out.getvalue()
    assert string == "one\ttwo\tthree\n"


def test_writer_one_item():
    out = io.StringIO()
    writer = Writer(out, fieldnames=["name"])
    item = Item(name="one")
    writer.write(item)
    writer.close()

    string = out.getvalue()
    assert string == "name\none\n"


def test_writer_one_list_item():
    out = io.StringIO()
    writer = Writer(out, fieldnames=["name"])
    item = Item(name=["one", "two", "three"])
    writer.write(item)
    writer.close()

    string = out.getvalue()
    assert string == "name\none;two;three\n"


def test_writer_many_items():
    out = io.StringIO()
    writer = Writer(out, fieldnames=["name", "text"])
    for name in ["one", "two", "three"]:
        item = Item(name=name, text="hello world")
        writer.write(item)
    writer.close()

    string = out.getvalue()
    assert string == (
        "name\ttext\n" "one\thello world\n" "two\thello world\n" "three\thello world\n"
    )


def test_writer_sparse_items():
    out = io.StringIO()
    writer = Writer(out, fieldnames=["name", "text", "address", "z"])
    for name in ["one", "two", "three"]:
        item = Item(name=name, text="hello world")
        writer.write(item)
    writer.close()

    string = out.getvalue()
    assert string == (
        "name\ttext\taddress\tz\n"
        "one\thello world\t\t\n"
        "two\thello world\t\t\n"
        "three\thello world\t\t\n"
    )
