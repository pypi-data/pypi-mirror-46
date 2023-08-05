import gzip
import io
import json
import logging

import certifi
import urllib3

from .asyncrecorder import AsyncRecorder
from ..formatters.dict import DictFormatter

logger = logging.getLogger(__name__)


class HTTPRecorder(AsyncRecorder):
    def __init__(self, api_key, api_endpoint, metadata=None, **kwargs):
        super(HTTPRecorder, self).__init__(**kwargs)
        self._api_key = api_key
        self._ingest_endpoint = "%s/%s" % (api_endpoint, 'api/agent/ingest')
        self.metadata = metadata or {}
        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    def flush(self, spans):
        payload = {
            "metadata": self.metadata,
            "spans": [],
            "events": [],
        }

        # TODO: limit number of objects sent per request
        for span in spans:
            span_dict = DictFormatter.dumps(span)
            events = span_dict.pop('logs')
            payload['spans'].append(span_dict)
            for event in events:
                event['context'] = span_dict['context']
                payload['events'].append(event)
        self._send(payload)

    def _send(self, body):
        from .. import version
        payload_json = json.dumps(body, default=lambda value: str(value))
        logger.debug("uncompressed json payload size is %d bytes", len(payload_json))
        out = io.BytesIO()
        with gzip.GzipFile(fileobj=out, mode="wb") as f:
            f.write(payload_json.encode('utf-8'))
        payload_gzip = out.getvalue()
        logger.debug("compressed gzip payload size is %d bytes", len(payload_gzip))

        headers = {
            "User-Agent": "scope-agent-python/%s" % version,
            "Content-Type": "application/json",
            "X-Scope-ApiKey": self._api_key,
            "Content-Encoding": "gzip",
        }
        resp = self.http.request('POST', self._ingest_endpoint,
                                 headers=headers, body=payload_gzip,
                                 retries=10)
        logger.debug("response from server: %d %s", resp.status, resp.data)
