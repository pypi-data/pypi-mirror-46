import argparse
import sys
from logging import getLogger

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import esgf_scraper.ext.dblite as dblite
from esgf_scraper import config
from esgf_scraper.items import DatasetSearchItem
from esgf_scraper.postprocess import run_postprocessing
from esgf_scraper.sqlite_queue import SqliteQueue
from esgf_scraper.utils import print_items

logger = getLogger("esgf-scraper")


def arglist_to_dict(arglist):
    res = dict(x.split("=", 1) for x in arglist)

    def _process_arg(v):
        if v.startswith("[") and v.endswith("]"):
            return [i.strip() for i in v[1:-1].split(",")]
        return v

    return {k: _process_arg(v) for k, v in res.items()}


def search_func(args):
    crawl_process = CrawlerProcess(config["scrapy"])
    crawl_process.crawl(
        "search",
        add=args.add,
        filters=arglist_to_dict(args.spargs) if len(args.spargs) else None,
        limit=args.limit,
    )
    crawl_process.start()

    sys.exit(int(crawl_process.bootstrap_failed))


def download_func(args):
    queue = SqliteQueue("datasets.sqlite", table_name="download_queue")
    failed_queue = SqliteQueue("datasets.sqlite", table_name="failed_download_queue")

    if args.requeue:
        while len(failed_queue):
            obj = failed_queue.popleft()
            logger.info("requeuing {} for downloading".format(obj))
            queue.append(obj, deduplicate=True)

    crawl_process = CrawlerProcess(config["scrapy"])
    crawl_process.crawl("download")
    crawl_process.start()

    sys.exit(int(crawl_process.bootstrap_failed))


def verify_func(args):
    queue = SqliteQueue("datasets.sqlite")
    ds = dblite.open(
        DatasetSearchItem, "sqlite://datasets.sqlite:items", autocommit=True
    )
    filters = arglist_to_dict(args.spargs)
    criteria = {k: 'r/"{}"/'.format(v) for k, v in filters.items()}
    items = list(ds.get(criteria=criteria))
    for item in items:
        queue.append({"instance_id": item["instance_id"]})

    print("Added {} items to queue for validation".format(len(items)))


def list_func(args):
    ds = dblite.open(
        DatasetSearchItem, "sqlite://datasets.sqlite:items", autocommit=True
    )

    filters = arglist_to_dict(args.spargs)
    cols = args.cols.split(",")
    criteria = {k: 'r/"{}"/'.format(v) for k, v in filters.items()}
    items = list(ds.get(criteria=criteria))

    print_items(items, cols)


def postprocess_func(args):
    queue = SqliteQueue("datasets.sqlite", table_name="postprocess_queue")
    failed_queue = SqliteQueue("datasets.sqlite", table_name="failed_postprocess_queue")
    ds = dblite.open(
        DatasetSearchItem, "sqlite://datasets.sqlite:items", autocommit=True
    )

    if args.requeue:
        while len(failed_queue):
            obj = failed_queue.popleft()
            logger.info("requeuing {} for postprocessing".format(obj))
            queue.append(obj, deduplicate=True)

    while len(queue):
        logger.info("{} items remaining".format(len(queue)))
        obj = queue.popleft()

        try:
            item = ds.get(criteria=obj, limit=1)
            assert item is not None
            run_postprocessing(item)
        except Exception:
            logger.exception("Failed to postprocess item: {}".format(obj))
            failed_queue.append(obj)


def main():
    scrapy_settings = get_project_settings()

    parser = argparse.ArgumentParser(description="Download climate data from ESGF")
    parser.add_argument(
        "-c",
        "--config",
        help="Path to configuration filename. Defaults to looking in the current directory and home directory for a "
        "file named `esgf_scraper.conf`",
    )
    parser.add_argument("-b", "--base-dir", help="Base directory to write files")
    parser.add_argument(
        "-l",
        "--log-level",
        help="Specify the level below which log messages are dropped. Defaults to WARNING. "
        "Other options include DEBUG, INFO, ERROR and FATAL",
        default="WARNING",
    )

    subparsers = parser.add_subparsers(help="subcommands", dest="cmd")

    commands = {
        "search": search_func,
        "verify": verify_func,
        "download": download_func,
        "list": list_func,
        "postprocess": postprocess_func,
    }

    parser_search = subparsers.add_parser("search", help="Search for files on ESGF")
    parser_search.add_argument(
        "--add",
        default=False,
        action="store_true",
        help="Add to the files to be downloaded",
    )
    parser_search.add_argument(
        "-f",
        "--filter",
        dest="spargs",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help="facets to filter. Of the format NAME=VALUE where value can be a string or a list of strings and name is a valid "
        "esgf facet. This argument can be passed many times. The results in this case will be an AND of the various filters",
    )
    parser_search.add_argument(
        "-l",
        "--limit",
        default=None,
        type=int,
        help="Limit the number of results to search",
    )

    parser_download = subparsers.add_parser("download", help="Runs the downloader")
    parser_download.add_argument(
        "--requeue",
        default=False,
        action="store_true",
        help="Requeues any previously failed items before downloading",
    )

    parser_verify = subparsers.add_parser(
        "verify", help="Queue all tracked tracked files to be reverified"
    )
    parser_verify.add_argument(
        "-f",
        "--filter",
        dest="spargs",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help="facets to filter. Of the format NAME=VALUE where value can be a string or a list of strings and name is a valid "
        "esgf facet. This argument can be passed many times. The results in this case will be an AND of the various filters",
    )

    parser_list = subparsers.add_parser(
        "list", help="List the files and their statuses"
    )
    parser_list.add_argument(
        "-f",
        "--filter",
        dest="spargs",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help="facets to filter. Of the format NAME=VALUE where value can be a string or a list of strings and name is a valid "
        "esgf facet. This argument can be passed many times. The results in this case will be an AND of the various filters",
    )
    parser_list.add_argument(
        "-c", "--columns", dest="cols", default="all", metavar="COL1,COL2"
    )

    parser_postprocess = subparsers.add_parser(
        "postprocess",
        help="Postprocess any items. The postprocessing steps are configured in the config file.",
    )
    parser_postprocess.add_argument(
        "--requeue",
        default=False,
        action="store_true",
        help="Requeues any previously failed items before running the postprocessing steps",
    )

    args = parser.parse_args()

    # Update some defaults
    if args.config is not None:
        config.load_from_file(args.config)

    if args.base_dir is not None:
        scrapy_settings["FILES_STORE"] = args.base_dir
    else:
        try:
            scrapy_settings["FILES_STORE"] = config["base_dir"]
        except KeyError:
            pass
        if scrapy_settings["FILES_STORE"] is None:
            raise ValueError("No valid `FILES_STORE` configuration")

    scrapy_settings["LOG_LEVEL"] = args.log_level
    config.update({"scrapy": scrapy_settings})

    # Run the command
    commands[args.cmd](args)


if __name__ == "__main__":
    main()
