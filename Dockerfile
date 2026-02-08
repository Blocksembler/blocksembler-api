FROM python:3.12
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
COPY ./docker/entrypoint.sh /entrypoint.sh

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./alembic /code/alembic
COPY ./alembic.ini /code/alembic.ini

EXPOSE 80

# Use entrypoint
ENTRYPOINT ["/entrypoint.sh"]

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
