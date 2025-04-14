from src.cli_config import args_parser
from src.reports import Reports


def main():
    # получаем переданные аргументы в командную строку
    args = args_parser()
    # запускаем необходимый отчет
    if args.report == "handlers":
        h = Reports()
        h.handlers(args)

if __name__ == "__main__":
    main()
