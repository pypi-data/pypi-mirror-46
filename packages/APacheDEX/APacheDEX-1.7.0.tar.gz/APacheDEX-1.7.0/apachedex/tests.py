import unittest
import sys
import json
import bz2
import gzip
from StringIO import StringIO
import tempfile
import apachedex
from . import lzma


class ApacheDEXTestCase(unittest.TestCase):
  def setUp(self):
    self._original_sys_argv = sys.argv
    self._original_sys_stdin = sys.stdin
    self._original_sys_stderr = sys.stderr
    self._original_sys_stdout = sys.stdout
    sys.stderr = StringIO()
    sys.stdout = StringIO()

  def tearDown(self):
    sys.argv = self._original_sys_argv
    sys.stdin = self._original_sys_stdin
    sys.stderr = self._original_sys_stderr
    sys.stdout = self._original_sys_stdout


class TestMalformedInput(ApacheDEXTestCase):
  def test_timestamp_mixed_in_timestamp(self):
    sys.argv = ['apachedex', '--base=/', '-']
    sys.stdin = StringIO(
    # this first line is valid, but second is not
    '''127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 200 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1754
127.0.0.1 - - [14/Jul/2017:127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 200 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1754''')
    apachedex.main()

    self.assertNotIn('Malformed line at -:1', sys.stderr.getvalue())
    self.assertIn('Malformed line at -:2', sys.stderr.getvalue())


class TestCharacterEncoding(ApacheDEXTestCase):
  def test_apache_referer_encoding(self):
    with tempfile.NamedTemporaryFile() as fin, tempfile.NamedTemporaryFile() as fout:
      # with apache, referer is "backslash escaped" (but quite often, referrer is %-encoded by user agent, like on
      # this example line taken from request-caddy-frontend-1/SOFTINST-49218_access_log-20190220 )
      fin.write(
        b'127.0.0.1 --  [19/Feb/2019:17:49:22 +0100] "POST /erp5/budget_module/20181219-2B1DB4A/1/Base_edit HTTP/1.1" 302 194 "https://example.org/erp5/budget_module/20181219-2B1DB4A/1/BudgetLine_viewSpreadsheet?selection_index=0&selection_name=budget_line_list_selection&ignore_layout:int=1&editable_mode=1&portal_status_message=Donn%C3%A9es%20enregistr%C3%A9es." "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36" 2999\n')
      fin.flush()
      sys.argv = ['apachedex', '--base=/', fin.name, '-f', 'json', '-o', fout.name]
      apachedex.main()
      self.assertNotIn('Malformed line', sys.stderr.getvalue())
      with open(fout.name) as f:
        self.assertTrue(json.load(f))

  def test_caddy_referer_encoding(self):
    with tempfile.NamedTemporaryFile() as fin, tempfile.NamedTemporaryFile() as fout:
      # with caddy, referer is written "as is"
      fin.write(
        # this is an (anonymised) line from request-caddy-frontend-1/SOFTINST-49218_access_log-20190220
        b'127.0.0.1 - - [19/Feb/2019:17:49:22 +0100] "GET / HTTP/1.1" 200 741 "https://example.org/erp5/budget_module/20190219-1F39610/9/BudgetLine_viewSpreadsheet?selection_index=4&selection_name=budget_line_list_selection&ignore_layout:int=1&editable_mode=1&portal_status_message=Donn\xe9es%20enregistr\xe9es." "Mozilla/5.0 (Windows NT 10.0; Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134" 7')
      fin.flush()
      sys.argv = ['apachedex', '--base=/', fin.name, '-f', 'json', '-o', fout.name]
      apachedex.main()
      with open(fout.name) as f:
        self.assertTrue(json.load(f))


class EncodedInputTestMixin:
  DEFAULT_LINE = b'127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 200 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1754'

  def test(self):
    with tempfile.NamedTemporaryFile() as fin, tempfile.NamedTemporaryFile() as fout:
      fin.write(self._getInputData())
      fin.flush()
      sys.argv = ['apachedex', '--base=/', fin.name, '-f', 'json', '-o', fout.name]
      apachedex.main()
      self.assertNotIn('Malformed line', sys.stderr.getvalue())
      with open(fout.name) as f:
        self.assertTrue(json.load(f))


class TestBzip2Encoding(ApacheDEXTestCase, EncodedInputTestMixin):
  def _getInputData(self):
    return bz2.compress(self.DEFAULT_LINE)


class TestZlibEncoding(ApacheDEXTestCase, EncodedInputTestMixin):
  def _getInputData(self):
    f = StringIO()
    with gzip.GzipFile(mode="w", fileobj=f) as gzfile:
      gzfile.write(self.DEFAULT_LINE)
    return f.getvalue()


if lzma is not None:
  class TestLzmaEncoding(ApacheDEXTestCase, EncodedInputTestMixin):
    def _getInputData(self):
      return lzma.compress(self.DEFAULT_LINE)
else:
  class TestLzmaEncoding(ApacheDEXTestCase):
    def test(self):
      self.skipTest("lzma not available")
