from concurrent import futures
from log import log_handler
from pconf import MAX_WORKERS, SCRAPE_LIMIT
from typing import List, Dict
from constants import COMPANY_RETRIEVE_URL, COMPANY_LIST_URL
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
    def _parse_score(score: Dict) -> Dict:
        return {
            "industryComparison": score["industryComparison"],
            "esgScore": score["esgScore"]["TR.TRESG"]['score'],
            "socialScore": score["esgScore"]["TR.SocialPillar"]['score'],
            "environmentScore": score["esgScore"]["TR.EnvironmentPillar"]['score'],
            "governanceScore": score["esgScore"]["TR.GovernancePillar"]['score'],
        }

    @staticmethod
    def _get_companies() -> List[Dict]:
        logger.info("start fetching companies list.")
        return requests.get(COMPANY_LIST_URL).json()

    @staticmethod
    def _get_company_score(company: Dict):
        company_ric = company['ricCode']
        company_name = company['companyName']

        req = requests.get(company_retrieve_url_generator(company_ric))
        print(req)
        if not req:
            raise FetchFailureError(req.status_code, req.content)
        return company_ric, company_name, req

    @staticmethod
    def get_all_companies_score():
        companies_rics = Crawler._get_companies()

        logger.info(f"fetched companies list. found {len(companies_rics)} companies")

        logger.info(f"starting fetching companies(limit={SCRAPE_LIMIT}) score using {MAX_WORKERS} workers.")

        # appending to list is thread-safe in python so no need to locks, ...
        results = []
        # using with, also shutting down futures will ensure that threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for company_ric, company_name, req in executor.map(Crawler._get_company_score, companies_rics):
                try:
                    if len(results) >= SCRAPE_LIMIT:
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                except futures.TimeoutError as e:
                    # Terminates if a thread lives longer than it should
                    logger.error(e)
                    break
                except FetchFailureError as e:
                    # Fails on non 2** requests
                    # Its better to implement fallback adapter for requests
                    logger.error(e, e.status_code, e.content)
                    break
                else:
                    # we already checked the responses status code,
                    # but it'd better to double check its valid json resp.
                    results.append({
                        "ric": company_ric,
                        "score": Crawler._parse_score(req.json()),
                        "name": company_name
                    })


if __name__ == '__main__':
    Crawler.get_all_companies_score()
