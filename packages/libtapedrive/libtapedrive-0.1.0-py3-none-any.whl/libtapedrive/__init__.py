import os
import feedparser
import logging
import tempfile
import xml.etree.ElementTree as etree
from collections import namedtuple
from io import BytesIO
from shutil import copyfileobj, move
from urllib.parse import urlparse, urlunparse
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# import requests
# from feedparser import CharacterEncodingOverride
# from PIL import Image

# from django.conf import settings

# from podcasts.utils.filters import shownotes_image_cleaner
# from podcasts.utils.parsers.feed_content import parse_feed_info

__version__ = "0.1.0"
__source__ = "https://github.com/janw/libtapedrive"

# Get an instance of a logger
logger = logging.getLogger(__name__)


feed_info = namedtuple("feed_info", ["data", "url", "next_page", "last_page"])


def replace_shownotes_images(content, allowed_domains=False):
    if len(allowed_domains) == 1 and allowed_domains[0] == "*":
        return content
    else:
        return shownotes_image_cleaner.clean(content, allowed_domains=allowed_domains)


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i : i + n]


def strip_url(link):
    linkpath = urlparse(link).path
    extension = os.path.splitext(linkpath)[1]
    return linkpath, extension


def handle_uploaded_file(f):
    with tempfile.NamedTemporaryFile(delete=False) as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return destination.name


def parse_opml_file(filename):
    with open(filename) as file:
        tree = etree.fromstringlist(file)
    return [
        node.get("xmlUrl")
        for node in tree.findall("*/outline/[@type='rss']")
        if node.get("xmlUrl") is not None
    ]


def unify_apple_podcasts_response(data):
    if "feed" in data:
        data["results"] = data["feed"]["results"]
        data["resultsCount"] = len(data["results"])
    for i, result in enumerate(data["results"]):
        if "collectionId" in result:
            data["results"][i]["id"] = int(result["collectionId"])
        else:
            data["results"][i]["id"] = int(result["id"])
        if "collectionName" in result:
            data["results"][i]["name"] = result["collectionName"]

        if "artworkUrl600" in result:
            data["results"][i]["artworkUrl"] = result["artworkUrl600"]
        elif "artworkUrl100" in result:
            data["results"][i]["artworkUrl"] = result["artworkUrl100"]

        if "genres" in result and isinstance(result["genres"][0], dict):
            data["results"][i]["genres"] = [
                dict(name=item.get("name")) for item in result["genres"]
            ]

    return data
