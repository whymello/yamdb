FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

# CMD ["python3", "manage.py", "runserver", "0:8000"]
CMD ["gunicorn", "yamdb.wsgi:application", "--bind", "0.0.0.0:8000"]
