FROM python:3.10

# Set environment variables
ENV SECRET_KEY "flytospace"
ENV DB_URL "sqlite+aiosqlite:///test.db"
ENV DEV_MODE "True"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

# Install dependencies
COPY /requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code/

EXPOSE 8000