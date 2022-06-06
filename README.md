# FlyAPI

**Fly API** is a REST-style API written in Python using the [FastAPI](https://fastapi.tiangolo.com/) framework. It's purpose is to act as a [backend service](https://en.wikipedia.org/wiki/API#Web_APIs) to facilitate the sharing of custom courses and ships (both defined as **JSON** files) for the GPLv3 [open-source](https://github.com/jukibom/FlyDangerous) game [Fly Dangerous](https://store.steampowered.com/app/1781750/Fly_Dangerous/). 


## Setting up the Project

1. Clone or download this repository locally
2. Create a [virtual environment](https://docs.python.org/3/library/venv.html) to install dependencies into
3. Activate your virtual environment and install dependencies using pip install -r requirements.txt from the project root

## Running the Project

1. Environmental variables to set:
	- SECRET_KEY a secure string used to encode JWTs. Defaults to: flytospace **IF YOU DON'T CHANGE THIS IN PRODUCTION YOU ARE EXPOSING YOUR APPLICATION TO ATTACKS**
	- DB_URL the database url used for creation the [SQLAlchemy async session](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html). The project was created with support for [SQLite](https://www.sqlite.org/index.html) and [PostgreSQL](https://www.postgresql.org/) in mind, but others may work as well. Check the SQLAlchemy docs and verify that all models (database/models/models.py) will work with your preferred database technology: Defaults to: sqlite+aiosqlite:///test.db
	- DEV_MODE a string (True or False) that is parsed into a boolean determining whether verbose SQL queries should be printed out into the console (for debugging purposes)

2. Now that you've set these variables, apply the [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) database migration by running the following command at the project root: alembic upgrade head
3. With the database tables created from the previous step, you're now ready to run FlyAPI. Ensure that your virtual environment has been activated and run the following command at the project root: python -m uvicorn main:app --reload (or without --reload if in a production environment)

## Running the Tests
1. Activate the virtual environment you've made for this project
2. Run the following command at the project root: pytest

## Understanding the Project
Check out the ARCHITECTURE.md file within the project's root