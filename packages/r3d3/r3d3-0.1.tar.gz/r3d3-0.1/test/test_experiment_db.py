import unittest
import typing

from r3d3 import experiment_db as db


class FakeConfig(typing.NamedTuple):
    alpha: float = 0


class TestExperimentDB(unittest.TestCase):

    def test_nb_experiments(self):
        db.init_experiment_table(drop=True)
        self.assertEqual(db.get_nb_experiments(), 0)
        db.add_experiment(
            experiment_id='0',
            run_id='1',
            experiment_name="foo",
            config=FakeConfig()
        )
        print(db.list_all_experiments())
        self.assertEqual(db.get_nb_experiments(), 1)
