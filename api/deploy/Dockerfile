FROM python:3.9.7

EXPOSE 5000

WORKDIR /app

RUN echo $(ls)
COPY ./requirements.txt .
COPY ./staging.env .env

RUN apt-get update

RUN pip install -r requirements.txt

COPY .. /app

#ENTRYPOINT ["python3" , "-m", "flask"]
ENTRYPOINT ["python3" , "api/app.py"]