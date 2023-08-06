import json
import logging
from urllib.parse import parse_qs, urlencode, urlsplit

import scrapy

from esgf_scraper import config
from esgf_scraper.items import DatasetSearchItem

logger = logging.getLogger(__name__)

ESGF_NODE = "esgf-node.llnl.gov"


def create_search_url(**kwargs):
    kwargs.setdefault("format", "application/solr+json")
    kwargs.setdefault("offset", 0)
    kwargs.setdefault("limit", 100)
    kwargs.setdefault("latest", True)
    kwargs.setdefault("type", "Dataset")
    kwargs.setdefault("replica", False)

    return "https://{}/esg-search/search?{}".format(
        ESGF_NODE, urlencode(kwargs, doseq=True)
    )


class SearchSpider(scrapy.Spider):
    name = "search"

    def __init__(self, *args, **kwargs):
        if isinstance(kwargs["filters"], dict):
            kwargs["filters"] = [kwargs["filters"]]
        else:
            kwargs["filters"] = config["data_filters"]
        super(SearchSpider, self).__init__(*args, **kwargs)
        self.count = 0

    def start_requests(self):
        for filters in self.filters:
            yield scrapy.Request(url=create_search_url(**filters), callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)

        resp = data["response"]
        logger.info(
            "reading {}-{}/{} documents".format(
                resp["start"], resp["start"] + len(resp["docs"]), resp["numFound"]
            )
        )

        for d in resp["docs"]:
            yield DatasetSearchItem(d)

            # Keep track of number of downloads
            self.count = self.count + 1
            if self.limit is not None and self.count >= self.limit:
                logging.info("reached limit. Stopping")
                return

        if resp["start"] + len(resp["docs"]) < resp["numFound"]:
            yield scrapy.Request(self.get_next_url(response.url))

    def get_next_url(self, old_url):
        url = urlsplit(old_url)
        qs = parse_qs(url.query)

        # update the offset
        offset = int(qs["offset"][0]) if "offset" in qs else 0
        limit = int(qs["limit"][0]) if "limit" in qs else 0
        qs["offset"] = offset + limit

        return create_search_url(**qs)
