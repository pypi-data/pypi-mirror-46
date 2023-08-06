# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
import os

from azureml._async import WorkerPool
from azureml._history.utils.constants import (OUTPUTS_DIR, DRIVER_LOG_NAME, LOGS_AZUREML_DIR,
                                              AZUREML_LOGS, AZUREML_LOG_FILE_NAME)
from azureml._history.utils.context_managers import (LoggedExitStack, SendRunKillSignal)

EXECUTION_ENV_FRAMEWORK = "AZUREML_FRAMEWORK"
EXECUTION_ENV_COMMUNICATOR = "AZUREML_COMMUNICATOR"
PY_SPARK_FRAMEWORK = "PySpark"
TARGET_TYPE_BATCH_AI = "batchai"
DIRECTORIES_TO_WATCH = "DirectoriesToWatch"


# This logger is actually for logs happening in this file
module_logger = logging.getLogger(__name__)

AZUREML_LOG_DIR = os.environ.get("AZUREML_LOGDIRECTORY_PATH", AZUREML_LOGS)
USER_LOG_PATH = os.path.join(AZUREML_LOG_DIR, DRIVER_LOG_NAME)


def get_history_context(callback, args, module_logger, track_folders=None, deny_list=None, **kwargs):
    return get_history_context_manager(track_folders=track_folders, deny_list=deny_list, **kwargs)


def get_cleanup_context_manager(**kwargs):
    # To work around circular dependencies in the SDK
    # we have to import Run first
    from azureml.core.run import Run  # noqa: F401
    Run.get_docs_url()
    override_disable = kwargs.get("override_disable_run_kill_signal", None)
    timeout_sec = kwargs.get("run_kill_signal_timeout_sec", None)

    send_kill_signal = override_disable if override_disable else \
        not os.environ.get("AZUREML_DISABLE_RUN_KILL_SIGNAL")
    kill_signal_timeout = timeout_sec if timeout_sec else \
        float(os.environ.get("AZUREML_RUN_KILL_SIGNAL_TIMEOUT_SEC", "300"))
    return SendRunKillSignal(send_kill_signal, kill_signal_timeout)


