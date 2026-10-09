"""Tests for the dashboard's request guard (security/0001-dashboard-request-guard.patch).

Why this file exists: the application source is not in this repository (it lives in the package
source project and ships to PyPI), so the fix is carried here as a patch and this test proves it
against a real checkout. Standard library only.

    WS_SRC=/path/to/package-source python3 -m unittest security/test_request_guard.py

WS_SRC is the directory that contains the `workflow_studio` package, with the patch applied.
HOME and WORKFLOW_STUDIO_DATA point at a temporary directory, so nothing on the machine is read
or written.
"""
import functools
import http.client
import io
import json
import os
import sys
import tempfile
import threading
import socketserver
import unittest

TMP = tempfile.mkdtemp(prefix="ws-guard-")
os.environ["HOME"] = TMP
os.environ["WORKFLOW_STUDIO_DATA"] = os.path.join(TMP, "data")
sys.path.insert(0, os.environ.get("WS_SRC", "."))
from workflow_studio import serve  # noqa: E402


class RequestGuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = functools.partial(serve.Handler, directory=serve.STATIC_ROOT)
        cls.httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
        cls.port = cls.httpd.server_address[1]
        serve.Handler.allowed_hosts = serve.host_allowlist("127.0.0.1", cls.port, "proxy.example")
        # Keep the real log_message: a refused request is logged through send_error, and that path
        # must not raise (0.2.0's log_message did, on its int argument). Capture the log instead.
        cls.stderr, sys.stderr = sys.stderr, io.StringIO()
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        log, sys.stderr = sys.stderr.getvalue(), cls.stderr
        assert "Traceback" not in log, log

    def req(self, method, path, host=None, headers=None, body=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        h = {"Host": host or "127.0.0.1:%d" % self.port}
        h.update(headers or {})
        conn.putrequest(method, path, skip_host=True, skip_accept_encoding=True)
        for k, v in h.items():
            conn.putheader(k, v)
        data = json.dumps(body).encode() if isinstance(body, dict) else (body or b"")
        conn.putheader("Content-Length", str(len(data)))
        conn.endheaders(data)
        res = conn.getresponse()
        res.read()
        conn.close()
        return res.status

    JSON = {"Content-Type": "application/json"}
    EMPTY = {"name": "guard-test", "script": ""}   # save_template refuses an empty script (400) before touching disk

    # Host
    def test_loopback_hosts_are_served(self):
        self.assertEqual(self.req("GET", "/context"), 200)
        self.assertEqual(self.req("GET", "/context", host="localhost:%d" % self.port), 200)
        self.assertEqual(self.req("GET", "/context", host="[::1]:%d" % self.port), 200)

    def test_rebinding_host_is_refused(self):
        self.assertEqual(self.req("GET", "/context", host="evil.example"), 403)
        self.assertEqual(self.req("GET", "/runs", host="evil.example:%d" % self.port), 403)
        self.assertEqual(self.req("HEAD", "/", host="evil.example"), 403)

    def test_loopback_on_another_port_is_refused(self):
        self.assertEqual(self.req("GET", "/context", host="127.0.0.1:1"), 403)

    def test_extra_host_without_port_allows_any_port(self):
        self.assertEqual(self.req("GET", "/context", host="proxy.example"), 200)
        self.assertEqual(self.req("GET", "/context", host="proxy.example:443"), 200)

    # POST
    def test_post_needs_json(self):
        self.assertEqual(self.req("POST", "/save", headers={"Content-Type": "text/plain"}, body=self.EMPTY), 415)
        self.assertEqual(self.req("POST", "/save", headers={"Content-Type": "application/x-www-form-urlencoded"}, body=b"name=x"), 415)

    def test_cross_origin_post_is_refused(self):
        h = dict(self.JSON, Origin="http://evil.example")
        self.assertEqual(self.req("POST", "/save", headers=h, body=self.EMPTY), 403)
        h = dict(self.JSON, Origin="null")
        self.assertEqual(self.req("POST", "/save", headers=h, body=self.EMPTY), 403)
        h = dict(self.JSON, **{"Sec-Fetch-Site": "cross-site"})
        self.assertEqual(self.req("POST", "/save", headers=h, body=self.EMPTY), 403)

    def test_same_origin_post_passes_the_guard(self):
        h = dict(self.JSON, Origin="http://127.0.0.1:%d" % self.port, **{"Sec-Fetch-Site": "same-origin"})
        self.assertEqual(self.req("POST", "/save", headers=h, body=self.EMPTY), 400)
        h = dict(self.JSON, Origin="https://proxy.example")
        self.assertEqual(self.req("POST", "/save", host="proxy.example", headers=h, body=self.EMPTY), 400)

    def test_post_without_origin_passes_the_guard(self):
        self.assertEqual(self.req("POST", "/save", headers=self.JSON, body=self.EMPTY), 400)

    def test_post_with_rebinding_host_is_refused(self):
        h = dict(self.JSON, Origin="http://evil.example")
        self.assertEqual(self.req("POST", "/save", host="evil.example", headers=h, body=self.EMPTY), 403)


if __name__ == "__main__":
    unittest.main()
