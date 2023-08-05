import os
import requests
from mfetcher.download import download_and_save
from mfetcher.utils import create_hash_list, find_image_link, page_exist


def download_chapter(mangas_chapter, mangas_url, out_dir, provider):

    # create a dir of the name of the chapter
    dir_name = "{}/chapter_{}".format(out_dir, mangas_chapter)

    scan_urls = []  # will keep the scans url of the current chapter
    hash_list = create_hash_list(dir_name)

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    # get the chapter url
    mangas_chapter_url = "{}/{}".format(mangas_url, mangas_chapter)

    page = 0
    while True:

        page = page + 1
        # page_url = urljoin(mangas_chapter_url, page)
        # page_url = "{mangas_chapter_url}?page={page}".format(mangas_chapter_url=mangas_chapter_url, page=page)
        if provider['URL_SUFFIX'] == "file":
            
            page_url = "{mangas_chapter_url}/{page}{suffix}".format(mangas_chapter_url=mangas_chapter_url, page=page,
                                                                suffix=provider['URL_SUFFIX'])
        else:
            page_url = "{mangas_chapter_url}?page={page}".format(mangas_chapter_url=mangas_chapter_url, page=page)

        if page_exist(dir_name, page, provider):
            """ If the file for the scan exist """
            # print("The Scan which is at page " + str(page) + " already exist. Skipping ...")
            print(str(page) + "exist: Skipping ...")
            continue

        # crawl the web page
        try:
            response = requests.get(page_url)
        except ConnectionError as err:
            print(err)
            break
        except Exception as err:
            print(err)
            break

        if response.status_code == 404:
            break

        # find the image link
        image_link = find_image_link(response.content.__str__(), provider)

        if image_link is None:
            # if the image link returned is not valid, skip the current index
            continue

        # append the current link to the scanned urm
        scan_urls.append(image_link)

        # download and save the file
        last_hash = download_and_save(image_link, dir_name, page, hash_list, provider)

        if last_hash is None:
            # if the hash return by the download function return None, skip the execution
            continue
        else:
            hash_list.append(last_hash)
