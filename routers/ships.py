from fastapi import Depends, HTTPException, APIRouter, Query
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from sqlalchemy.exc import IntegrityError

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_cache.decorator import cache

from database.database import User, get_async_session
from database.models.models import Ship
from schemas.ship import ShipIn as SchemaShipIn, ShipRead as SchemaShipRead, ShipUpdate as SchemaShipUpdate
from utilities.fastapi_users.users import current_active_user

ship_router = APIRouter()


# ToDo consider refactoring out duplicated methods within routes- introduce DAL in large refactor?


@ship_router.post("/ships/", response_model=SchemaShipRead, status_code=201, tags=["ships"])
async def create_ship(ship: SchemaShipIn,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):
    try:
        db_ship = Ship(name=ship.name,
                       author_id=user.id,
                       description=ship.description,
                       ship_json=ship.ship_json.dict())

        session.add(db_ship)
        await session.commit()
        await session.refresh(db_ship)
    except IntegrityError as _:
        raise HTTPException(status_code=409, detail=f"Ship name: {ship.name} already taken")

    return db_ship.__dict__


@ship_router.patch("/ships/id/{ship_id}", status_code=204, tags=["ships"])
async def update_ship_by_id(ship_id: int,
                            ship: SchemaShipUpdate,
                            session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(current_active_user)):
    # Get the ship if it exists
    result = await session.execute(select(Ship).where(Ship.id == ship_id))
    db_ship: Ship = result.scalars().first()

    if db_ship is None:
        raise HTTPException(status_code=404, detail=f"Ship with id: {ship_id} not found")

    if db_ship.author_id != user.id:
        raise HTTPException(status_code=403,
                            detail=f"You: {User.username} are not the creator of ship: {db_ship.id}")

    for var, value in vars(ship).items():
        if var != "ship_json":
            setattr(db_ship, var, value) if value else None
        elif var == "ship_json":
            setattr(db_ship, "ship_json", ship.ship_json.dict())

    await session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@ship_router.patch("/ships/name/{ship_name}", status_code=204, tags=["ships"])
async def update_ship_by_name(ship_name: str,
                              ship: SchemaShipUpdate,
                              session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_active_user)):
    # Get the ship if it exists
    result = await session.execute(select(Ship).where(Ship.name == ship_name))
    db_ship: Ship = result.scalars().first()

    if db_ship is None:
        raise HTTPException(status_code=404, detail=f"Ship with id: {ship_name} not found")

    if db_ship.author_id != user.id:
        raise HTTPException(status_code=403,
                            detail=f"You: {User.username} are not the creator of ship: {db_ship.id}")

    for var, value in vars(ship).items():
        if var != "ship_json":
            setattr(db_ship, var, value) if value else None
        elif var == "ship_json":
            setattr(db_ship, "ship_json", ship.ship_json.dict())

    await session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@ship_router.get("/ships/", response_model=list[SchemaShipRead], status_code=200, tags=["ships"])
@cache(expire=30)
async def get_ships(request: Request,
                    response: Response,
                    username: str | None = None,
                    offset: int = 0,
                    limit: int = Query(default=30, lte=50),
                    session: AsyncSession = Depends(get_async_session)):
    if username is None:
        stmt = select(Ship).offset(offset).limit(limit)
    elif username is not None:
        user_result = await session.execute(select(User).where(User.username == username))
        user = user_result.scalars().first()

        if user is None:
            raise HTTPException(status_code=404,
                                detail=f"Can't search for ship by {username} because: {username} doesn't exist")

        stmt = select(Ship).where(Ship.author_id == user.id).offset(offset).limit(limit)

    result = await session.execute(stmt)
    ships_db = result.scalars().all()

    return [SchemaShipRead.from_orm(ship).dict() for ship in ships_db]


@ship_router.get("/ships/name/{ship_name}", response_model=SchemaShipRead, status_code=200, tags=["ships"])
@cache(expire=30)
async def get_ship_by_name(ship_name: str,
                           request: Request,
                           response: Response,
                           session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Ship).where(Ship.name == ship_name))
    db_ship = result.scalars().first()

    if db_ship is None:
        raise HTTPException(status_code=404, detail=f"Ship: {ship_name} not found")
    return SchemaShipRead.from_orm(db_ship).dict()


@ship_router.get("/ships/id/{ship_id}", response_model=SchemaShipRead, status_code=200, tags=["ships"])
@cache(expire=30)
async def get_ship_by_id(ship_id: int,
                         request: Request,
                         response: Response,
                         session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Ship).where(Ship.id == ship_id))
    db_ship = result.scalars().first()

    if db_ship is None:
        raise HTTPException(status_code=404, detail=f"Ship id: {ship_id} not found")

    return SchemaShipRead.from_orm(db_ship).dict()


@ship_router.delete("/ships/id/{ship_id}", status_code=204, tags=["ships"])
async def delete_ship_by_id(ship_id: int,
                            session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(current_active_user)):
    result = await session.execute(select(Ship).where(Ship.id == ship_id))
    db_ship = result.scalars().first()

    if db_ship is None:
        raise HTTPException(status_code=404, detail=f"Ship id: {ship_id} not found")

    if db_ship.author_id != user.id:
        raise HTTPException(status_code=403,
                            detail=f"You: {User.username} are not the creator of ship: {db_ship.name}")
    await session.delete(db_ship)
    await session.commit()

    return Response(status_code=HTTP_204_NO_CONTENT)
