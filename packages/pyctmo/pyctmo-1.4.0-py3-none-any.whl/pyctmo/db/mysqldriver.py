import pymysql
import configparser
import time
import pandas as pd
import warnings
from typing import List

ListStr_t = List[str]


from ..utils.simplelog import SimpleLog


class MySqlDriver:

    CONFIG_ARIANN: str = "/etc/pyctmo/pyctmo_config"
    DICT_CURSOR_CLASS: str = "DICT"

    def __init__(self, config_file=CONFIG_ARIANN, cursorclass=""):
        self._logger = SimpleLog(logger_name="MySqlDriver")
        self.config_file = config_file
        self._cursorclass = cursorclass

        config = configparser.ConfigParser()
        config.read(self.config_file)
        params = {}
        params["cursorclass"] = (
            pymysql.cursors.DictCursor
            if cursorclass.upper() == MySqlDriver.DICT_CURSOR_CLASS
            else pymysql.cursors.Cursor
        )

        params["host"] = config.get("MYSQLDB", "host")
        params["user"] = config.get("MYSQLDB", "user")
        params["password"] = config.get("MYSQLDB", "password")
        params["database"] = config.get("MYSQLDB", "database")

        self._params = params
        self._db = None  # assigned to in _connect
        self._cursor = None
        self._lastupdate = None  # assigned to in _connect
        self._connect()

    def _connect(self):
        self._db = pymysql.connect(
            host=self._params["host"],
            user=self._params["user"],
            passwd=self._params["password"],
            db=self._params["database"],
            cursorclass=self._params["cursorclass"],
        )
        sql = "SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci"
        self._cursor = self._db.cursor()
        self._cursor.execute(sql)
        self._lastupdate = time.time()
        self._logger.debug("MySqlParser connected to Database.")

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
        cursor = self._db.cursor()
        cursor.execute(sql, params)
        res = cursor.fetchone()
        return res

    def fetchall(self, sql, params=None):
        self._check_usage()
        cursor = self._db.cursor()
        cursor.execute(sql, params)
        res = cursor.fetchall()
        return res

    @staticmethod
    def get_df(sqlcmd: str, table_name: str):
        sqldriver = MySqlDriver(cursorclass="DICT")
        return sqldriver.build_df(sqlcmd, table_name)

    def build_df(self, sqlcmd: str, table_name: str) -> pd.DataFrame:
        if not self._cursorclass == MySqlDriver.DICT_CURSOR_CLASS:
            warnings.warn(
                f"get_df only implemented for cursor {MySqlDriver.DICT_CURSOR_CLASS}"
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
