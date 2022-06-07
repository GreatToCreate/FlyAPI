from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.exc import IntegrityError

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from database.database import User, get_async_session
from database.models.models import Course, Collection
from schemas.collection import CollectionIn as SchemaCollectionIn, CollectionRead as SchemaCollectionRead, \
    CollectionUpdate as SchemaCollectionUpdate
from utilities.fastapi_users.users import current_active_user

collection_router = APIRouter()


# ToDo consider refactoring out duplicated methods within routes- introduce DAL in large refactor?


@collection_router.post("/collections/", response_model=SchemaCollectionRead, status_code=201, tags=["collections"])
async def create_collection(collection: SchemaCollectionIn,
                            session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(current_active_user)):
    try:
        collection = Collection(name=collection.name,
                                description=collection.description,
                                author_id=user.id)

        session.add(collection)
        await session.commit()
        await session.refresh(collection)
    except IntegrityError as _:
        raise HTTPException(status_code=409, detail=f"Collection name already taken")
    return collection.__dict__


@collection_router.patch("/collections/id/{collection_id}", status_code=204, tags=["collections"])
async def update_collection_by_id(collection_id: int,
                                  collection: SchemaCollectionUpdate | None = None,
                                  courses_to_add_by_id: list[int] | None = None,
                                  courses_to_remove_by_id: list[int] | None = None,
                                  courses_to_add_by_name: list[str] | None = None,
                                  courses_to_remove_by_name: list[str] | None = None,
                                  session: AsyncSession = Depends(get_async_session),
                                  user: User = Depends(current_active_user)):
    # Get the collection
    result = await session.execute(select(Collection).where(Collection.id == collection_id))
    db_collection: Collection = result.scalars().first()

    if db_collection is None:
        raise HTTPException(status_code=404, detail=f"Collection with id: {collection_id} not found")

    if db_collection.author_id != user.id:
        raise HTTPException(status_code=403,
                            detail=f"You: {User.username} are not the creator of collection: {db_collection.id}")

    if courses_to_add_by_id is not None:
        course_result = await session.execute(select(Course).where(Course.id.in_(tuple(courses_to_add_by_id))))
        courses = course_result.scalars().all()

        for course in courses:
            db_collection.courses.append(course)

        # for course_id in courses_to_add_by_id
        # course_result = await session.execute(select(Course).where(Course.id == course_id))
        # course = course_result.scalars().first()
        # if course is not None:
        #     db_collection.courses.append(course)
        # elif course is None:
        #     session.rollback()
        #     raise HTTPException(status_code=404, detail=f"Course with id: {course_id} not found. Transaction "
        #                                                 f"rolled back to pre-patch state.")

    if courses_to_remove_by_id is not None:
        course_result = await session.execute(select(Course).where(Course.id.in_(tuple(courses_to_remove_by_id))))
        courses = course_result.scalars().all()

        for course in courses:
            db_collection.courses.remove(course)

        # for course_id in courses_to_remove_by_id:
        # course_result = await session.execute(select(Course).where(Course.id == course_id))
        # course = course_result.scalars().first()
        #
        # if course is not None:
        #     db_collection.courses.remove(course)
        # elif course is None:
        #     raise HTTPException(status_code=404, detail=f"Course with id: {course_id} not found. Transaction "
        #                                                 f"rolled back to pre-patch state.")

    if courses_to_add_by_name is not None:
        course_result = await session.execute(select(Course).where(Course.name.in_(tuple(courses_to_add_by_name))))
        courses = course_result.scalars().all()

        for course in courses:
            db_collection.courses.append(course)

    if courses_to_remove_by_name is not None:
        course_result = await session.execute(select(Course).where(Course.name.in_(tuple(courses_to_remove_by_name))))
        courses = course_result.scalars().all()

        for course in courses:
            db_collection.courses.remove(course)

    if collection is not None:
        for var, value in vars(collection).items():
            setattr(db_collection, var, value)

    await session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@collection_router.get("/collections/", response_model=list[SchemaCollectionRead], status_code=200,
                       tags=["collections"])
async def get_collections(username: str | None = None,
                          offset: int = 0,
                          limit: int = Query(default=20, lte=30),
                          session: AsyncSession = Depends(get_async_session)):
    if username is None:
        stmt = select(Collection).offset(offset).limit(limit)
    elif username is not None:
        user_result = await session.execute(select(User).where(User.username == username))
        user = user_result.scalars().first()

        if user is None:
            raise HTTPException(status_code=404,
                                detail=f"Can't search for ship by {username} because: {username} doesn't exist")

        stmt = select(Collection).where(Collection.author_id == user.id).offset(offset).limit(limit)

    result = await session.execute(stmt)
    collections = result.scalars().unique()

    return [collection.__dict__ for collection in collections]


@collection_router.get("/collections/name/{collection_name}", response_model=SchemaCollectionRead, status_code=200,
                       tags=["collections"])
