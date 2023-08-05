from .postgresqldriver import PgSqlDriver
from typing import Dict
import pandas as pd

def get_dataframes() -> Dict[str, pd.DataFrame]:
    pgdriver = PgSqlDriver()
    ctmo_tables = dict()

    sqlcmd = f"""
                SELECT * FROM simulations WHERE model_name = 'SIAM_Square';
                """
    pgdriver._check_usage()
    ctmo_tables["simulations"] = pd.read_sql(sqlcmd, pgdriver._db)
    sim_ids = tuple(ctmo_tables["simulations"]["id"].tolist())

    sqlcmd = f"""
                SELECT * FROM obs__scalar WHERE simulation_id IN {sim_ids}
                """
    pgdriver._check_usage()
    ctmo_tables["obs__scalar"] = pd.read_sql(sqlcmd, pgdriver._db)

    sqlcmd = f"""
                SELECT * FROM configs__batches WHERE simulation_id IN {sim_ids}
                """

    pgdriver._check_usage()
    ctmo_tables["configs__batches"] = pd.read_sql(sqlcmd, pgdriver._db)

    sqlcmd = f"""
                SELECT * FROM obs__gf WHERE simulation_id IN {sim_ids}
                """

    pgdriver._check_usage()
    ctmo_tables["obs__gf"] = pd.read_sql(sqlcmd, pgdriver._db)

    # ctmo_tables["configs_onemsgpack"] =
    return ctmo_tables
