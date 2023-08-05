import gc
import logging
import sys
import threading
import time
import traceback
from typing import Dict, Mapping, List, Any, Callable

import objgraph
import pyramid.response
from pyramid.httpexceptions import HTTPException, exception_response

from c2cwsgiutils import _utils, auth, broadcast

CONFIG_KEY = 'c2c.debug_view_enabled'
ENV_KEY = 'C2C_DEBUG_VIEW_ENABLED'

LOG = logging.getLogger(__name__)


def _dump_stacks(request: pyramid.request.Request) -> List[Mapping[str, Any]]:
    auth.auth_view(request)
    result = broadcast.broadcast('c2c_dump_stacks', expect_answers=True)
    assert result is not None
    return _beautify_stacks(result)


def _beautify_stacks(source: List[Mapping[str, Any]]) -> List[Mapping[str, Any]]:
    """
    Group the identical stacks together along with a list of threads sporting them
    """
    results = []  # type: List[Mapping[str, Any]]
    for host_stacks in source:
        host_id = '%s/%d' % (host_stacks['hostname'], host_stacks['pid'])
        for thread, frames in host_stacks['threads'].items():
            full_id = host_id + '/' + thread
            for existing in results:
                if existing['frames'] == frames:
                    existing['threads'].append(full_id)
                    break
            else:
                results.append({
                    'frames': frames,
                    'threads': [full_id]
                })
    return results


def _dump_stacks_impl() -> Dict[str, Any]:
    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    threads = {}
    for thread_id, stack in sys._current_frames().items():  # pylint: disable=W0212
        frames = []
        for filename, lineno, name, line in traceback.extract_stack(stack):  # type: ignore
            cur = {
                'file': filename,
                'line': lineno,
                'function': name
            }
            if line:
                cur['code'] = line.strip()
            frames.append(cur)
        threads["%s(%d)" % (id2name.get(thread_id, ""), thread_id)] = frames
    return {
        'threads': threads
    }


def _dump_memory(request: pyramid.request.Request) -> List[Mapping[str, Any]]:
    auth.auth_view(request)
    limit = int(request.params.get('limit', '30'))
    result = broadcast.broadcast('c2c_dump_memory', params={'limit': limit}, expect_answers=True)
    assert result is not None
    return result


def _dump_memory_diff(request: pyramid.request.Request) -> List:
    auth.auth_view(request)
    limit = int(request.params.get('limit', '30'))
    if 'path' in request.matchdict:
        # deprecated
        path = '/' + '/'.join(request.matchdict['path'])
    else:
        path = request.params['path']

    sub_request = request.copy()
    split_path = path.split('?')
    sub_request.path_info = split_path[0]
    if len(split_path) > 1:
        sub_request.query_string = split_path[1]

    # warmup run
    try:
        request.invoke_subrequest(sub_request)
    except Exception:  # nosec
        pass

    LOG.debug("checking memory growth for %s", path)

    peak_stats = {}  # type: Dict
    for i in range(3):
        gc.collect(i)

    objgraph.growth(limit=limit, peak_stats=peak_stats, shortnames=False)

    response = None
    try:
        response = request.invoke_subrequest(sub_request)
        LOG.debug("response was %d", response.status_code)

    except HTTPException as ex:
        LOG.debug("response was %s", str(ex))

    del response

    for i in range(3):
        gc.collect(i)

    growth = objgraph.growth(limit=limit, peak_stats=peak_stats, shortnames=False)

    return growth


def _dump_memory_impl(limit: int) -> Mapping[str, Any]:
    nb_collected = [gc.collect(generation) for generation in range(3)]
    return {
        'nb_collected': nb_collected,
        'most_common_types': objgraph.most_common_types(limit=limit, shortnames=False),
        'leaking_objects': objgraph.most_common_types(limit=limit, shortnames=False,
                                                      objects=objgraph.get_leaking_objects())
    }


def _sleep(request: pyramid.request.Request) -> pyramid.response.Response:
    auth.auth_view(request)
    timeout = float(request.params['time'])
    time.sleep(timeout)
    request.response.status_code = 204
    return request.response


def _headers(request: pyramid.request.Request) -> Mapping[str, str]:
    auth.auth_view(request)
    return dict(request.headers)


def _error(request: pyramid.request.Request) -> Any:
    auth.auth_view(request)
    raise exception_response(int(request.params['status']), detail="Test")


def _add_view(config: pyramid.config.Configurator, name: str, path: str, view: Callable) -> None:
    config.add_route("c2c_debug_" + name, _utils.get_base_path(config) + r"/debug/" + path,
                     request_method="GET")
    config.add_view(view, route_name="c2c_debug_" + name, renderer="fast_json", http_cache=0)


def init(config: pyramid.config.Configurator) -> None:
    if auth.is_enabled(config, ENV_KEY, CONFIG_KEY):
        broadcast.subscribe('c2c_dump_memory', _dump_memory_impl)
        broadcast.subscribe('c2c_dump_stacks', _dump_stacks_impl)

        _add_view(config, "stacks", "stacks", _dump_stacks)
        _add_view(config, "memory", "memory", _dump_memory)
        _add_view(config, "memory_diff", "memory_diff", _dump_memory_diff)
        _add_view(config, "memory_diff_deprecated", "memory_diff/*path", _dump_memory_diff)
        _add_view(config, "sleep", "sleep", _sleep)
        _add_view(config, "headers", "headers", _headers)
        _add_view(config, "error", "error", _error)

        LOG.info("Enabled the /debug/... API")
