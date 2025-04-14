import shlex
import pytest
from contextlib import nullcontext as does_not_raises

from src.cli_config import args_parser


class TestCLIconfig:
    @pytest.mark.parametrize(
        "command, paths, report, expectation",
        [
            # one param
            ("logs/app1.log --report handlers",
             ["logs/app1.log"], "handlers", does_not_raises()
             ),
            ("logs/app2.log --report handlers",
             ["logs/app2.log"], "handlers", does_not_raises()
             ),
            ("logs/app3.log --report handlers",
             ["logs/app3.log"], "handlers", does_not_raises()
             ),
            # all params
            ("logs/app1.log logs/app2.log logs/app3.log --report handlers",
             ["logs/app1.log", "logs/app2.log",
                 "logs/app3.log"], "handlers", does_not_raises()
             ),
            # short option_param
            ("logs/app1.log -r handlers",
             ["logs/app1.log"], "handlers", does_not_raises()
             ),
            # 1 wrong path
            ("logs/app1 -r handlers",
             ["logs/app1.log"], "handlers", pytest.raises(FileNotFoundError)
             ),
            # 2 paths - 1 wrong
            ("logs/app1.log logs/app -r handlers",
             ["logs/app1.log"], "handlers", pytest.raises(FileNotFoundError)
             ),

        ])
    def test_args_parser(self, command, paths, report, expectation):
        with expectation:
            args = args_parser(shlex.split(command))
            assert args.paths == paths
            assert args.report == report
