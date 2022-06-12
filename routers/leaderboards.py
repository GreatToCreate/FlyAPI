from fastapi import Depends, APIRouter, Query
from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy import text

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache.decorator import cache

from database.database import get_async_session
from schemas.leaderboard import Leader as SchemaLeader, TopScore as SchemaTopScore

leaderboard_router = APIRouter()


@leaderboard_router.get("/leaderboards/", response_model=list[SchemaTopScore], status_code=200, tags=["leaderboards"])
@cache(expire=30)
async def get_leaderboards(request: Request,
                           response: Response,
                           session: AsyncSession = Depends(get_async_session)):

    result = await session.execute(
        """SELECT ts.course, ts.steam_id, ts.time, t.points
            FROM (
                SELECT course, MAX(points) AS points 
                FROM top_score
                WHERE timestamp = (SELECT MAX(timestamp) FROM top_score)
                GROUP BY course
            ) t JOIN top_score ts ON ts.course = t.course AND t.points = ts.points"""
    )

    top_scores = result.all()

    return [SchemaTopScore.from_orm(ts) for ts in top_scores]


@leaderboard_router.get("/leaderboards/{course_name}", response_model=list[SchemaTopScore], status_code=200, tags=["leaderboards"])
@cache(expire=30)
async def get_leaderboard_by_name(request: Request,
                           response: Response,
                           course_name: str | None = None,
                           session: AsyncSession = Depends(get_async_session)):
    if course_name is not None:
        stmt = text("SELECT course, rank, steam_id, time, points FROM top_score ts WHERE timestamp = (SELECT MAX(timestamp) FROM top_score) AND course = :c ORDER BY points desc limit 20")
        result = await session.execute(stmt, {"c": course_name})

    top_scores = result.all()

    return [SchemaTopScore.from_orm(ts) for ts in top_scores]



@leaderboard_router.get("/leaders/", response_model=list[SchemaLeader], status_code=200, tags=["leaderboards"])
@cache(expire=30)
async def get_top_players(request: Request,
                          response: Response,
                          session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        """SELECT steam_username, points from leader where timestamp = (SELECT MAX(timestamp) FROM leader)"""
    )
    leaders = result.all()

    return [SchemaLeader.from_orm(leader) for leader in leaders]

