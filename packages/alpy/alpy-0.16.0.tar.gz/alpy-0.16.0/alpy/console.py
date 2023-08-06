# SPDX-License-Identifier: GPL-3.0-or-later

import contextlib
import logging
import pathlib
import random
import socket
import threading

import pexpect
import pexpect.fdpexpect

import alpy.pexpect_log
import alpy.utils

PORT = 2023


class SerialConsole:
    def __init__(self, *, timeout, host="127.0.0.1", port=PORT):
        log = alpy.utils.context_logger(__name__)
        with log("Connect to serial console"):
            self._serial_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )
            try:
                self._serial_socket.connect((host, port))

                self.fdpexpect_handle = pexpect.fdpexpect.fdspawn(
                    self._serial_socket, timeout=timeout
                )
                logger = logging.getLogger(__name__)
                self._logfile_read = alpy.pexpect_log.LogfileRead(logger)
                self.fdpexpect_handle.logfile_read = self._logfile_read
                self.fdpexpect_handle.logfile_send = alpy.pexpect_log.LogfileSend(
                    logger
                )
            except:
                self._serial_socket.close()
                raise

    def expect_exact(self, pattern):
        self.fdpexpect_handle.expect_exact(pattern)
        self._logfile_read.log_remaining_text()

    def sendline(self, data):
        self.fdpexpect_handle.sendline(data)

    @contextlib.contextmanager
    def read_in_background(self):
        stop_reading = threading.Event()

        def console_read():
            while not stop_reading.is_set():
                self.fdpexpect_handle.expect_exact(pexpect.TIMEOUT, timeout=0.5)

        thread = threading.Thread(target=console_read)
        thread.start()
        try:
            yield
        finally:
            stop_reading.set()
            thread.join()

    def close(self):
        log = alpy.utils.context_logger(__name__)
        with log("Close serial console"):
            self.fdpexpect_handle.expect_exact(
                [pexpect.EOF, pexpect.TIMEOUT], timeout=1
            )

            self.fdpexpect_handle.close()
            self._logfile_read.log_remaining_text()


def random_delimiter():
    return f"eof{random.randrange(1000000):06}"


def upload_text_file(console, prompt, source_filename, destination_filename):
    delimiter = random_delimiter()
    console.expect_exact(prompt)
    # Delimiter is quoted in order to disable parameter expansion etc. in the
    # here-document.
    command = f"cat > {destination_filename} <<'{delimiter}'"
    console.sendline(command)
    console.expect_exact(command + "\r\n")
    console.fdpexpect_handle.send(pathlib.Path(source_filename).read_bytes())
    console.sendline(delimiter)
    console.expect_exact(delimiter)


def execute_program(console, prompt, program, timeout):
    console.expect_exact(prompt)
    command = program + "; echo Exit status: $?."
    console.sendline(command)
    console.expect_exact(f"{command}\r\n")
    console.fdpexpect_handle.expect(r"Exit status: (\d+).", timeout=timeout)
    exit_status_bytes = console.fdpexpect_handle.match.group(1)
    return int(exit_status_bytes.decode())


def check_execute_program(console, prompt, program, timeout):
    exit_status = execute_program(console, prompt, program, timeout)

    if exit_status != 0:
        raise alpy.utils.NonZeroExitCode(
            f"Program {program} exited with non-zero code {exit_status}"
        )


def upload_and_execute_script(console, prompt, filename, timeout):

    log = alpy.utils.context_logger(__name__)
    logger = logging.getLogger(__name__)

    with log("Type in script " + filename):
        upload_text_file(console, prompt, filename, filename)
        console.expect_exact(prompt)
        command = "chmod +x " + filename
        console.sendline(command)
        console.expect_exact(f"{command}\r\n")

    with log("Run script " + filename):
        if timeout != console.fdpexpect_handle.timeout:
            logger.info(f"Timeout, seconds: {timeout}")
        check_execute_program(console, prompt, "./" + filename, timeout)