def get_history_context_manager(track_folders=None, deny_list=None, **kwargs):
    # Configure logging for azureml namespace - debug logs+
    aml_logger = logging.getLogger('azureml')
    aml_logger.debug("Called azureml._history.utils.context_managers.get_history_context")
    directories_to_watch = kwargs.pop(DIRECTORIES_TO_WATCH, None)

    directories_to_watch = directories_to_watch if directories_to_watch is not None else []
    directories_to_watch.append(LOGS_AZUREML_DIR)

    # load the msrest logger to log requests and responses
    msrest_logger = logging.getLogger("msrest")

    aml_loggers = [aml_logger, msrest_logger]

    # Log inputs to simplify debugging remote runs
    inputs = ("Inputs:: kwargs: {kwargs}, "
              "track_folders: {track_folders}, "
              "deny_list: {deny_list}, "
              "directories_to_watch: {directories_to_watch}").format(kwargs=kwargs,
                                                                     track_folders=track_folders,
                                                                     deny_list=deny_list,
                                                                     directories_to_watch=directories_to_watch)

    if not os.path.exists(LOGS_AZUREML_DIR):
        os.makedirs(LOGS_AZUREML_DIR, exist_ok=True)
    azureml_log_file_path = os.path.join(LOGS_AZUREML_DIR, AZUREML_LOG_FILE_NAME)

    # Configure loggers to: log to known file, format logs, log at specified level
    # Send it to the tracked log folder
    file_handler = logging.FileHandler(azureml_log_file_path)
    file_handler.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')
    file_handler.setFormatter(formatter)

    # Also move this to RunConfig resolver
    LOG_LEVEL = int(os.environ.get("AZUREML_LOG_LEVEL", logging.DEBUG))

    for logger in aml_loggers:
        logger.setLevel(LOG_LEVEL)

        # This is not a great thing, but both revo and jupyter appear to add
        # root streamhandlers, causing too much information to be sent to the
        # user
        logger.propagate = 0

        logger.addHandler(file_handler)
    # Done configuring loggers
    aml_logger.debug(inputs)

    track_folders = track_folders if track_folders is not None else []
    deny_list = deny_list if deny_list is not None else []

    os.environ["AZUREML_OUTPUT_DIRECTORY"] = OUTPUTS_DIR
    if not os.path.exists(OUTPUTS_DIR):
        os.mkdir(OUTPUTS_DIR)

    context_managers = []

    # Load run and related context managers
    py_wd_cm = get_py_wd()

    worker_pool = WorkerPool(_ident="HistoryTrackingWorkerPool", _parent_logger=aml_logger)
    # Enters the worker pool so that it's the last flushed element
    context_managers.append(worker_pool)

    # Send the "about to be killed" signal so Runs can clean up quickly
    context_managers.append(get_cleanup_context_manager())

    # Important! decompose here so we don't construct a run object
    from azureml.core.run import Run
    run = Run.get_context(_worker_pool=worker_pool, allow_offline=False, py_wd=py_wd_cm,
                          outputs=track_folders + [OUTPUTS_DIR], deny_list=deny_list + [USER_LOG_PATH])
    run_context_manager = run._context_manager

    # Prepare MLflow integration if supported
    try:
        # mlflow import is needed for registering azureml tracking loaders in mlflow
        import mlflow

        # check if the mlflow features are enabled
        import azureml.contrib.mlflow
    except ImportError:
        logger.warning("Could not import azureml.contrib.mlflow mlflow APIs will not run against AzureML services."
                       " Add azureml-contrib-run as a conda dependency for the run if this behavior is desired")
    else:
        logger.debug("Installed azureml.contrib.mlflow with version {} and mlflow version {}.".format(
            azureml.contrib.mlflow.VERSION, mlflow.version.VERSION))
        azureml.contrib.mlflow._setup_remote(run)

    # Send heartbeats if enabled
    if run_context_manager.heartbeat_enabled:
        context_managers.append(run_context_manager.heartbeat_context_manager)

    # Catch sys.exit(0) - like signals from examples such as TF to avoid failing the run
    # Also set Run Errors for user failures
    context_managers.append(run_context_manager.status_context_manager)

    # TODO uncomment after fixed spark bug
    # from azureml._history.utils.daemon import ResourceMonitor
    # context_managers.append(ResourceMonitor("ResourceMonitor", aml_logger))

    # Tail the directories_to_watch to cloud
    context_managers.append(run_context_manager.get_content_uploader(directories_to_watch,
                                                                     azureml_log_file_path=azureml_log_file_path))

    # Upload the ./outputs folder and any extras we need
    context_managers.append(run_context_manager.output_file_context_manager)

    # python working directory context manager is added last to ensure the
    # working directory before and after the user code is the same for all
    # the subsequent context managers
    return LoggedExitStack(aml_logger, context_managers + [py_wd_cm])


class PythonWorkingDirectory(object):
    _python_working_directory = None

    @classmethod
    def get(cls):
        logger = module_logger.getChild(cls.__name__)
        if cls._python_working_directory is None:
            fs_list = []
            from azureml._history.utils.filesystem import PythonFS
            py_fs = PythonFS('pyfs', logger)
            fs_list.append(py_fs)
            target_type = str(os.environ.get("AZUREML_TARGET_TYPE")).lower()
            logger.debug("Execution target type: {0}".format(target_type))
            try:
                from pyspark import SparkContext
                logger.debug("PySpark found in environment.")

                if SparkContext._active_spark_context is not None:
                    logger.debug("Adding SparkDFS")
                    from azureml._history.utils.filesystem import SparkDFS
                    spark_dfs = SparkDFS("spark_dfs", logger)
                    fs_list.append(spark_dfs)
                    logger.debug("Added SparkDFS")

                else:
                    if target_type == PY_SPARK_FRAMEWORK:
                        logger.warning("No active spark context with target type {}".format(target_type))

            except ImportError as import_error:
                logger.debug("Failed to import pyspark with error: {}".format(import_error))

            from azureml._history.utils.context_managers import WorkingDirectoryCM
            cls._python_working_directory = WorkingDirectoryCM(logger, fs_list)

        return cls._python_working_directory


def get_py_wd():
    return PythonWorkingDirectory.get()
