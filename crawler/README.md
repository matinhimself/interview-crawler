## Crawler 

- sends a request to https://www.refinitiv.com/bin/esg/esgsearchsuggestions to fetch all companies.

- fetch companies one by one from https://www.refinitiv.com/bin/esg/esgsearchresult in a threadpool.

- batch import into the db.
