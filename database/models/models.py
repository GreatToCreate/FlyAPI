from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, JSON, Table
from sqlalchemy.orm import relationship
from database.database import Base


# Consider breaking these out into their own files
# Argument for: readability of the codebase

# Argument against: seemingly unnecessary as this file is easily searchable and won't ever contain many more models
# than what currently exist (this might be a bad assumption but I really doubt it)


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    User sqlalchemy ORM user model inhering from the fastapi-user model with the extended columns in the fields below
    """
    __tablename__ = "user"
    username = Column(String(20), unique=True, nullable=False)
    steam_id = Column(String, nullable=True)
    steam_username = Column(String, nullable=True)
    courses = relationship("Course", back_populates="author", lazy="select")
    ships = relationship("Ship", back_populates="author", lazy="select")
    collections = relationship("Collection", back_populates="author", lazy="select")


class Ship(Base):
    """
    Ship sqlalchemy ORM model. Mostly metadata for filtering on searches but also containing the actual JSON the game
    expects to serialize
    """
    __tablename__ = "ship"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True, index=True)
    author_id = Column(ForeignKey("user.id"), nullable=True)
    description = Column(String(), nullable=False)
    # The actual ship JSON that is serialized by Fly Dangerous
    ship_json = Column(JSON, nullable=False)
    author = relationship("User", back_populates="ships", lazy="select")


# Associative table allow us to backfill all courses in a collection and all collection with a course
collection_has_course = Table(
    "collection_has_course",
    Base.metadata,
    Column("collection_id", ForeignKey("collection.id"), primary_key=True),
    Column("course_id", ForeignKey("course.id"), primary_key=True)
)


class Course(Base):
    """
    Course sqlalchemy ORM model. Mostly metadata for filtering on searches and containing the actual JSON the game
    expects to serialize
    """
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    # MetaData describing a course
    name = Column(String(20), unique=True, nullable=False, index=True)
    author_id = Column(ForeignKey("user.id"), nullable=True)
    author = relationship("User", back_populates="courses", lazy="select")
    collections = relationship("Collection", secondary=collection_has_course, back_populates="courses")
    game_type = Column(Enum("Free Roam", "Time Trial", "Sprint", "Laps", "Hoon Attack", "Training", name="game_types"),
                       nullable=False)
    difficulty = Column(Enum("Easy", "Medium", "Hard", "Dangerous", name="difficulty_types"), nullable=False)
    length = Column(Enum("Short", "Medium", "Long", "Endurance", name="length_types"), nullable=False)
    description = Column(String, nullable=False)
    link = Column(String, nullable=True)
    # The actual JSON that is serialized into a track by Fly Dangerous
    course_json = Column(JSON, nullable=False)


class Collection(Base):
    """
    Collection sqlalchemy ORM model
    """
    __tablename__ = "collection"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    author_id = Column(ForeignKey("user.id"), nullable=True)
    author = relationship("User", back_populates="collections", lazy="select")
    description = Column(String, nullable=False)
    # joined is the strategy we have to use for courses as it pre-fetches the data so that we don't run into async
    # errors relating to lazy select
    courses = relationship("Course", secondary=collection_has_course, back_populates="collections", lazy="joined")


class CourseHasRating(Base):
    """
    Ship sqlalchemy ORM model. Mostly metadata for filtering on searches but also containing the actual JSON the game
    expects to serialize
    """
    __tablename__ = "course_has_rating"
    course_id = Column("course_id", ForeignKey("course.id"), primary_key=True)
    user_id = Column("user_id", ForeignKey("user.id"), primary_key=True)
    rating = Column("rating", Integer, nullable=True)


class ShipHasRating(Base):
    """
    Ship sqlalchemy ORM model. Mostly metadata for filtering on searches but also containing the actual JSON the game
    expects to serialize
    """
    __tablename__ = "ship_has_rating"
    ship_id = Column("ship_id", ForeignKey("ship.id"), primary_key=True)
    user_id = Column("user_id", ForeignKey("user.id"), primary_key=True)
    rating = Column("rating", Integer, nullable=True)


class CollectionHasRating(Base):
    """
    Ship sqlalchemy ORM model. Mostly metadata for filtering on searches but also containing the actual JSON the game
    expects to serialize
    """
    __tablename__ = "collection_has_rating"
    collection_id = Column("collection_id", ForeignKey("collection.id"), primary_key=True)
    user_id = Column("user_id", ForeignKey("user.id"), primary_key=True)
    rating = Column("rating", Integer, nullable=True)