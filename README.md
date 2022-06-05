## Crawler

Scrapes companies esg scores from [refinitiv.com](https://www.refinitiv.com/en/sustainable-finance/esg-scores) and
stores them into a mongodb database.

```
cd crawler

virtualenv venv
source mypython/bin/activate

cp .env.sample .env
# replace .env content with ur mongodb config

pip install -r requirements.txt

python3 crawler.py
```

## Api

### Run api service using docker compose

```
   cp .env.sample .env
   
   docker-compose up flask
```

## usage

since there are only two endpoints, I didn't document it using any standard api documentation tools (i.e swagger and
...)

### - companies api

| endpoint | description | result |
|----|----|---|
| /api/corps | returns list of names and ids of all companies | [...{"name":"Aliens","_id": "ALI"},...]
| /api/corps/`<query>` | returns list of names and ids of companies whose name matches `<query>` | [...{"name":"Alien", "_id","ALI"},...]
|/api/corps/esgscore/`<id>`| returns scores of company with id `<id>` |  below |

```
  {"_id": "ALQ.AX", 
  "environmentScore": 59, 
  "esgScore": 77, 
  "governanceScore": 88, 
  "industryType": "Professional & Commercial Services", 
  "name": "ALS Ltd", 
  "rank": "27", 
  "socialScore": 78, 
  "totalIndustries": "444" 
} 
```


### suggestions/problem to implement/fix 

- better api documentation using swagger
- currently project is using flasks builtin webserver that is not a production ready solution
- crawler and api are using same db package repository having different domains
- better config solutions instead of a simple .env file
- the api authentication is missing its logic due to simplicity of testing process
- the website is behind cloudfront cdn so there is a chance that its ddos protection ip-ban crawler. but because of limited amount of data (10,000 in total), it can be prevented by just delaying requests. by default it does more than 40 requests per second on 8-core cpu. 
