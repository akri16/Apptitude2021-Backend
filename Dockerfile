FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./docs.py /code/docs.py

COPY ./static /code/static

COPY ./app /code/app

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]
