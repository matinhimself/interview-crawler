FROM python:3.9.7

EXPOSE 5000

WORKDIR /app

COPY ./requirements.txt .

RUN apt-get update

RUN pip install -r requirements.txt

COPY ./.env .env

COPY .. /app

#ENTRYPOINT ["python3" , "-m", "flask"]
ENTRYPOINT ["python3" , "api/app.py"]