#!/usr/bin/python3
"""ScanFetcher

Usage:
    mfetcher --mangas <mangas_name> --out-dir <out_dir> --chapter-range <chap_start> <chap_end> --provider <provider>
    mfetcher --mangas <mangas_name> --chap <chapter>
    mfetcher --mangas <mangas_name> --chap <chapter> --provider <provider>
    mfetcher --mangas <mangas_name> --chapter-range <chap_start> <chap_end>
    mfetcher --mangas <mangas_name> --chapter-range <chap_start> <chap_end> --provider <provider>
    mfetcher (-h | --help)

Options:
    -h --help   Show this help

"""
from mfetcher.utils import get_slug

from mfetcher.download_chapter import download_chapter
from os import mkdir
from os.path import exists

import os

from urllib.parse import urljoin

# Information per providers
# BASE_URL = "https://scantrad.fr/mangas/"
# from mfetcher.download_chapter import download_chapter
# from mfetcher.providers import PROVIDERS, get_provider
# from mfetcher.utils import get_slug

from mfetcher.providers import PROVIDERS, get_provider


HASH_LIST = []


def main(args):

    # get the arguments
    out_dir = args["<out_dir>"]
    mangas_chapter = args["<chapter>"]
    mangas_name = args["<mangas_name>"]
    chapter_range = [args["<chap_start>"], args["<chap_end>"]]
    provider = args["<provider>"]
    provider = get_provider(provider)

    # get the slug of the mangas
    mangas_name_slug = get_slug(mangas_name)

    if out_dir is not None and not exists(out_dir):
        mkdir(out_dir)

    else:
        if not exists(mangas_name_slug): # Check if the if the mangas out directory exist
            mkdir(mangas_name_slug)

        out_dir = mangas_name_slug

    mangas_url = urljoin(provider["BASE_URL"], mangas_name_slug)  # get the mangas url

    if mangas_chapter is not None:  # if the mangas chapter is define
        download_chapter(mangas_chapter, mangas_url, out_dir, provider)

    elif chapter_range is not None:  # if a range of chapter is define
        for mangas_chapter in range(int(chapter_range[0]), int(chapter_range[1])+1):
            # Download the scans for this chapter
            download_chapter(mangas_chapter, mangas_url, out_dir, provider)
