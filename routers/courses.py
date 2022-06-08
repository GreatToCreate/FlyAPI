from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.exc import IntegrityError

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from fastapi_cache.decorator import cache

from database.database import User, get_async_session
from database.models.models import Course
from schemas.course import CourseIn as SchemaCourseIn, CourseRead as SchemaCourseRead, \
    CourseUpdate as SchemaCourseUpdate, CourseReadSimple as SchemaCourseReadSimple
from utilities.fastapi_users.users import current_active_user

course_router = APIRouter()


# ToDo consider refactoring out duplicated methods within routes- introduce DAL in large refactor?


@course_router.post("/courses/", response_model=SchemaCourseRead, status_code=201, tags=["courses"])
async def create_course(course: SchemaCourseIn,
                        session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_active_user)):
    try:
        db_course = Course(name=course.name,
                           author_id=user.id,
                           game_type=course.game_type,
                           difficulty=course.difficulty,
                           length=course.length,
                           description=course.description,
                           link=course.link,
                           course_json=course.course_json.dict())

        session.add(db_course)
        await session.commit()
        await session.refresh(db_course)
    except IntegrityError as _:
        raise HTTPException(status_code=409, detail=f"Course name already taken")
    return db_course.__dict__


@course_router.patch("/courses/id/{course_id}", status_code=204, tags=["courses"])
async def update_course_by_id(course_id: int,
                              course: SchemaCourseUpdate,
                              session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_active_user)):
    # Get the course if it exists
    result = await session.execute(select(Course).where(Course.id == course_id))
    db_course: Course = result.scalars().first()

    if db_course is None:
        raise HTTPException(status_code=404, detail=f"Course with id: {course_id} not found")

    if db_course.author_id != user.id:
        raise HTTPException(status_code=403,
                            detail=f"You: {User.username} are not the creator of course: {db_course.id}")

    for var, value in vars(course).items():
        if var != "course_json":
            setattr(db_course, var, value) if value else None
        elif var == "course_json":
            setattr(db_course, "course_json", course.course_json.dict())

    await session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@course_router.patch("/courses/name/{course_name}", status_code=204, tags=["courses"])
async def update_course_by_name(course_name: str,
                                course: SchemaCourseUpdate,
                                session: AsyncSession = Depends(get_async_session),
                                user: User = Depends(current_active_user)):
    # Get the course if it exists
    result = await session.execute(select(Course).where(Course.name == course_name))
    db_course: Course = result.scalars().first()

    if db_course is None:
        raise HTTPException(status_code=404, detail=f"Course with : {course_name} not found")

    if db_course.author_id != user.id:
        raise HTTPException(status_code=403,
                            detail=f"You: {User.username} are not the creator of course: {db_course.id}")

    for var, value in vars(course).items():
        if var != "course_json":
            setattr(db_course, var, value) if value else None
        elif var == "course_json":
            setattr(db_course, "course_json", course.course_json.dict())

    await session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@course_router.get("/courses/", response_model=list[SchemaCourseReadSimple], status_code=200, tags=["courses"])
@cache(expire=30)
async def get_courses(request: Request,
                      response: Response,
                      username: str | None = None,
                      offset: int = 0,
                      limit: int = Query(default=20, lte=50),
                      session: AsyncSession = Depends(get_async_session)):
    if username is None:
        stmt = select(Course).offset(offset).limit(limit)
    elif username is not None:
        user_result = await session.execute(select(User).where(User.username == username))
        user = user_result.scalars().first()

        if user is None:
            raise HTTPException(status_code=404,
                                detail=f"Can't search for ship by {username} because: {username} doesn't exist")

        stmt = select(Course).where(Course.author_id == user.id).offset(offset).limit(limit)

    result = await session.execute(stmt)
    courses = result.scalars().all()

    return [SchemaCourseReadSimple.from_orm(course).dict() for course in courses]


@course_router.get("/courses/name/{course_name}", response_model=SchemaCourseRead, status_code=200, tags=["courses"])
@cache(expire=30)
async def get_course_by_name(course_name: str,
                             session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Course).where(Course.name == course_name))
    course = result.scalars().first()

    if course is None:
        raise HTTPException(status_code=404, detail=f"Course: {course_name} not found")

    return SchemaCourseRead.from_orm(course).dict()


@course_router.get("/courses/id/{course_id}", response_model=SchemaCourseRead, status_code=200, tags=["courses"])
@cache(expire=30)
async def get_course_by_id(course_id: int,
                           session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()

    if course is None:
        raise HTTPException(status_code=404, detail=f"Course id: {course_id} not found")

    return SchemaCourseRead.from_orm(course).dict()


@course_router.delete("/courses/id/{course_id}", status_code=204, tags=["courses"])
async def delete_course_by_id(course_id: int,
                              session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_active_user)):
    result = await session.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()

    if course is None:
        raise HTTPException(status_code=404, detail=f"Course id: {course_id} not found")

    if course.author_id != user.id:
        raise HTTPException(status_code=403,
                            detail=f"You: {User.username} are not the creator of course: {course.name}")
    await session.delete(course)
    await session.commit()

    return Response(status_code=HTTP_204_NO_CONTENT)
