FROM python:3.7

COPY . .

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8888

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]