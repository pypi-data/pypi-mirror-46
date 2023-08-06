from pyctmo.simulation.simfinder import SimFinder
from pyctmo.simulation.simsaver import SimSaver
from pyctmo.stats.statsfiles_runner import StatsFileRunner
from pyctmo.stats.statslogic import StatsLogic
import subprocess
import argparse
from pyctmo.db.postgresqldriver import PgSqlDriver


parser = argparse.ArgumentParser(
    description="""Helping utilities for the ctmo C++ Monte Carlo Solver. Save the simulation in DB.
                 Prepare the files for SLMC and configuration savings."""
)

# optional arguments
parser.add_argument(
    "--save",
    action="store_const",
    const=True,
    help="Perform the statistics and save the simulation in the Database.",
)


args = parser.parse_args()


def main():
    if args.save:
        PgSqlDriver.backup_db("ctmo")

        cmd_clean = r"""
                    find ./ -name "Stats*" -exec rm -rf {} \;
                    """
        subprocess.run(cmd_clean, shell=True)
        simfinder = SimFinder()
        sim_folders = simfinder.sim_folders

        stats_runner = StatsFileRunner()

        for folder in sim_folders:
            print(f"Performing pyctmo for folder = {folder}")
            stats_logic = StatsLogic(folder, is_simplelogic=True)
            startiter = stats_logic.startiter
            stats_runner.run_statsfiles(folder, startiter)
            sim_saver = SimSaver(folder, istest=False)
            sim_saver.save_sim()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

