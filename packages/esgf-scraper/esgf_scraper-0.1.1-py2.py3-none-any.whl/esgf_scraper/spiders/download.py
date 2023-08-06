import logging
from urllib.parse import urljoin, urlsplit

import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError, TimeoutError

import esgf_scraper.ext.dblite as dblite
from esgf_scraper.items import DatasetSearchItem, ESGFDownloadItem
from esgf_scraper.sqlite_queue import SqliteQueue

logger = logging.getLogger(__name__)


def parse_esgf_meta(queue, obj):
    """
    Wrapper for parsing a ESGF thredds response

    If it fails for whatever reason then the result is added to the failed queue
    :param queue:
    :param obj:
    :return:
    """

    def _parse(response):
        try:
            response.selector.remove_namespaces()

            instance_id = response.selector.xpath("/catalog/dataset/@ID").get()
            url_components = urlsplit(response.url)
            path = response.selector.xpath(
                '//service[@serviceType="HTTPServer"]/@base'
            ).get()
            assert path
            data_url = "{}://{}{}".format(
                url_components.scheme, url_components.netloc, path
            )
            output_dir = "/".join(
                instance_id.split(".")
            )  # The instance id is the . separated equiv of the folder directory

            # Find all the files to download
            for dataset in response.selector.xpath("/catalog/dataset/dataset"):
                dataset_rel_url = dataset.xpath("@urlPath").get()

                # Some aggregations don't list a urlPath
                if dataset_rel_url:
                    url = urljoin(data_url, dataset_rel_url)
                    yield ESGFDownloadItem(
                        url=url,
                        instance_id=instance_id,
                        checksum=dataset.xpath(
                            "property[@name='checksum']/@value"
                        ).get(),
                        checksum_type=dataset.xpath(
                            "property[@name='checksum_type']/@value"
                        ).get(),
                        size=dataset.xpath("property[@name='size']/@value").get(),
                        output_dir=output_dir,
                        filename=dataset.xpath("@name").get(),
                    )
        except Exception:
            logger.exception("Couldnt parse esgf metadata")
            queue.append(obj)

    return _parse


class DownloadSpider(scrapy.Spider):
    """
    Processes the download queue

    Any instances which are queued up to download are processed with this spider. The scraper makes a query to determine what files
    are available for a given instance id. Then the files are downloaded in the `ESGFDownloadPipeline`.
    """

    name = "download"

    def start_requests(self):
        self.queue = SqliteQueue("datasets.sqlite", table_name="download_queue")
        self.failed_queue = SqliteQueue(
            "datasets.sqlite", table_name="failed_download_queue"
        )
        ds = dblite.open(
            DatasetSearchItem, "sqlite://datasets.sqlite:items", autocommit=True
        )

        while len(self.queue):
            logger.info("{} items remaining".format(len(self.queue)))
            obj = self.queue.popleft()

            def request_dropped(failure):
                logger.error(repr(failure))
                if failure.check(HttpError):
                    # these exceptions come from HttpError spider middleware
                    # you can get the non-200 response
                    response = failure.value.response
                    logger.error(
                        "HttpError on {} with {}".format(
                            response.url, response.status_code
                        )
                    )

                elif failure.check(DNSLookupError):
                    # this is the original request
                    request = failure.request
                    self.logger.error("DNSLookupError on %s", request.url)

                elif failure.check(TimeoutError, TCPTimedOutError):
                    request = failure.request
                    logger.error("TimeoutError on %s", request.url)

                logger.error("could not download {}. adding to queue".format(obj))
                self.failed_queue.append(obj)

            try:
                item = ds.get(criteria=obj, limit=1)
                assert item is not None
                url = item["url"][0]
                yield scrapy.Request(
                    url=url,
                    callback=parse_esgf_meta(self.queue, obj),
                    errback=request_dropped,
                )
            except Exception:
                logger.exception("Failed to extract url")
                self.failed_queue.append(obj)

        ds.close()
