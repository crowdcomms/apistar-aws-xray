import traceback
import logging

from apistar import http
from aws_xray_sdk.core.models import http as xray_http
from aws_xray_sdk.ext.util import construct_xray_header, calculate_segment_name, calculate_sampling_decision, \
    prepare_response_header

logger = logging.getLogger(__file__)


__all__ = ['AWSXrayEventHook']

class AWSXrayEventHook:

    def __init__(self, recorder):
        self._recorder = recorder

    def on_request(self,
                   host: http.Host,
                   headers: http.Headers,
                   method:http.Method,
                   path: http.Path,
                   url: http.URL):
        xray_header = construct_xray_header(headers)

        name = calculate_segment_name(host, self._recorder)
        
        sampling_req = {
            'host': host,
            'method': method,
            'path': path,
            'service': name,
        }

        sampling_decision = calculate_sampling_decision(
            trace_header=xray_header,
            recorder=self._recorder,
            sampling_req=sampling_req,
        )

        segment = self._recorder.begin_segment(
            name=name,
            traceid=xray_header.root,
            parent_id=xray_header.parent,
            sampling=sampling_decision
        )

        segment.save_origin_trace_header(xray_header)
        segment.put_http_meta(xray_http.URL, url)
        segment.put_http_meta(xray_http.METHOD, method)
        segment.put_http_meta(xray_http.USER_AGENT, headers.get('User-Agent'))

        client_ip = headers.get('X-Forwarded-For') or headers.get('HTTP_X_FORWARDED_FOR')
        if client_ip:
            segment.put_http_meta(xray_http.CLIENT_IP, client_ip)
            segment.put_http_meta(xray_http.X_FORWARDED_FOR, True)


    def on_response(self, response: http.Response, exc: Exception = None):
        segment = self._recorder.current_segment()
        segment.put_http_meta(xray_http.STATUS, response.status_code)

        origin_header = segment.get_origin_trace_header()
        resp_header_str = prepare_response_header(origin_header, segment)
        response.headers[xray_http.XRAY_HEADER] = resp_header_str

        cont_len = response.headers.get('Content-Length')
        if cont_len:
            segment.put_http_meta(xray_http.CONTENT_LENGTH, int(cont_len))
        self._recorder.end_segment()

    def on_error(self, exc: Exception = None):
        if not exc:
            return
        segment = self._recorder.current_segment()
        segment.put_http_meta(xray_http.STATUS, 500)
        stack = traceback.extract_stack(limit=self._recorder._max_trace_back)
        segment.add_exception(exc, stack)
        self._recorder.end_segment()
