# Architecture
The point of this file is to help new users become more easily acquainted with the tooling and concepts used within this project.

## Language
The FlyAPI REST-style service is written using the Python (v3.10) programming language

## API Framework
[FastAPI](https://fastapi.tiangolo.com/) is an opinionated Python framework for creating performant asynchronous web services running on the [ASGI](https://asgi.readthedocs.io/en/latest/) web server [Uvicorn](https://www.uvicorn.org/). It heavily leans on libraries like SQLAlchemy (to define and use relational database objects) and Pydantic (to validate entered data by the user and to generate explicit and helpful documentation at the ip:port/docs endpoint).

## SQLAlchemy
SQLAlchemy allows us to define our relational database objects using python code. This allows us to create/read/update/delete these objects in a pythonic way as opposed to interacting with the database by creating the sql statements ourselves (SQLAlchemy's session object will monitor changes we make to our python database-representation objects and then generate those SQL statements for us). By explicitly defining our database objects in code, we are able to use database migration tools to ensure that our actual database tables are up-to-date with changes made to our local objects. If we've made changes to our objects that don't match the current state of the database, we can generate a new revision to update the structure of the database automatically).

## Pydantic
Pydantic provides us data validation and enforces type checks at runtime. It's used within this project to define the structure of the request bodies for various endpoints (as well as ensuring that entered data is of the correct type/within validation parameters) as well as defining what the response body (if any) to be returned. These models also assist with the generation of documentation.

## Alembic
This is the specific database migration tool we use to ensure that any changes to our models (defined using SQLAlchemy declarative mappings) are tracked. When changing a model within the database.models.models.py file, we can then run the command: alembic revision --autogenerate -m "Some relevant comment" which will assess the changes to the model and create a new revision within the alembic/versions folder. This revision provide us with upgrade/downgrade scripts to alter the state of the database to reflect changes to our models. We can apply these upgrade scripts by running the command: alembic upgrade head.

## Pytest
This is the python testing framework used to test various aspects of the FlyAPI codebase. All tests reside within the test/ module. Currently, tests are split into 2 primary groups.
1. models: the tests within this directory are independent of the actual web service (FastAPI) and are tested to ensure that the various CRUD operations are valid and working for each database model. There are also some slightly more advanced tests used (specifically among collections) to ensure that the many-to-many relationship between Collections and Courses (associative table: collection_has_course) in the database are correctly being represented and functioning. The tests also ensure that the ORM functionality of SQLAlchemy is working as intended
2. api: the tests within this directory are for testing the functionality of our actual web service. They are intended to cover the route groups (auth, users, ships, courses, and collections) and provide a variety of tests to make sure that common process flows (examples being: registering a user, creating a course as a user, creating a collection and course and then adding the course to the collection as a user). To create these requests, this project uses the httpx asynchronous requests library (very similar in syntax to requests if you're more familiar with that library) and makes various HTTP verb calls to our endpoints defined in the routers/ directory in the project root.

### Additional Information
Due to this project using asynchronous database connections and the nature of FastAPI's incredibly power dependency injection system, there is a LOT more complexity in setting up an environment capable of testing various components of the application. In order to create the ability to test, we define various pytest.fixtures at test/conftest.py

Among them:


## PostgreSQL
This is the database intended to be used 


## Insomnia


## Docker