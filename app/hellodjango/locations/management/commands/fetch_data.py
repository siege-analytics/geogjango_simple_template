# Imports
import pathlib

# Django Management Command Imports

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# Generic Python Library Imports

import sys, os
import importlib.util

# custom functions and data

# from utilities.file_utilities import *
from utilities import *

# Useful Constants

# BOUNDARIES_URL = 'https://github.com/evansiroky/timezone-boundary-builder/releases/download/2024a/timezones-with-oceans-now.shapefile.zip'


class Command(BaseCommand):
    args = ""
    help = "Fetches data specified by CLI argument, data must be in the dispatcher"

    def add_arguments(self, parser):
        parser.add_argument("models", nargs="*")

    def handle(self, *args, **kwargs):

        # get command line specified options
        model_set = kwargs["models"]
        known_models = list(DOWNLOADS_DISPATCHER.keys())

        # container variables
        models_to_work_on = []
        models_that_cannot_be_worked_on = []
        successes = []
        failures = []

        # specify which models to work on
        # if the user specifies nothing, do them all

        if len(model_set) == 0:
            models_to_work_on = known_models
        else:
            models_to_work_on = [m for m in model_set if m.lower() in known_models]
            models_that_cannot_be_worked_on = [
                m for m in model_set if not m.lower() in known_models
            ]

        print(models_that_cannot_be_worked_on)
        print(models_to_work_on)

        # start work
        try:
            for m in models_to_work_on:
                m = m.lower()
                fetch_and_load_all_data(m)
                successes.append(m)
        except Exception as e:
            message = (
                "There was an error at the management command level working on {m}: {e}"
            )
            failures.append(m)

        # count failures
        if len(failures) > 0:
            message = "\n FAILURE"
            message += f"\n The following models succeeded : {successes}"
            message += f"\n The following models failed : {failures}"

            logger.error(message)

        else:
            message = "\n SUCCESS"
            message += f"\n The following models succeeded : {successes}"
            message += f"\n The following models failed : {failures}"

            logger.info(message)


def fetch_and_unzip_the_file(model_to_work_on: str, url: str, data_type: str):
    # create path to file for download
    try:
        data_path = DATA_TYPES_TO_PATH[data_type]

        local_filename = generate_local_path_from_url(
            url=url,
            directory_path=data_path,
        )
        message = f"Successfully generated {local_filename}"
        logger.debug(message)

        downloaded_file = download_file(
            url=url,
            local_filename=local_filename,
        )

        message = f"Successfully downloaded {downloaded_file}"
        logger.debug(message)

        unzipped_file_path = unzip_file_to_its_own_directory(
            path_to_zipfile=downloaded_file, new_dir_name=None, new_dir_parent=None
        )

        message = f"Successfully unzipped {unzipped_file_path}"
        logger.debug(message)

        return unzipped_file_path

    except Exception as e:
        message = f"There was an error: {e}"
        print(message)


def fetch_and_load_all_data(model_to_work_on: str):
    message = f"Working on {model_to_work_on}"
    print(message)

    # get params
    params = DOWNLOADS_DISPATCHER[model_to_work_on]

    url = params["url"]
    data_type = params["type"].upper()
    model_to_model = params["model_to_model"]

    data_file = fetch_and_unzip_the_file(
        model_to_work_on=model_to_work_on, url=url, data_type=data_type
    )
