import os
import shlex
import pytest

from src.cli_config import BASE_DIR, args_parser
from src.reports import Reports

expected_logs = ["2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]",
                 "2025-03-28 12:21:51,000 INFO django.request: GET /admin/dashboard/ 200 OK [192.168.1.68]",
                 "2025-03-28 12:40:47,000 CRITICAL django.core.management: DatabaseError: Deadlock detected",
                 "2025-03-28 12:25:45,000 DEBUG django.db.backends: (0.41) SELECT * FROM 'products' WHERE id = 4;",
                 "2025-03-28 12:03:09,000 DEBUG django.db.backends: (0.19) SELECT * FROM 'users' WHERE id = 32;",
                 "2025-03-28 12:05:13,000 INFO django.request: GET /api/v1/reviews/ 201 OK [192.168.1.97]",
                 "2025-03-28 12:11:57,000 ERROR django.request: Internal Server Error: /admin/dashboard/ [192.168.1.29] - ValueError: Invalid input data"]


@pytest.fixture
def logs():
    expected_dict = {
        "/admin/dashboard/": {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 0,
            "ERROR": 1,
            "CRITICAL": 0,
        },
        "/api/v1/reviews/": {
            "DEBUG": 0,
            "INFO": 2,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0,
        },
    }
    report = Reports(debug=True)
    filepath = BASE_DIR.joinpath("logs/test_app.log")
    with open(filepath, "w") as file:
        for line in expected_logs:
            file.write(f"{line}\n")
    yield report, expected_dict
    os.remove(filepath)


@pytest.fixture
def args():
    test_args = args_parser(shlex.split("logs/test_app.log --report handlers"))
    return test_args


class TestReports:
    def test_read_file(self, logs, args):
        logs_list = []
        # report = logs[0]
        for line in logs[0]._read_file("".join(args.paths)):
            logs_list.append(" ".join(line))
        assert logs_list == expected_logs

    def test_handlers(self, logs, args):
        handlers_dict = logs[0].handlers(args)
        assert handlers_dict == logs[1]
