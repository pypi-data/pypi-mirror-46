# -*- coding: utf-8 -*-
""" Timestamp file """

import logging

_log = logging.getLogger(__name__)


class TimestampFile(object):
	def __init__(self, file_path, *args, **kwds):
		super(TimestampFile, self).__init__(*args, **kwds)
		self.file_path = file_path
		self._last_timestamp = None

	def fetch(self):
		if self._last_timestamp is not None:
			return self._last_timestamp
		if self.file_path is None:
			return 0
		try:
			with open(self.file_path, "r") as fp:
				l = fp.read()
			t = int(l.strip())
			self._last_timestamp = t
			return t
		except Exception as e:
			_log.debug("failed on read timestamp file [%r]: %r", self.file_path, e)
		return 0

	def save(self, t):
		t = int(t)
		if (self._last_timestamp is not None) and (t <= self._last_timestamp):
			return
		self._last_timestamp = t
		if self.file_path is None:
			return
		try:
			l = str(t) + "\n"
			with open(self.file_path, "w") as fp:
				fp.write(l)
		except Exception:
			_log.exception("failed on save timestamp %r into file [%r]", t, self.file_path)

	def is_later(self, t, update_if_later=False):
		t = int(t)
		prev_t = self.fetch() if (self._last_timestamp is None) else self._last_timestamp
		if t > prev_t:
			if update_if_later:
				self.save(t)
			return True
		return False
