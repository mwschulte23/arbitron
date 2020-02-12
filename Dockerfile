FROM python:3.7

COPY . .

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 6379 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]