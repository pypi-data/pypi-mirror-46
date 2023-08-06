# -*- coding: utf-8 -*-
import logging
import threading

import pkg_resources
from pkg_resources import VersionConflict, DistributionNotFound, UnknownExtra

COMMON_DEPENDENCIES = [
    'ml-legit>=19.5.2954',
]

GCS_DEPENDENCIES = [
    'google-cloud-storage~=1.13',
]
S3_DEPENDENCIES = [
    'boto3~=1.9',
]

KEYWORDS = []


__pip_install_lock = threading.Lock()


def install_dependencies(dependencies, throw_exception=True):
    from missinglink.sdk import install_package

    needed_dependencies = []
    for requirement in dependencies:
        if _is_dependency_installed(requirement):
            continue

        needed_dependencies += [requirement]

    if not needed_dependencies:
        return

    with __pip_install_lock:
        install_package(needed_dependencies)


def _is_dependency_installed(requirement):
    try:
        pkg_resources.require(requirement)
    except (DistributionNotFound, ) as ex:
        logging.debug('DistributionNotFound when checking if %s is installed "%s"', requirement, ex)
        return False
    except (VersionConflict, ) as ex:
        if str(ex.req) != requirement:
            logging.warning('VersionConflict when checking if %s is installed "%s"', requirement, ex)

        return False
    except (IOError, UnknownExtra) as ex:
        logging.warning('Error when checking if %s is installed "%s"', requirement, ex)
        return False

    return True
