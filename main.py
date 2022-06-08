from fastapi import FastAPI

from routers.collections import collection_router
from routers.courses import course_router
from schemas.user import UserCreate, UserRead, UserUpdate
from utilities.fastapi_users.users import auth_backend, fastapi_users
from routers.ships import ship_router

import aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import sys

from config import config

# # This allows us to do further json serialization when traversing down our course_json schema. Default is 1000
# sys.setrecursionlimit(10000)


app = FastAPI(
    title=config.TITLE,
    description=config.DESCRIPTION,
    version="0.1.0",
    license_info={
        "name": "AGPLv3",
        "url": "https://www.gnu.org/licenses/agpl-3.0.en.html"
    }
)

# Adding the various Fastapi-User routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Adding the ship routes
app.include_router(
    ship_router
)

# Adding the course routes
app.include_router(
    course_router
)

# Adding the collection routes
app.include_router(
    collection_router
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(config.REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
