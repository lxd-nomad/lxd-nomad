# -*- coding: utf-8 -*-

import logging

from .container import Container
from .logging import console_handler

logger = logging.getLogger(__name__)


class Project(object):
    """ A project is used to orchestrate a collection of containers. """

    def __init__(self, name, homedir, client, containers):
        self.name = name
        self.homedir = homedir
        self.client = client
        self.containers = containers

    @classmethod
    def from_config(cls, project_name, homedir, client, config):
        """ Creates a `Project` instance from a config object. """
        containers = []
        for container_config in config.containers:
            containers.append(Container(project_name, homedir, client, **container_config))
        return cls(project_name, homedir, client, containers)

    def destroy(self):
        """ Destroys the containers of the project. """
        for container in self._containers_generator():
            container.destroy()

    def halt(self):
        """ Stops containers of the project. """
        for container in self._containers_generator():
            container.halt()

    def provision(self):
        """ Provisions the containers of the project. """
        for container in self._containers_generator():
            container.provision()

    def shell(self):
        """ Opens a new shell in our first container. """
        self.containers[0].shell()

    def up(self):
        """ Creates, starts and provisions the containers of the project. """
        [logger.info('Bringing container "{}" up'.format(c.name)) for c in self.containers]
        for container in self._containers_generator():
            container.up()

    def _containers_generator(self):
        for container in self.containers:
            console_handler.setFormatter(logging.Formatter(
                '==> {name}: %(message)s'.format(name=container.name)))
            yield container
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(console_handler)
