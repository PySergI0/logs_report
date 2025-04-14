import argparse
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


def _check_paths(args: argparse.Namespace) -> None:
    """Checks if files exist in the \logs directory passed to the command line.
    Args:
        args (argparse.Namespace): arguments passed to the terminal
    Raises:
        if the file does not exist - rases FileNotFoundError
    """
    list_files = os.listdir(BASE_DIR.joinpath("logs"))
    for path in args.paths:
        if not path.split("/")[1] in list_files:
            raise FileNotFoundError(
                f"File {path} does not exist in directory {BASE_DIR.joinpath('logs')}")


def args_parser(arg_list: list[str] | None = None) -> argparse.Namespace:
    """Processes the arguments passed to the command line
    Args:
        arg_list (list[str] | None, optional): For testing purposes. The path/paths to the log files and the name of the report. Defaults to None.
    Returns:
        argparse.Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("paths",
                        nargs="+",
                        help="Paths to log files. The number of paths is at least 1")
    parser.add_argument("-r", "--report", choices=["handlers"],
                        help="Report name",
                        )
    args = parser.parse_args(arg_list)
    _check_paths(args)
    return args
