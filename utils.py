from contextlib import contextmanager

import grpc

@contextmanager
def default_error(context):
    try:
        yield
    except Exception as e:
        context.set_details(str(e))
        context.set_code(grpc.StatusCode.INTERNAL)
