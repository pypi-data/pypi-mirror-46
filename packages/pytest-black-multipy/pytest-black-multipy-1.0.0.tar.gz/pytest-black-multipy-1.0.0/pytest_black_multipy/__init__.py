import importlib


def pytest_addoption(parser):
    try:
        importlib.import_module('pytest_black')
        return
    except ImportError:
        pass

    group = parser.getgroup("general")
    group.addoption(
        "--black",
        action="store_false",
        dest="name",
        default=False,
        help="Suppress black on older Pythons",
    )
