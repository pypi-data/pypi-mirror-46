# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from datetime import datetime
from io import BytesIO
from os.path import exists, join

from scrapy.pipelines.files import FilesPipeline

import esgf_scraper.ext.dblite as dblite
from esgf_scraper.checksum import md5sum, sha1sum, sha256sum
from esgf_scraper.items import DatasetSearchItem, ESGFDownloadItem
from esgf_scraper.middlewares import ESGFRequest
from esgf_scraper.sqlite_queue import SqliteQueue
from esgf_scraper.utils import print_items

logger = logging.getLogger(__name__)


class DuplicateItem(Exception):
    pass


class StoreItemsPipeline(object):
    def __init__(self):
        self.ds = None
        self.items = []

    def open_spider(self, spider):
        self.ds = dblite.open(
            DatasetSearchItem, "sqlite://datasets.sqlite:items", autocommit=True
        )

    def close_spider(self, spider):
        self.ds.close()
        if len(self.items):
            print_items(self.items, cols=["instance_id", "status"])

    def process_item(self, item, spider):
        if isinstance(item, DatasetSearchItem):
            res = dict(item)
            try:
                res["status"] = "New"
                # Check to see if the file is already downloaded
                if (
                    self.ds.get(criteria={"instance_id": item["instance_id"]}, limit=1)
                    is not None
                ):
                    res["status"] = "Downloaded"

                if spider.add:
                    try:
                        self.ds.put(item)
                        res["status"] = "Added"
                    except dblite.DuplicateItem:
                        res["status"] = "Duplicate"
                        raise DuplicateItem("Duplicate item found: %s" % item)
            finally:
                self.items.append(res)
        return item


class ToDownloadPipeline(object):
    def __init__(self):
        self.ds = None

    def open_spider(self, spider):
        self.queue = SqliteQueue("datasets.sqlite")

    def process_item(self, item, spider):
        if isinstance(item, DatasetSearchItem) and spider.add:
            self.queue.append({"instance_id": item["instance_id"]})
        return item


class ESGFDownloadPipeline(FilesPipeline):
    def __init__(self, *args, **kwargs):
        super(ESGFDownloadPipeline, self).__init__(*args, **kwargs)
        self.items = []

    def open_spider(self, spider):
        super(ESGFDownloadPipeline, self).open_spider(spider)
        self.queue = SqliteQueue("datasets.sqlite", table_name="postprocess_queue")
        self.ds = dblite.open(
            DatasetSearchItem, "sqlite://datasets.sqlite:items", autocommit=True
        )

    def close_spider(self, spider):
        self.ds.close()
        if len(self.items):
            print_items(self.items, cols=["instance_id", "filename", "status"])

    def get_file_path(self, item):
        return join(item["output_dir"], item["filename"])

    def _check_existing(self, item):
        """
        Check if an existing file is valid
        :param item:
        :return: True if file exists and has a valid checksum
        """
        fname = join(self.store.basedir, self.get_file_path(item))
        if not exists(fname):
            return False

        checksum = self.get_checksum(fname, item["checksum_type"])
        checksum_matches = checksum == item["checksum"]
        if not checksum_matches:
            logger.error(
                "checksum for existing file {} did not match expected value of {}:{}".format(
                    fname, item["checksum_type"], item["checksum"]
                )
            )
        return checksum_matches

    def _update_times(self, item):
        db_item = self.ds.get(criteria={"instance_id": item["instance_id"]}, limit=1)
        assert db_item is not None
        db_item["verified_at"] = datetime.utcnow().isoformat()
        if db_item["downloaded_at"] is None:
            db_item["downloaded_at"] = datetime.utcnow().isoformat()
        self.ds.put(db_item)

    def get_checksum(self, fname_or_buff, checksum_type):
        fname_or_buff = (
            open(fname_or_buff, "rb")
            if isinstance(fname_or_buff, str)
            else fname_or_buff
        )
        fname_or_buff.seek(0)
        if checksum_type.lower() == "md5":
            return md5sum(fname_or_buff)
        elif checksum_type.lower() == "sha1":
            return sha1sum(fname_or_buff)
        elif checksum_type.lower() == "sha256":
            return sha256sum(fname_or_buff)

        raise ValueError("Unknown checksum type: " + checksum_type)

    def get_media_requests(self, item, info):
        if isinstance(item, ESGFDownloadItem):
            res = dict(item)
            if not self._check_existing(item):
                return [ESGFRequest(item)]
            else:
                logger.debug("{} exists already".format(self.get_file_path(item)))
                res["status"] = "Verified"
                self._update_times(res)
                self.items.append(res)

        return []

    def file_downloaded(self, response, request, info):
        res = dict(request.item)
        path = self.get_file_path(request.item)
        buf = BytesIO(response.body)
        checksum_type = request.item["checksum_type"]
        checksum = self.get_checksum(buf, checksum_type)
        exp_checksum = request.item["checksum"]

        if checksum != exp_checksum:
            logging.error(
                "Checksum for download {} does not match {}:{} != {}:{}".format(
                    request.url, checksum_type, checksum, checksum_type, exp_checksum
                )
            )
            res["status"] = "Failed Checksum"

            return checksum
        else:
            buf.seek(0)
            self.store.persist_file(path, buf, info)
            res["status"] = "Downloaded"
            self._update_times(res)

            # Queue item up for postprocessing
            self.queue.append({"instance_id": res["instance_id"]}, deduplicate=True)
        self.items.append(res)
        return checksum
