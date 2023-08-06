# SPDX-License-Identifier: GPL-3.0-or-later

import contextlib
import logging

import docker

import alpy.console
import alpy.node
import alpy.utils


class ControllerBase:
    def __init__(self, *, link_count, timeout, test_name, test_description):
        alpy.utils.configure_logging()
        self._link_count = link_count
        self.timeout = timeout
        self._exit_stack = contextlib.ExitStack()
        self._skeleton = None
        self.docker_client = None
        self.qmp = None
        self.console = None
        logger = logging.getLogger(__name__)
        logger.info("Test name: " + test_name)
        logger.info("Test description: " + test_description)

    def __enter__(self):
        logger = logging.getLogger(__name__)
        with self._exit_stack:
            try:
                self._create()
            except:
                logger.error("Test failed")
                raise
            self._exit_stack = self._exit_stack.pop_all()
        logger.info("Enter test environment")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self._close_after_failure()
        else:
            self._close_after_success()

    def configure_interface(self, *, node, address, gateway=None):
        self._skeleton.configure_interface(node, address, gateway)

    def tap_interfaces(self):
        return [f"alpy{i}" for i in range(self._link_count)]

    def _close_after_failure(self):
        logger = logging.getLogger(__name__)
        logger.error("Exit test environment with failure")
        try:
            self._exit_stack.close()
        finally:
            logger.error("Test failed")

    def _close_after_success(self):
        logger = logging.getLogger(__name__)
        logger.info("Exit test environment with success")
        try:
            self._exit_stack.close()
        except:
            logger.error("Test failed")
            raise
        logger.info("Test passed")

    def _create(self):

        self.docker_client = docker.from_env()
        self._exit_stack.callback(self.docker_client.close)

        self._skeleton = alpy.node.Skeleton(
            tap_interfaces=self.tap_interfaces(),
            docker_client=self.docker_client,
            timeout=self.timeout,
        )

        self._exit_stack.callback(self._skeleton.close)
        self._skeleton.create_tap_interfaces()
        qemu_args = self._get_qemu_args()

        self.qmp = self._exit_stack.enter_context(
            alpy.qemu.run(qemu_args, self.timeout)
        )

        self._skeleton.create()

        self.console = alpy.console.SerialConsole(timeout=self.timeout)

        self._exit_stack.callback(self.console.close)
        alpy.qemu.read_events(self.qmp)

    def _get_qemu_args(self):
        raise NotImplementedError
