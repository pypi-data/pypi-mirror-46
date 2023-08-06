# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Track Git repository information."""

import os
import subprocess

from .tracking_info_provider import TrackingInfoProvider


class GitTrackingInfoProvider(TrackingInfoProvider):
    ENV_REPOSITORY_URI = 'AZUREML_GIT_REPOSITORY_URI'
    ENV_BRANCH = 'AZUREML_GIT_BRANCH'
    ENV_COMMIT = 'AZUREML_GIT_COMMIT'
    ENV_DIRTY = 'AZUREML_GIT_DIRTY'
    ENV_BUILD_ID = 'AZUREML_GIT_BUILD_ID'
    ENV_BUILD_URI = 'AZUREML_GIT_BUILD_URI'

    PROP_REPOSITORY_URI = 'azureml.git.repository_uri'
    PROP_BRANCH = 'azureml.git.branch'
    PROP_COMMIT = 'azureml.git.commit'
    PROP_DIRTY = 'azureml.git.dirty'
    PROP_BUILD_ID = 'azureml.git.build_id'
    PROP_BUILD_URI = 'azureml.git.build_uri'

    PROP_MLFLOW_GIT_BRANCH = 'mlflow.source.git.branch'
    PROP_MLFLOW_GIT_COMMIT = 'mlflow.source.git.commit'
    PROP_MLFLOW_GIT_REPO_URL = 'mlflow.source.git.repoURL'

    TRUE_VALUES = '1', 'true'

    @staticmethod
    def clean_property_bool(value):
        return value and str(value).strip().lower() in GitTrackingInfoProvider.TRUE_VALUES

    @staticmethod
    def clean_property_str(value):
        return value and str(value).strip() or None

    def gather(self):
        """
        Gather Git tracking info from the local environment.

        :return: Properties dictionary.
        :rtype: dict
        """
        # Check for enivronment variable overrides.
        repository_uri = os.environ.get(GitTrackingInfoProvider.ENV_REPOSITORY_URI)
        branch = os.environ.get(GitTrackingInfoProvider.ENV_BRANCH)
        commit = os.environ.get(GitTrackingInfoProvider.ENV_COMMIT)
        dirty = os.environ.get(GitTrackingInfoProvider.ENV_DIRTY)
        build_id = os.environ.get(GitTrackingInfoProvider.ENV_BUILD_ID)
        build_uri = os.environ.get(GitTrackingInfoProvider.ENV_BUILD_URI)

        # Ask git itself to fill in any blanks.
        repository_uri = repository_uri or GitTrackingInfoProvider._run_git_cmd(['ls-remote', '--get-url'])
        branch = branch or GitTrackingInfoProvider._run_git_cmd(['symbolic-ref', '--short', 'HEAD'])
        commit = commit or GitTrackingInfoProvider._run_git_cmd(['rev-parse', 'HEAD'])
        dirty = dirty or bool(GitTrackingInfoProvider._run_git_cmd(['status', '--porcelain', '.']))

        # Parsing logic.
        repository_uri = GitTrackingInfoProvider.clean_property_str(repository_uri)
        branch = GitTrackingInfoProvider.clean_property_str(branch)
        commit = GitTrackingInfoProvider.clean_property_str(commit)
        dirty = GitTrackingInfoProvider.clean_property_bool(dirty)
        build_id = GitTrackingInfoProvider.clean_property_str(build_id)
        build_uri = GitTrackingInfoProvider.clean_property_str(build_uri)

        # Return with appropriate labels.
        return {
            GitTrackingInfoProvider.PROP_REPOSITORY_URI: repository_uri,
            GitTrackingInfoProvider.PROP_BRANCH: branch,
            GitTrackingInfoProvider.PROP_COMMIT: commit,
            GitTrackingInfoProvider.PROP_DIRTY: str(dirty),
            GitTrackingInfoProvider.PROP_BUILD_ID: build_id,
            GitTrackingInfoProvider.PROP_BUILD_URI: build_uri,

            GitTrackingInfoProvider.PROP_MLFLOW_GIT_BRANCH: branch,
            GitTrackingInfoProvider.PROP_MLFLOW_GIT_COMMIT: commit,
            GitTrackingInfoProvider.PROP_MLFLOW_GIT_REPO_URL: repository_uri,
        }

    @staticmethod
    def _run_git_cmd(args):
        """Return the output of running git with arguments, or None if it fails."""
        try:
            with open(os.devnull, 'wb') as devnull:
                return subprocess.check_output(['git'] + list(args), stderr=devnull).decode()
        except KeyboardInterrupt:
            raise
        except BaseException:
            return None
