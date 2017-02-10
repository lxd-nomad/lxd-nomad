"""
    LXD-Nomad specific pytest fixtures
    ==================================
    This module provides fixtures that can be used to perform common operations before or after test
    execution.
"""

import os

import pytest

from nomad.client import get_client
from nomad.container import Container

__all__ = [
    'persistent_container', 'remove_persistent_container',
]


THIS_DIR = os.path.join(os.path.dirname(__file__))

_persistent_container = None


@pytest.fixture
def persistent_container():
    """ Returns a persistent `nomad.container.Container` instance.

    This container will be removed when tearing down the test class. Of course this container should
    not be removed by test methods (in that case it will be recreated) in order to speed up test
    execution.
    """
    global _persistent_container
    if _persistent_container is None:
        _persistent_container = Container(
            'lxdtestcase-persistentcontainer', THIS_DIR, get_client(), **{
                'name': 'testcase-persistent', 'image': 'ubuntu/xenial', 'mode': 'pull',
            })
    # Ensures the persistent container is up and running.
    if not _persistent_container.exists \
            or (_persistent_container.exists and _persistent_container.is_stopped):
        _persistent_container.up()
    return _persistent_container


@pytest.fixture(scope='session', autouse=True)
def remove_persistent_container():
    """ Removes the directories inside the MEDIA_ROOT that could have been filled during tests. """
    yield
    # Removes the persistent container after tests execution.
    global _persistent_container
    _persistent_container.destroy()
    del _persistent_container
