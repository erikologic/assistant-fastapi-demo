from fastapi import FastAPI
from app.routes.heartbeat import router as heartbeat_router
from app.routes.assistance.router import router as assistance_router

app = FastAPI()

app.include_router(heartbeat_router)
app.include_router(assistance_router)

import os
import time

import structlog
from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.context import correlation_id
from fastapi import Request, Response
from pydantic import parse_obj_as
from uvicorn.protocols.utils import get_path_with_query_string

from app.custom_logging import setup_logging


LOG_JSON_FORMAT = parse_obj_as(bool, os.getenv("LOG_JSON_FORMAT", False))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
setup_logging(json_logs=LOG_JSON_FORMAT, log_level=LOG_LEVEL)

access_logger = structlog.stdlib.get_logger("api.access")


@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    structlog.contextvars.clear_contextvars()
    # These context vars will be added to all log entries emitted during the request
    request_id = correlation_id.get()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start_time = time.perf_counter_ns()
    # If the call_next raises an error, we still want to return our own 500 response,
    # so we can add headers to it (process time, request ID...)
    response = Response(status_code=500)
    try:
        response = await call_next(request)
    except Exception:
        # TODO: Validate that we don't swallow exceptions (unit test?)
        structlog.stdlib.get_logger("api.error").exception("Uncaught exception")
        raise
    finally:
        process_time = time.perf_counter_ns() - start_time
        status_code = response.status_code
        url = get_path_with_query_string(request.scope)
        client_host = request.client.host
        client_port = request.client.port
        http_method = request.method
        http_version = request.scope["http_version"]
        # Recreate the Uvicorn access log format, but add all parameters as structured information
        access_logger.info(
            f"""{client_host}:{client_port} - "{http_method} {url} HTTP/{http_version}" {status_code}""",
            http={
                "url": str(request.url),
                "status_code": status_code,
                "method": http_method,
                "request_id": request_id,
                "version": http_version,
            },
            network={"client": {"ip": client_host, "port": client_port}},
            duration=process_time,
        )
        response.headers["X-Process-Time"] = str(process_time / 10**9)
        return response


# This middleware must be placed after the logging, to populate the context with the request ID
# NOTE: Why last??
# Answer: middlewares are applied in the reverse order of when they are added (you can verify this
# by debugging `app.middleware_stack` and recursively drilling down the `app` property).
app.add_middleware(CorrelationIdMiddleware)

# # UGLY HACK
# # Datadog's `TraceMiddleware` is applied as the very first middleware in the list, by patching `FastAPI` constructor.
# # Unfortunately that means that it is the innermost middleware, so the trace/span are created last in the middleware
# # chain. Because we want to add the trace_id/span_id in the access log, we need to extract it from the middleware list,
# # put it back as the outermost middleware, and rebuild the middleware stack.
# # TODO: Open an issue in dd-trace-py to ask if it can change its initialization, or if there is an easy way to add the
# #       middleware manually, so we can add it later in the chain and have it be the outermost middleware.
# # TODO: Open an issue in Starlette to better explain the order of middlewares
# tracing_middleware = next(
#     (m for m in app.user_middleware if m.cls == TraceMiddleware), None
# )
# if tracing_middleware is not None:
#     app.user_middleware = [m for m in app.user_middleware if m.cls != TraceMiddleware]
#     structlog.stdlib.get_logger("api.datadog_patch").info(
#         "Patching Datadog tracing middleware to be the outermost middleware..."
#     )
#     app.user_middleware.insert(0, tracing_middleware)
#     app.middleware_stack = app.build_middleware_stack()
