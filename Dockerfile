FROM python:3.12.6 

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./tricount /app

CMD ["python", "manage.py", "runserver"]

