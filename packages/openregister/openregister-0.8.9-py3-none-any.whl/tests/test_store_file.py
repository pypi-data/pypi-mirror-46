from tempdir import TempDir
from openregister import Item
from openregister.stores.file import FileStore


def test_not_found():
    store = FileStore()
    item = store.item("invalid hash")
    assert item is None


def test_defaults():
    store = FileStore()
    assert store.dir == "./data"


def test_simple_store():
    with TempDir() as tmp:
        store = FileStore(dir=tmp)
        text = "This is a test"
        item = Item(text=text)
        store.put(item)

        got = store.item(item.hash)
        assert item.hash == got.hash
        assert item.text == got.text


def test_store():
    with TempDir() as tmp:
        store = FileStore(dir=tmp)

        item = Item()
        empty_hash = item.hash
        store.put(item)

        item = Item(text="Foo Value")
        foo_hash = item.hash
        store.put(item)

        item = Item(text="Bar Value")
        bar_hash = item.hash
        store.put(item)

        item = store.item(empty_hash)
        assert item.hash == empty_hash

        item = store.item(foo_hash)
        assert item.hash == foo_hash
        assert item.text == "Foo Value"

        item = store.item(bar_hash)
        assert item.hash == bar_hash
        assert item.text == "Bar Value"


def test_tags():
    with TempDir() as tmp:
        store = FileStore(dir=tmp)
        item = Item()
        item.tags = {"one", "two", "three"}
        item = store.put(item)


def test_own_dir_and_suffix():
    dir = "./tmp/testing_named_items"
    suffix = ""
    store = FileStore(dir=dir, suffix=suffix)
    assert store.dir == dir
    assert store.suffix == suffix


def test_idempotent_put():
    with TempDir() as tmp:
        store = FileStore(dir=tmp)
        item = Item(text="Idempotent?")
        store.put(item)
        store.put(item)
        store.put(item)
