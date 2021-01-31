import os
from pathlib import Path

import nox
import toml

nox.options.stop_on_first_error = False
nox.options.reuse_existing_virtualenvs = True

with open("./pyproject.toml") as pyproj_toml:
    parsed_toml = toml.load(pyproj_toml)
    project_name = parsed_toml["tool"]["poetry"]["name"].replace("-", "_")


@nox.session(python=False)
def version(session):
    project_current_version = parsed_toml["tool"]["poetry"]["version"].replace("-", "_")
    suffix = os.getenv("DRONE_BUILD_NUMBER", None)
    if suffix and os.getenv("DRONE_BRANCH") != "master":
        session.run(
            "poetry", "version", f"{project_current_version}+{suffix}", external=True
        )


@nox.session(python=False)
def poetry(session):
    session.run("poetry", "install", external=True)


@nox.session(python=False)
def black(session):
    session.run("black", ".", external=True)


@nox.session(python=False)
def tests(session):
    session.run("pytest", "-rap", "-p", "no:faulthandler", "tests/", external=True)


@nox.session(python=False)
def coverage(session):
    session.run(
        "coverage",
        "run",
        f"--source={project_name}",
        "-m",
        "pytest",
        "-p",
        "no:faulthandler",
        "./tests/",
        external=True,
    )
    session.run("coverage", "report", "--fail-under=80", "-m", external=True)


@nox.session(python=False)
def flake8(session):
    session.run("pylint", "--rcfile=./nox.ini", project_name, external=True)


@nox.session(python=False)
def pylint(session):
    session.run("pylint", "--rcfile=./nox.ini", project_name, external=True)


@nox.session(python=False)
def mypy(session):
    session.env["MYPYPATH"] = project_name
    session.run("mypy", "--config-file=./nox.ini", project_name, "tests", external=True)


@nox.session(python=False)
def bandit(session):
    session.run("bandit", "-r", project_name, external=True)


@nox.session(python=False)
def build(session):
    session.run("poetry", "build", external=True)


# @nox.session(python=False)
# def build_w(session):
#     session.run(
#         "pyinstaller",
#         "--hidden-import",
#         "win32ctypes.core.ctypes",
#         "--hidden-import",
#         "win32ctypes.core.ctypes._common",
#         "--hidden-import",
#         "win32ctypes.core.ctypes._dll",
#         "--hidden-import",
#         "win32ctypes.core.ctypes._resource",
#         "--hidden-import",
#         "win32ctypes.core.ctypes._system_information",
#         "--hidden-import",
#         "win32ctypes.core.ctypes._time",
#         "--hidden-import",
#         "win32ctypes.core.ctypes._authentication",
#         "--hidden-import",
#         "win32timezone",
#         "--name",
#         "devcli",
#         os.path.join(os.getcwd(), "devcli", "entrypoint.py"),
#         "-F",
#     )
