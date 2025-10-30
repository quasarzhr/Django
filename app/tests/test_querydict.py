# app/tests/test_querydict.py

from django.http import QueryDict
from django.test import SimpleTestCase


class QueryDictTests(SimpleTestCase):
    def test_create_with_no_args(self):
        self.assertEqual(QueryDict(), QueryDict(""))

    def test_missing_key(self):
        q = QueryDict()
        with self.assertRaises(KeyError):
            q.__getitem__("foo")

    def test_immutability(self):
        q = QueryDict()
        with self.assertRaises(AttributeError):
            q.__setitem__("something", "bar")
        with self.assertRaises(AttributeError):
            q.setlist("foo", ["bar"])
        with self.assertRaises(AttributeError):
            q.appendlist("foo", ["bar"])
        with self.assertRaises(AttributeError):
            q.update({"foo": "bar"})
        with self.assertRaises(AttributeError):
            q.pop("foo")
        with self.assertRaises(AttributeError):
            q.popitem()
        with self.assertRaises(AttributeError):
            q.clear()

    def test_immutable_get_with_default(self):
        q = QueryDict()
        self.assertEqual(q.get("foo", "default"), "default")

    def test_immutable_basic_operations(self):
        q = QueryDict()
        self.assertEqual(q.getlist("foo"), [])
        self.assertNotIn("foo", q)
        self.assertEqual(list(q), [])
        self.assertEqual(list(q.items()), [])
        self.assertEqual(list(q.lists()), [])
        self.assertEqual(list(q.keys()), [])
        self.assertEqual(list(q.values()), [])
        self.assertEqual(len(q), 0)
        self.assertEqual(q.urlencode(), "")

    def test_single_key_value(self):
        """Test QueryDict with one key/value pair"""

        q = QueryDict("foo=bar")
        self.assertEqual(q["foo"], "bar")
        with self.assertRaises(KeyError):
            q.__getitem__("bar")
        with self.assertRaises(AttributeError):
            q.__setitem__("something", "bar")

        self.assertEqual(q.get("foo", "default"), "bar")
        self.assertEqual(q.get("bar", "default"), "default")
        self.assertEqual(q.getlist("foo"), ["bar"])
        self.assertEqual(q.getlist("bar"), [])

        with self.assertRaises(AttributeError):
            q.setlist("foo", ["bar"])
        with self.assertRaises(AttributeError):
            q.appendlist("foo", ["bar"])

        self.assertIn("foo", q)
        self.assertNotIn("bar", q)

        self.assertEqual(list(q), ["foo"])
        self.assertEqual(list(q.items()), [("foo", "bar")])
        self.assertEqual(list(q.lists()), [("foo", ["bar"])])
        self.assertEqual(list(q.keys()), ["foo"])
        self.assertEqual(list(q.values()), ["bar"])
        self.assertEqual(len(q), 1)

        with self.assertRaises(AttributeError):
            q.update({"foo": "bar"})
        with self.assertRaises(AttributeError):
            q.pop("foo")
        with self.assertRaises(AttributeError):
            q.popitem()
        with self.assertRaises(AttributeError):
            q.clear()
        with self.assertRaises(AttributeError):
            q.setdefault("foo", "bar")

        self.assertEqual(q.urlencode(), "foo=bar")

    def test_urlencode(self):
        q = QueryDict(mutable=True)
        q["next"] = "/a&b/"
        self.assertEqual(q.urlencode(), "next=%2Fa%26b%2F")
        self.assertEqual(q.urlencode(safe="/"), "next=/a%26b/")
        q = QueryDict(mutable=True)
        q["next"] = "/t\xebst&key/"
        self.assertEqual(q.urlencode(), "next=%2Ft%C3%ABst%26key%2F")
        self.assertEqual(q.urlencode(safe="/"), "next=/t%C3%ABst%26key/")
