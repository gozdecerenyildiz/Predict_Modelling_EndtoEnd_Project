FROM python:3.11-slim-bullseye
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8080

CMD [ "uvicorn","main:app","--host=0.0.0.0", "--port=8080"]