# Architecture  
The point of this file is to help new users become more easily acquainted with the tooling and concepts used within this project.  
  
## Language  
The FlyAPI REST-style service is written using the [Python](https://www.python.org/) (v3.10) programming language  
  
## API Framework  
[FastAPI](https://fastapi.tiangolo.com/) is an opinionated Python framework for creating performant asynchronous web services running on the [ASGI](https://asgi.readthedocs.io/en/latest/) web server [Uvicorn](https://www.uvicorn.org/). It heavily leans on libraries like SQLAlchemy (to define and use relational database objects) and Pydantic (to validate entered data by the user and to generate explicit and helpful documentation at the ip:port/docs endpoint).  
  
## SQLAlchemy  
[SQLAlchemy](https://www.sqlalchemy.org/) allows us to [define our relational database objects](https://docs.sqlalchemy.org/en/14/orm/quickstart.html#declare-models) using python code. This allows us to create/read/update/delete these objects in a pythonic way as opposed to interacting with the database by creating the sql statements ourselves (SQLAlchemy's session object will monitor changes we make to our python database-representation objects and then generate those SQL statements for us). By explicitly defining our database objects in code, we are able to use database migration tools to ensure that our actual database tables are up-to-date with changes made to our local objects. If we've made changes to our objects that don't match the current state of the database, we can generate a new revision to update the structure of the database automatically).  
  
## Pydantic  
[Pydantic](https://pydantic-docs.helpmanual.io/) provides us data validation and enforces type checks at runtime. It's used within this project to define the structure of the request bodies for various endpoints (as well as ensuring that entered data is of the correct type/within validation parameters) as well as defining what the response body (if any) to be returned. These models also assist with the generation of the swagger documentation.  
  
## Alembic  
[Alembic](https://alembic.sqlalchemy.org/en/latest/) is the specific database migration tool we use to ensure that any changes to our models (defined using SQLAlchemy declarative mappings) are [tracked](https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment). When changing a model within the database.models.models.py file, we can then run the command: alembic revision --autogenerate -m "Some relevant comment" which will assess the changes to the model and [create a new revision](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) within the alembic/versions folder. This revision provide us with upgrade/downgrade scripts to alter the state of the database to reflect changes to our models. We can apply these upgrade scripts by running the command: alembic upgrade head.  
  
## Pytest  
[Pytest](https://docs.pytest.org/en/7.1.x/) is the python testing framework used to test various aspects of the FlyAPI codebase. All tests reside within the test/ module. Currently, tests are split into 2 primary groups.  
1. models: the tests within this directory are independent of the actual web service (FastAPI) and are tested to ensure that the various CRUD operations are valid and working for each database model. There are also some slightly more advanced tests used (specifically among collections) to ensure that the many-to-many relationship between Collections and Courses (associative table: collection_has_course) in the database are correctly being represented and functioning. The tests also ensure that the ORM functionality of SQLAlchemy is working as intended  
2. api: the tests within this directory are for testing the functionality of our actual web service. They are intended to cover the route groups (auth, users, ships, courses, and collections) and provide a variety of tests to make sure that common process flows (examples being: registering a user, creating a course as a user, creating a collection and course and then adding the course to the collection as a user). To create these requests, this project uses the httpx asynchronous requests library (very similar in syntax to requests if you're more familiar with that library) and makes various HTTP verb calls to our endpoints defined in the routers/ directory in the project root.  
  
### Additional Information  
Due to this project using asynchronous database connections and the nature of FastAPI's incredibly power dependency injection system, there is a LOT more complexity in setting up an environment capable of testing various components of the application. In order to create the ability to test, we define various [pytest.fixtures](https://docs.pytest.org/en/7.1.x/reference/fixtures.html#fixture) at test/conftest.py  

- event_loop(request): this fixture allows us to run tests with our async methods throughout the codebase
- session(): this fixture acts as our SQLAlchemy asynchronous session which allows us to interact with the database (e.g. the tests only in tests/models
- override_get_async_session(session) and app(override_get_async_session): these two fixtures work override the injected sqlalchemy session within our endpoint routes by changing the dependency injected to be our override_get_async_session() method instead of the usual get_async_session dependency.
- async_client(app): this fixture acts as our async testing client to allow us to finally test the endpoints defined by out FastAPI app.

  
  
## PostgreSQL  
[PostgreSQL](https://www.postgresql.org/) is the relational database system intended to be used  in the "production" [this repo is in its infancy with many changes still happening on the Fly Dangerous custom model definitions so this term is really more of a misnomer]. 

Of relevance to its use in this project is its support for named ENUM types (that are used for restricting certain select-list-type-values within our models). Its support for storing J[SON objects as either the JSON or JSONB data types](https://www.postgresql.org/docs/current/datatype-json.html) also gives us flexibility in storing/retrieving the direct object to be used for custom courses and ships directly within Fly Dangerous.

Finally, its data type support for [Test Search Types](https://www.postgresql.org/docs/current/datatype-textsearch.html) will be the future base of fuzzy search matching for get requests on various endpoints.
  
  
## Insomnia  
[Insomnia](https://insomnia.rest/) is a REST API testing program that can import the generated openapi.json from the swagger docs and intelligently create endpoint-testing-requests. It is currently used for manual process-flow testing (register a user, create a ship as a user, etc.) to add another layer of test-validation to ensure that the API is functioning correctly. In a future version, this will hopefully be directly integrated into github actions to provide integration-test functionality to ensure that any PR's pass through multiple layers of validation to enable a [CI/CD pipeline](https://www.redhat.com/en/topics/devops/what-cicd-pipeline) to the live instance of this API.
  
## Docker
[Docker](https://docs.docker.com/) is a containerization platform to simplify the process of developing, shipping, and running applications. It is currently used in this repository to allow users to quickly spin up instances of the service in a testing environment so that potential integrations are more easily and rapidly understood.

This project defines a Dockerfile at the project root which creates an environment from the base python:3.10 instance, declares some environmental variables to be used by the application, installs the application dependencies into the environment, and finally exposes the internal container port 8000 for future host-machine mapping.

The two docker-compose-{db}-test.yml files define application bundles to automatically create the environments needed for running the application.
1. postgres-test defines a postgres database service container to be used by the FlyAPI rest-style backend container.
2. sqlite-test defines just the FlyAPI rest-style backend container with an embedded SQLite database running in the same container.

# FastAPI Users
[FastAPI Users](https://fastapi-users.github.io/fastapi-users/10.0/) is the user registration and authentication system used within the project. It is largely unmodified from it's example code for minimum integration, but there is one distinct difference (with more to come) currently of note:
- Within utilities/fastapi_users/register_fastapi_user_custom you'll notice that a subclass of FastAPIUsers is defined that overrides the get_register_router() method. The only reason this was done was to extend the usefulness of error checking by adding an addition caught exception (IntegrityError for duplicate username).

The next steps of utilizing this module is  further work in utilities/fastapi_users/users.py to implement email verification, reset password functionality, and eventually steam oauth support.