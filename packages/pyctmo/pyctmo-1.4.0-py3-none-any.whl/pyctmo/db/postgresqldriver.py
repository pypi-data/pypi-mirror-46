import psycopg2
import psycopg2.extras
import configparser
import time
import pandas as pd
import warnings
from typing import List
import subprocess
import datetime as dt
from pathlib import Path
import os


ListStr_t = List[str]


from ..utils.simplelog import SimpleLog


class PgSqlDriver:

    CONFIG_ARIANN: str = "/etc/pyctmo/pyctmo.cnf"
    DICT_CURSOR_CLASS: str = "DICT"

    def __init__(self, config_file=CONFIG_ARIANN, cursorclass=""):
        self._logger = SimpleLog(logger_name="PgSqlDriver")
        self.config_file = config_file
        self._cursorclass = cursorclass

        config = configparser.ConfigParser()
        config.read(self.config_file)
        if not "POSTGRESQL" in config:
            config.clear()
            config.read(os.path.join(Path.home(), ".pyctmo/pyctmo.cnf"))

        params = dict()

        params["host"] = config.get("POSTGRESQL", "host")
        params["user"] = config.get("POSTGRESQL", "user")
        params["password"] = config.get("POSTGRESQL", "password")
        params["database"] = config.get("POSTGRESQL", "database")
        params["port"] = config.get("POSTGRESQL", "port")
        params["sslmode"] = "require"  # config.get("POSTGRESQL", "sslmode")

        self._params = params
        self._db = None  # assigned to in _connect
        self._cursor = None
        self._lastupdate = None  # assigned to in _connect
        self._connect()

    def _connect(self):
        self._db = psycopg2.connect(
            f"""
            host={self._params["host"]} user={self._params["user"]} password={self._params["password"]}
             dbname={self._params["database"]}
             port={self._params["port"]}
             sslmode={self._params["sslmode"]}
            """
        )
        # if self._cursorclass == PgSqlDriver.DICT_CURSOR_CLASS:
        self._cursor = self._db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # else:
        #     self._cursor = self._db.cursor()

        self._lastupdate = time.time()
        self._logger.debug("Postgresql connected to Database.")

    def _check_usage(self):
        if time.time() - self._lastupdate < 60:
            self._lastupdate = time.time()
            return

        # Disconnect database
        if self._db is not None:
            self._db.close()

        # Reconnect
        self._connect()

    def fetchone(self, sql, params=None):
        self._check_usage()
        cursor = self._cursor
        cursor.execute(sql, params)
        res = cursor.fetchone()
        return res

    def fetchall(self, sql, params=None):
        self._check_usage()
        cursor = self._cursor
        cursor.execute(sql, params)
        res = cursor.fetchall()
        return res

    def build_df(self, sqlcmd: str, table_name: str) -> pd.DataFrame:
        if not self._cursorclass == PgSqlDriver.DICT_CURSOR_CLASS:
            warnings.warn(
                f"get_df only implemented for cursor {PgSqlDriver.DICT_CURSOR_CLASS}"
            )
            return pd.DataFrame()

        result = self.fetchall(sqlcmd)

        sql_get_cols = f""" SELECT `column_name`
                            FROM `information_schema`.`columns`
                            WHERE `table_schema`='{self._params['database']}'
                            AND `table_name`='{table_name}';
                            """

        columns = []
        result_columns = self.fetchall(sql_get_cols)
        for dd in result_columns:
            columns.append(dd["column_name"])
        columns.sort()

        list_keys = list(result[0].keys())
        list_keys.sort()
        assert columns == list_keys
        data = dict()
        for column in columns:
            data[column] = []

        for dd in result:
            for (key, value) in dd.items():
                data[key].append(value)

        df = pd.DataFrame(data=data)
        return df

    def execute(self, sql, commit=False, params=None):
        self._check_usage()
        cursor = self._db.cursor()
        cursor.execute(sql, params)
        if commit:
            self._db.commit()

    def executemany(self, sql, commit=False, params=None):
        self._check_usage()
        cursor = self._db.cursor()
        cursor.executemany(sql, params)
        if commit:
            self._db.commit()

    def commit(self):
        self._db.commit()

    @staticmethod
    def backup_db(db_name: str):
        now_str = dt.datetime.now().strftime("%Y-%m-%d-%H-%M")
        cmd: str = f"pg_dump -Fc {db_name} > {db_name + '__' + now_str  + '.pgFc_dump'}"
        #cmd: str = f"pg_dump {db_name} > {db_name + '__' + now_str  + '.pg_dump'}"

        subprocess.run(cmd, shell=True)
