from uuid import uuid4
from datetime import datetime, date

from shuttlis.serialization import serialize


def test_serialize_with_None():
    res = serialize(None)
    assert res is None


def test_serialize_with_uuid():
    uuid = uuid4()
    res = serialize(uuid)
    assert str(uuid) == res


def test_serialize_with_datetime():
    ts = datetime(2019, 1, 1, 8, 30, 0)
    res = serialize(ts)
    assert "2019-01-01T08:30:00" == res
    assert datetime.fromisoformat(res) == ts


def test_serialize_with_date():
    dt = date(2019, 1, 1)
    res = serialize(dt)
    assert "2019-01-01" == res
    assert date.fromisoformat(res) == dt


def test_serialize_with_byte_array():
    bytes = b"Hey Dude!!!!"
    res = serialize(bytes)
    assert "Hey Dude!!!!" == res


def test_serialize_with_list():
    uuid = uuid4()
    res = serialize([uuid])
    assert [str(uuid)] == res


def test_serialize_with_set_converts_it_to_list():
    uuid = uuid4()
    res = serialize({uuid})
    assert [str(uuid)] == res
