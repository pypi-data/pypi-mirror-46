# -*- coding: utf-8 -*-
""" Process ID file """

import os
import sys
import errno
from hashlib import sha512
import logging

_log = logging.getLogger(__name__)


def _digest_procfs_cmdline(proc_id):
	p = "/proc/%d/cmdline" % (proc_id, )
	try:
		with open(p, "r") as fp:
			l = fp.read()
	except IOError as e:
		if e.errno == errno.ENOENT:
			return '-'
		_log.exception("failed on fetching command line info from procfs")
		return 'x'
	except Exception:
		_log.exception("failed on fetching command line info from procfs")
		return 'x'
	return sha512(l).hexdigest()


def load_pid_file_content(fp):
	process_id = None
	cmd_digest = '?'
	for n, l in enumerate(fp):
		l = l.strip()
		if n == 0:
			process_id = int(l)
		elif n == 1:
			cmd_digest = str(l)
		else:
			break
	return (process_id, cmd_digest)


# {{{ routines for checking if process is running


def _is_process_running_impl_linux(process_id, cmd_digest):
	current_cmd_digest = _digest_procfs_cmdline(process_id)
	if cmd_digest != current_cmd_digest:
		_log.debug("digest of command mismatch: (PID=%r) %r vs. %r", process_id, cmd_digest, current_cmd_digest)
		return False
	return True


def _is_process_running_impl_posix(process_id, cmd_digest):  # pylint: disable=unused-argument
	try:
		os.kill(process_id, 0)
	except OSError as e:
		if e.errno == errno.ESRCH:
			return False
		elif e.errno == errno.EPERM:
			_log.warning("given PID %r exists but cannot be signal. treat as process still running.", process_id)
			return True
		raise
	return True


def _get_process_running_checker():
	if sys.platform.startswith("linux"):
		return _is_process_running_impl_linux
	return _is_process_running_impl_posix


# }}} routines for checking if process is running


class ProcessIDFile(object):
	def __init__(self, file_path, *args, **kwds):
		super(ProcessIDFile, self).__init__(*args, **kwds)
		self.file_path = file_path
		self._is_running_checker = _get_process_running_checker()

	def fetch(self, check_running=False):
		try:
			with open(self.file_path, "r") as fp:
				process_id, cmd_digest = load_pid_file_content(fp)
		except Exception as e:
			_log.debug("cannot fetch content from PID file [%r] %r", self.file_path, e)
			return None
		if (process_id is not None) and check_running:
			if not self._is_running_checker(process_id, cmd_digest):
				return None
		return process_id

	def save(self):
		process_id = os.getpid()
		cmd_digest = _digest_procfs_cmdline(process_id)
		l0 = str(process_id) + "\n"
		l1 = cmd_digest + "\n"
		with open(self.file_path, "w") as fp:
			fp.write(l0)
			fp.write(l1)

	def is_running(self):
		if self.fetch(check_running=True) is None:
			return False
		return True

	def signal(self, sig, check_running=True):
		try:
			process_id = self.fetch(check_running)
		except Exception:
			_log.exception("failed on fetching process-id (check_running=%r)", check_running)
			process_id = None
		if process_id is not None:
			os.kill(process_id, sig)
		else:
			_log.debug("not sending signal since no PID loaded: %r", self.file_path)
		return process_id

	def remove(self):
		try:
			if not os.path.isfile(self.file_path):
				return
			os.unlink(self.file_path)
		except Exception:
			_log.exception("failed on removing PID file: %r", self.file_path)
