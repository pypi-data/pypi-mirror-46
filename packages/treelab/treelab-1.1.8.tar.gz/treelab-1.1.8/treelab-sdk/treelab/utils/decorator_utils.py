import asyncio
import time
from functools import wraps
from sys import version_info

import grpc
from rx import Observable

from treelab.rxmq.rxmq import Rxmq


def async_run(fn):
    """
    Wrapper that makes async run (the developers' lives as well) easier
    :param fn:
    :return:
    """
    
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if version_info.major == 3:
            if version_info.minor >= 7:
                return asyncio.run(fn(*args, **kwargs))
            else:
                loop = asyncio.get_event_loop()
                return loop.run_until_complete(fn(*args, **kwargs))
        else:
            raise ValueError("Python 2 is not currently supported")
    
    return wrapped


def wait(event_name):
    """
    Wrapper for taking care of asynchronous grpc calls
    """
    
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, workspace_id=None, wait_till_complete=True, name_spaces=None):
            if not name_spaces:
                name_spaces = []
            grpc_api, grpc_input, meta_data = fn(*args)
            fn_name = fn.__name__
            if wait_till_complete:
                response = grpc_api(grpc_input, metadata=meta_data)
                
                if not workspace_id and fn_name == "create_workspace":
                    workspace_id = response.id
                elif fn_name == "add_table" or fn_name == "add_core":
                    name_spaces.append(response.id)
                
                complete_event_name = '.'.join(name_spaces + [event_name])
                if fn_name != 'create_workspace':
                    _wait_for_first_event(workspace_id, complete_event_name)
                else:
                    time.sleep(0.1)
                return response
            else:
                future: grpc.Future = grpc_api.future(grpc_input)
                return future
        
        return wrapper
    
    return decorator


def _observe_event(workspace_id: str, event_name: str) -> Observable:
    return Rxmq.channel(workspace_id).observe(event_name)


def _wait_for_first_event(workspace_id: str, event_name: str) -> Observable:
    """
    Listening for the first event with topic under workspace with workspace_id
    :param workspace_id:
    :param topic:
    :return:
    """
    return _observe_event(workspace_id, event_name)
