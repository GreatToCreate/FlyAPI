import hashlib
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response


def custom_key_builder(
    func,
    namespace: Optional[str] = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
):
    from fastapi_cache import FastAPICache

    ignored_arg_types = [AsyncSession, Request, Response]

    args = [arg for arg in args if type(arg) not in ignored_arg_types]


    prefix = f"{FastAPICache.get_prefix()}:{namespace}:"
    cache_key = (
        prefix
        + hashlib.md5(  # nosec:B303
            f"{func.__module__}:{func.__name__}:{args}".encode()
        ).hexdigest()
    )
    return cache_key