"""
OC Channel Client — sends messages to OC via the oac-bridge channel webhook
and receives replies via an HTTP callback server.

Flow:
  OAC ──POST /webhook/oac-bridge──▶ OC Gateway
       ◀──POST /oc-reply──────────  OC (callback)
"""

import json
import threading
import time
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Callable, Dict, List, Optional
from urllib.parse import urljoin

import requests
from loguru import logger


class OcReplyMessage:
    """A single reply from OC delivered via callback."""

    def __init__(self, oac_session_id: str, text: str, timestamp: float):
        self.oac_session_id = oac_session_id
        self.text = text
        self.timestamp = timestamp


class OcReplyQueue:
    """Thread-safe reply queue indexed by oac_session_id."""

    def __init__(self):
        self._lock = threading.Lock()
        self._queues: Dict[str, List[OcReplyMessage]] = defaultdict(list)
        self._events: Dict[str, threading.Event] = {}
        self._callbacks: Dict[str, Callable[[OcReplyMessage], None]] = {}

    def push(self, msg: OcReplyMessage):
        with self._lock:
            self._queues[msg.oac_session_id].append(msg)
            evt = self._events.get(msg.oac_session_id)
            cb = self._callbacks.get(msg.oac_session_id)
        if evt:
            evt.set()
        if cb:
            try:
                cb(msg)
            except Exception as e:
                logger.warning(f"[OcReplyQueue] callback error: {e}")

    def wait_for_reply(
        self, oac_session_id: str, timeout: float = 60.0
    ) -> Optional[OcReplyMessage]:
        """Block until a reply arrives for this session, or timeout."""
        evt = threading.Event()
        with self._lock:
            pending = self._queues.get(oac_session_id)
            if pending:
                return pending.pop(0)
            self._events[oac_session_id] = evt

        evt.wait(timeout=timeout)

        with self._lock:
            self._events.pop(oac_session_id, None)
            pending = self._queues.get(oac_session_id)
            if pending:
                return pending.pop(0)
        return None

    def register_callback(
        self, oac_session_id: str, cb: Callable[[OcReplyMessage], None]
    ):
        with self._lock:
            self._callbacks[oac_session_id] = cb

    def unregister_callback(self, oac_session_id: str):
        with self._lock:
            self._callbacks.pop(oac_session_id, None)


class _CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler that receives OC replies at /oc-reply."""

    reply_queue: Optional[OcReplyQueue] = None
    expected_token: str = ""

    def do_POST(self):
        if self.path != "/oc-reply":
            self.send_response(404)
            self.end_headers()
            return

        if self.expected_token:
            auth = self.headers.get("Authorization", "")
            if not auth.startswith("Bearer ") or auth[7:] != self.expected_token:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'{"error":"unauthorized"}')
                return

        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 256 * 1024:
            self.send_response(413)
            self.end_headers()
            return

        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error":"invalid json"}')
            return

        oac_session_id = data.get("oac_session_id", "")
        text = data.get("text", "")
        if not oac_session_id or not text:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error":"missing oac_session_id or text"}')
            return

        msg = OcReplyMessage(
            oac_session_id=oac_session_id,
            text=text,
            timestamp=data.get("timestamp", time.time()),
        )
        logger.info(
            f"[OcCallbackServer] Received OC reply "
            f"(session={oac_session_id}, len={len(text)}): "
            f"{text[:120]}..."
        )
        if self.reply_queue:
            self.reply_queue.push(msg)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def log_message(self, format, *args):
        logger.debug(f"[OcCallbackServer] {format % args}")


class OcChannelClient:
    """
    Manages bidirectional communication with OC via the oac-bridge channel.

    - Sends: HTTP POST to OC gateway's /webhook/oac-bridge
    - Receives: HTTP callback server on a local port
    """

    def __init__(
        self,
        gateway_url: str = "http://localhost:18789",
        webhook_path: str = "/webhook/oac-bridge",
        token: str = "",
        callback_port: int = 8011,
        callback_host: str = "0.0.0.0",
    ):
        self._gateway_url = gateway_url.rstrip("/")
        self._webhook_path = webhook_path
        self._token = token
        self._callback_port = callback_port
        self._callback_host = callback_host
        self._reply_queue = OcReplyQueue()
        self._server: Optional[HTTPServer] = None
        self._server_thread: Optional[threading.Thread] = None
        self._started = False

    @property
    def reply_queue(self) -> OcReplyQueue:
        return self._reply_queue

    @property
    def callback_url(self) -> str:
        return f"http://localhost:{self._callback_port}/oc-reply"

    def start(self) -> bool:
        """Start the callback HTTP server in a background thread."""
        if self._started:
            return True
        try:
            handler_class = type(
                "_OacCallbackHandler",
                (_CallbackHandler,),
                {
                    "reply_queue": self._reply_queue,
                    "expected_token": self._token,
                },
            )
            self._server = HTTPServer(
                (self._callback_host, self._callback_port), handler_class
            )
            self._server_thread = threading.Thread(
                target=self._server.serve_forever,
                daemon=True,
                name="oc-callback-server",
            )
            self._server_thread.start()
            self._started = True
            logger.info(
                f"[OcChannelClient] Callback server started on "
                f"{self._callback_host}:{self._callback_port}"
            )
            return True
        except Exception as e:
            logger.error(f"[OcChannelClient] Failed to start callback server: {e}")
            return False

    def stop(self):
        if self._server:
            self._server.shutdown()
            self._server = None
        self._started = False
        logger.info("[OcChannelClient] Callback server stopped")

    def send_message(
        self,
        oac_session_id: str,
        text: str,
        sender_name: str = "OAC User",
        timeout: float = 10.0,
    ) -> Dict[str, Any]:
        """Send a message to OC via the oac-bridge webhook."""
        url = f"{self._gateway_url}{self._webhook_path}"
        headers = {"Content-Type": "application/json"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        payload = {
            "oac_session_id": oac_session_id,
            "text": text,
            "sender_name": sender_name,
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            logger.error(f"[OcChannelClient] send_message failed: {e}")
            return {"error": str(e)}

    def send_and_wait(
        self,
        oac_session_id: str,
        text: str,
        sender_name: str = "OAC User",
        wait_timeout: float = 60.0,
    ) -> Optional[str]:
        """Send a message and wait for the reply."""
        result = self.send_message(oac_session_id, text, sender_name)
        if "error" in result:
            return None

        reply = self._reply_queue.wait_for_reply(oac_session_id, timeout=wait_timeout)
        return reply.text if reply else None
