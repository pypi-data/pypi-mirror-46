import unittest
import typing

from r3d3.config_encoder import namedtuple_to_json


class FakeSubConfig(typing.NamedTuple):
    foo: str = "bar"


class FakeConfig(typing.NamedTuple):
    alpha: float = 0
    sub_conf: FakeSubConfig = FakeSubConfig()


class TestConfigEncoder(unittest.TestCase):

    def test_encode(self):
        self.assertEqual(
            namedtuple_to_json(FakeConfig()),
            "{'alpha': 0, 'sub_conf': {'foo': 'bar'}}"
        )
