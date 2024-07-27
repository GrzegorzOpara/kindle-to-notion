FROM python:3.12.4-alpine3.20
WORKDIR /
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
EXPOSE 8080 
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]