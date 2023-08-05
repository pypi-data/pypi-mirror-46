import datetime
import json
import logging
import os
import sqlite3
import typing
from contextlib import contextmanager

import pandas as pd

from r3d3.config_encoder import namedtuple_to_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("[ExperimentDB]")

default_db = "{}/experiment_v3.db".format(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.environ.get("SEARCHGANS_DB", default=default_db)

@contextmanager
def db_cursor():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        yield cursor
    except Exception as e:
        logger.error("Error: {}".format(e))
        conn.rollback()
    else:
        conn.commit()


# Initialize experiments table
def init_experiment_table(drop=False):
    with db_cursor() as cur:
        if drop:
            cur.execute("DROP TABLE IF EXISTS experiments")

        cur.execute('''CREATE TABLE IF NOT EXISTS experiments
                     (
                     experiment_id text,
                     run_id text,
                     experiment_name text,
                     date text,
                     config text,
                     metrics text,
                     owner text,
                     PRIMARY KEY (experiment_id, run_id, owner)
                     )''')


def get_nb_experiments():
    with db_cursor() as cur:
        cur.execute("SELECT count(1) FROM experiments")
        nb_experiments = cur.fetchone()[0]

    return nb_experiments


def add_experiment(experiment_id: str,
                   run_id: str,
                   experiment_name: str,
                   config: typing.NamedTuple):
    init_experiment_table()

    with db_cursor() as cur:
        date = str(datetime.datetime.now().isoformat())

        cur.execute(f"""INSERT INTO experiments VALUES (
            '{experiment_id}',
            '{run_id}',
            '{experiment_name}',
            '{date}',
            '{namedtuple_to_json(config)}',
            '',
            '{os.environ.get("USER", "unknown")}'
        )
        """)


def update_experiment(experiment_id, run_id, metrics):
    with db_cursor() as cur:
        cur.execute(f"""
        UPDATE experiments
        SET metrics = '{json.dumps(metrics)}'
        WHERE run_id = '{run_id}' AND experiment_id = '{experiment_id}'""")


def list_all_experiments():
    with db_cursor() as cur:
        ret = list()
        for row in cur.execute("SELECT * FROM experiments"):
            ret.append(row)

    return pd.DataFrame(
        data=ret,
        columns=[
            "experiment_id",
            "run_id",
            "experiment_name",
            "date",
            "config",
            "metrics",
            "owner"])


def parse_json(s):
    try:
        return json.loads(s)
    except:
        return dict()


def recursive_get(d: typing.Dict, path: str):
    path_spl = path.split(".")
    res = d
    for elem in path_spl:
        res = res.get(elem, dict())

    if isinstance(res, dict) and len(res) == 0:
        return None

    return res


def show_experiment(metarun_id: int, params: typing.Dict, metrics: typing.Dict):
    with db_cursor() as cur:
        ret = list()
        for row in cur.execute(f"SELECT * FROM experiments WHERE metarun_id = '{metarun_id}'"):
            ret.append(row)

    df = pd.DataFrame(
        data=ret,
        columns=[
            "experiment_id",
            "run_id",
            "experiment_name",
            "date",
            "config",
            "metrics",
            "owner"])
    df["run_id"] = df["run_id"].apply(int)

    for name in params:
        df[name] = df["config"].apply(lambda s: recursive_get(parse_json(s), params[name]))
    for name in metrics:
        df[name] = df["metrics"].apply(lambda s: recursive_get(parse_json(s), metrics[name]))

    df.drop(columns=["experiment_id", "experiment_name", "date", "metrics", "config", "owner"], inplace=True)

    return df
