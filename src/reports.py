import argparse
from typing import Iterator

from src.cli_config import BASE_DIR


class Reports():
    """Analyzes logs and generates a report in the console
    """
    def __init__(self, debug: bool = False) -> None:
        # словарь для подсчета общего воличества логов по каждому уровню
        self.sum_logs: dict[str: int] = {
            "DEBUG": 0,
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0,
        }
        self.levels = self.sum_logs.copy()  # словарь с уровнями логов
        # словарь, ключ - ручка API, значение - вложенный словарь self.levels
        self.dict_handlers: dict[dict[str: int]] = {}
        self.total_requests: int = 0  # кол-во обработанных логов
        self.debug = debug

    def handlers(self, args: argparse.Namespace) -> None | dict:
        """Counts the number of requests to each API handle for each logging level
        Args:
            args (argparse.Namespace): accepts the result of Argparser operation
        Returns:
            None | dict: In case of testing or debugging, it returns a dictionary. By default retutns None
        """
        marker = "django.request:"
        # итерируемся по переданным позиционным аргументам
        for path in args.paths:
            # считываем файл построчно
            for line in self._read_file(path):
                # проверям, есть ли в строке лога необходимая запись
                if marker in line:
                    self.total_requests += 1
                    # ищем в строке ручку API
                    HANDLER = "".join([i for i in line if i.startswith("/")])
                    # записываем в словарь ручку API если ее нет и во вложенном словаре
                    # увеличиваем количество по уровню лога
                    self.dict_handlers.setdefault(
                        HANDLER, self.levels.copy())[line[2]] += 1
                    self.sum_logs[line[2]] += 1
        if self.debug:
            return self.dict_handlers
        self._beautiful_print()

    def _read_file(self, path: str) -> Iterator[list]:
        """reads the logs files line by line
        Args:
            path (str): relative path to the logs file
        Returns:
            Iterator[str]: file string
        """
        with open(BASE_DIR.joinpath(path), "r") as file:
            for line in file:
                yield line.replace("\n", "").split()

    def _beautiful_print(self) -> None:
        """Prints the report
        """
        levels: list = []
        # Печатаем общее количество логов
        print(f"Total requests: {self.total_requests} \n")

        # печатаем заголовок отчета
        for hand, logs in sorted(self.dict_handlers.items(), key=lambda x: x):
            for level in logs.keys():
                levels.append(level)
        print(
            "HANDLER".ljust(20, " "),
            levels[0].ljust(10, " "),
            levels[1].ljust(10, " "),
            levels[2].ljust(10, " "),
            levels[3].ljust(10, " "),
            levels[4].ljust(10, " "),
        )
        # печатаем ручки API и кол-во логов по каждому уровню
        for hand, logs in sorted(self.dict_handlers.items(), key=lambda x: x):
            print(hand.ljust(21, " "),
                  str(logs["DEBUG"]).ljust(10, " "),
                  str(logs["INFO"]).ljust(10, " "),
                  str(logs["WARNING"]).ljust(10, " "),
                  str(logs["ERROR"]).ljust(10, " "),
                  str(logs["CRITICAL"]).ljust(10, " "),
                  )
        # печатаем итоговое кол-во логов по каждому уровню отдельно
        print(
            "Total -- ".ljust(21, " "),
            str(self.sum_logs[levels[0]]).ljust(10, " "),
            str(self.sum_logs[levels[1]]).ljust(10, " "),
            str(self.sum_logs[levels[2]]).ljust(10, " "),
            str(self.sum_logs[levels[3]]).ljust(10, " "),
            str(self.sum_logs[levels[4]]).ljust(10, " "),

        )