async def get_collection_by_name(collection_name: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Collection).where(Collection.name == collection_name))
    collection = result.scalars().first()

    if collection is None:
        raise HTTPException(status_code=404, detail=f"Course: {collection_name} not found")

    return collection.__dict__


@collection_router.get("/collections/id/{collection_id}", response_model=SchemaCollectionRead, status_code=200,
                       tags=["collections"])
async def get_collection_by_id(collection_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Collection).where(Collection.id == collection_id))
    collection = result.scalars().first()

    if collection is None:
        raise HTTPException(status_code=404, detail=f"Course id: {collection_id} not found")

    return collection.__dict__


@collection_router.patch("/collections/id/{collection_id}/id/{course_id}", response_model=SchemaCollectionRead,
                         status_code=201,
                         tags=["collections"])
async def add_course_to_collection_by_ids(collection_id: int, course_id: int,
                                          session: AsyncSession = Depends(get_async_session),
                                          user: User = Depends(current_active_user)):
    # Step one, verify that the current user is the creator of the collection
    collection_result = await session.execute(select(Collection).where(Collection.id == collection_id))
    collection = collection_result.scalars().first()

    # Check to make sure the collection exists
    if collection is None:
        raise HTTPException(status_code=404, detail=f"Collection with id: {collection_id} not found")

    # Check to make sure the course exists
    course_result = await session.execute(select(Course).where(Course.id == course_id))
    course = course_result.scalars().first()

    if course is None:
        raise HTTPException(status_code=404, detail=f"Course with id: {course_id} not found")

    # Ensuring that the user requesting to add a course is the creator of the collection
    if collection.author_id != user.id:
        raise HTTPException(status_code=403,
                            detail=f"You: {User.username} are not the creator of collection: {collection.name}")

    # Adding the course to the collection
    collection.courses.append(course)
    await session.commit()
    await session.refresh(collection)

    return collection.__dict__


@collection_router.patch("/collections/id/{collection_id}/name/{course_name}", response_model=SchemaCollectionRead,
                         status_code=201,
                         tags=["collections"])
async def add_course_to_collection_by_course_name(collection_id: int, course_name: str,
                                                  session: AsyncSession = Depends(get_async_session),
                                                  user: User = Depends(current_active_user)):
    # Step one, verify that the current user is the creator of the collection
    collection_result = await session.execute(select(Collection).where(Collection.id == collection_id))
    collection = collection_result.scalars().first()

    # Check to make sure the collection exists
    if collection is None:
        raise HTTPException(status_code=404, detail=f"Collection with id: {collection_id} not found")

    # Check to make sure the course exists
    course_result = await session.execute(select(Course).where(Course.name == course_name))
    course = course_result.scalars().first()

    if course is None:
        raise HTTPException(status_code=404, detail=f"Course with name: {course_name} not found")

    # Ensuring that the user requesting to add a course is the creator of the collection
    if collection.author_id != user.id:
        raise HTTPException(status_code=403,
                            detail=f"You: {User.username} are not the creator of collection: {collection.name}")

    # Adding the course to the collection
    collection.courses.append(course)
    await session.commit()
    await session.refresh(collection)

    return collection.__dict__


@collection_router.patch("/collections/name/{collection_name}/name/{course_name}", response_model=SchemaCollectionRead,
                         status_code=201,
                         tags=["collections"])
async def add_course_to_collection_by_names(collection_name: str, course_name: str,
                                            session: AsyncSession = Depends(get_async_session),
                                            user: User = Depends(current_active_user)):
    # Step one, verify that the current user is the creator of the collection
    collection_result = await session.execute(select(Collection).where(Collection.name == collection_name))
    collection = collection_result.scalars().first()

    # Check to make sure the collection exists
    if collection is None:
        raise HTTPException(status_code=404, detail=f"Collection with name: {collection_name} not found")

    # Check to make sure the course exists
    course_result = await session.execute(select(Course).where(Course.name == course_name))
    course = course_result.scalars().first()

    if course is None:
        raise HTTPException(status_code=404, detail=f"Course with name: {course_name} not found")

    # Ensuring that the user requesting to add a course is the creator of the collection
    if collection.author_id != user.id:
        raise HTTPException(status_code=403,
                            detail=f"You: {User.username} are not the creator of collection: {collection.name}")

    # Adding the course to the collection
    collection.courses.append(course)
    await session.commit()
    await session.refresh(collection)

    return collection.__dict__


@collection_router.delete("/collections/id/{collection_id}", status_code=204, tags=["collections"])
async def delete_course_by_id(collection_id: int,
                              session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_active_user)):
    result = await session.execute(select(Collection).where(Collection.id == collection_id))
    collection = result.scalars().first()

    if collection is None:
        raise HTTPException(status_code=404, detail=f"Collection id: {collection_id} not found")

    if collection.author_id != user.id:
        raise HTTPException(status_code=403,
                            detail=f"You: {User.username} are not the creator of collection: {collection.name}")
    await session.delete(collection)
    await session.commit()

    return Response(status_code=HTTP_204_NO_CONTENT)
