from concurrent import futures
from log import log_handler
from pconf import MAX_WORKERS, SCRAPE_LIMIT
from typing import List, Dict
from constants import COMPANY_RETRIEVE_URL, COMPANY_LIST_URL, BASE_HEADERS
import requests
import concurrent.futures

company_retrieve_url_generator = lambda ric: f"{COMPANY_RETRIEVE_URL}?ricCode={ric}"

logger = log_handler('crawler')


class FetchFailureError(Exception):
    def __init__(self, status_code, content):
        super().__init__(f"Failed to fetch: code {status_code}")
        self.status_code = status_code
        self.content = content


class Crawler:
    @staticmethod
    def _get_companies() -> List[Dict]:
        logger.info("start fetching companies list.")
        return requests.get(COMPANY_LIST_URL).json()

    @staticmethod
    def _get_company_score(company_score_retrieve_url: str):
        req = requests.get(company_score_retrieve_url)
        if not req:
            raise FetchFailureError(req.status_code, req.content)
        return req

    @staticmethod
    def get_all_companies_score():
        companies_rics = [c['ricCode'] for c in Crawler._get_companies()]

        logger.info(f"fetched companies list. found {len(companies_rics)} companies")

        urls = list(map(company_retrieve_url_generator, companies_rics))

        logger.info(f"starting fetching companies(limit={SCRAPE_LIMIT}) score using {MAX_WORKERS} workers.")

        resp_ok = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            res = executor.map(Crawler._get_company_score, urls)
            for req in res:
                try:
                    if resp_ok >= SCRAPE_LIMIT:
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                except futures.TimeoutError as e:
                    logger.error(e)
                    break
                except FetchFailureError as e:
                    logger.error(e, e.status_code, e.content)
                    break
                else:
                    resp_ok = resp_ok + 1


if __name__ == '__main__':
    Crawler.get_all_companies_score()
