# -*- coding: utf-8 -*-
""" Unit test for timestamp file """

import time
import os
import unittest

from commonutil_fileio_runtimerecord.timestamp import TimestampFile

SUBJECT_FILEPATH = "/tmp/test-cfrtrec-tstamp-1"


class _TestTimestampFile_General(unittest.TestCase):
	"""
	General test cases for timestamp file operations
	"""

	def setUp(self):
		self.inst = TimestampFile(None)

	def test_fetch_save_0(self):
		self.assertEqual(0, self.inst.fetch())
		self.inst.save(65536.512)
		self.assertEqual(65536, self.inst.fetch())
		self.inst.save(1024)
		self.assertEqual(65536, self.inst.fetch())

	def test_fetch_save_1(self):
		t1 = time.time()
		t0 = int(t1) - 1
		self.inst.save(t1)
		t = self.inst.fetch()
		self.assertGreaterEqual(t1, t)
		self.assertGreater(t, t0)

	def test_is_later_0(self):
		self.inst.save(65536)
		self.assertEqual(65536, self.inst.fetch())
		self.assertFalse(self.inst.is_later(65500))
		self.assertTrue(self.inst.is_later(86400))
		self.assertEqual(65536, self.inst.fetch())

	def test_is_later_1(self):
		self.inst.save(65536)
		self.assertEqual(65536, self.inst.fetch())
		self.assertFalse(self.inst.is_later(65500, update_if_later=True))
		self.assertEqual(65536, self.inst.fetch())
		self.assertTrue(self.inst.is_later(86400, update_if_later=True))
		self.assertEqual(86400, self.inst.fetch())
		self.assertFalse(self.inst.is_later(65500, update_if_later=True))
		self.assertEqual(86400, self.inst.fetch())
		self.inst.save(32767)
		self.inst.is_later(65500, update_if_later=True)
		self.assertEqual(86400, self.inst.fetch())


class TestTimestampFile_WithFile(_TestTimestampFile_General):
	"""
	Operate with file
	"""

	def setUp(self):
		try:
			os.unlink(SUBJECT_FILEPATH)
		except Exception:
			pass
		self.inst = TimestampFile(SUBJECT_FILEPATH)

	def tearDown(self):
		self.inst = None


class TestTimestampFile_WithoutFile(_TestTimestampFile_General):
	"""
	Operate with file
	"""

	def setUp(self):
		self.inst = TimestampFile(None)

	def tearDown(self):
		self.inst = None
