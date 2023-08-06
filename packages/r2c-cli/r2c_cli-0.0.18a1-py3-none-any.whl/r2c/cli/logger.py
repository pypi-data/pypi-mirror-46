import datetime
import logging
import os
import platform
import subprocess
import sys
from logging import Logger
from pathlib import Path
from subprocess import CalledProcessError

import click

LOCAL_CONFIG_DIR = os.path.join(Path.home(), ".r2c")
LOG_FILE_DIR = os.path.join(LOCAL_CONFIG_DIR, "_logs")
LOG_FILE_NAME = "r2c-debug.log"
Path(LOG_FILE_DIR).mkdir(parents=True, exist_ok=True)
LOG_FILE_LOCATION = os.path.join(LOG_FILE_DIR, LOG_FILE_NAME)
BUG_REPORTING_URL = "https://github.com/returntocorp/cli/issues/new/choose"

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fileHandler = logging.FileHandler(LOG_FILE_LOCATION, mode="w")
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()  # default stream is stderr
streamHandler.setLevel(logging.CRITICAL)  # allow some things to force prompt to user
logging.basicConfig(
    handlers=[fileHandler, streamHandler], level=logging.INFO
)  # set to info so system info can print to file
logger = logging.getLogger(
    "r2c.cli"
)  # otherwise it's r2c.cli.logger since it's in the user's logs, I think this is ok for now


def get_docker_version() -> str:
    try:
        docker_version = subprocess.check_output(["docker", "--version"])
    except CalledProcessError as e:
        return str(e)
    return docker_version.decode("utf-8").strip()


logger.info("=" * 60)
logger.info(f"System: {platform.system()}/{platform.release()}")
logger.info(f"Python: {platform.python_version()}")
logger.info(f"Timestamp: {datetime.datetime.now()}")
logger.info(f"Docker: {get_docker_version()}")
logger.info("=" * 60 + "\n")
fileHandler.setLevel(
    logging.WARNING
)  # now we just want warning and above in the debug file


def set_debug_log_level():
    level = logging.DEBUG
    logging.getLogger().setLevel(
        level
    )  # root logger instead of 'r2c' so we get all loggers in debug mode
    streamHandler.setLevel(level)
    fileHandler.setLevel(level)


def set_verbose_log_level():
    level = logging.INFO
    logging.getLogger("r2c").setLevel(level)
    streamHandler.setLevel(level)
    fileHandler.setLevel(level)


def get_logger() -> Logger:
    "Get centralized logger for cli module"
    return logger


def print_msg(message: str, err: bool = True) -> None:
    click.echo(message, err=err)


def print_success(message: str, err: bool = True) -> None:
    click.echo(click.style(f"✔ {message}", fg="green"), err=err)


def print_success_step(message: str, err: bool = True) -> None:
    click.echo(f"✔ {message}", err=err)


def print_warning(message: str, err: bool = True) -> None:
    click.echo(click.style(f"! {message}", fg="yellow"), err=err)
    logger.warning(message)


def print_error(message: str, err: bool = True, already_logged: bool = False) -> None:
    if not already_logged:
        logger.error(message)
    click.echo(click.style(f"✘ {message}", fg="red"), err=err)


def print_error_exit(
    message: str, status_code: int = 1, err: bool = True, already_logged: bool = False
) -> None:
    print_error(message, err=err, already_logged=already_logged)
    print_prompt_for_gh_issue()
    sys.exit(status_code)


def print_exception_exit(message: str, e: Exception, err: bool = True) -> None:
    logger.exception(message)
    print_error_exit(f"{message}: {str(e)}", already_logged=True)


def print_prompt_for_gh_issue() -> None:
    click.echo(
        click.style(f"Please file a bug report at ", fg="yellow")
        + click.style(BUG_REPORTING_URL, fg="blue")
        + click.style("\nwith the information provided in ", fg="yellow")
        + click.style(LOG_FILE_LOCATION, fg="white", bold=True)
    )


def abort_on_build_failure(build_status: int) -> None:
    if build_status != 0:
        print_error_exit(
            f"Failed to build analyzer: {build_status}", status_code=build_status
        )
    else:
        print_success_step("Successfully built docker.")


def log_manifest_not_found():
    print_error(
        "Couldn't find an analyzer.json for this analyzer. Check that you're currently in an analyzer directory, or make sure the --analyzer-directory path contains an analyzer.json"
    )
