import re

from os import scandir
from os.path import exists
from hashlib import sha256


def get_slug(name):
    name = name.replace(" ", "-")

    return name


def find_image_link(response, provider):

    img_tags_re = re.compile(provider['IMG_REGEX'])
    img_tags = img_tags_re.search(response)

    try:
        return img_tags.group(1)

    except IndexError:
        return None


def page_exist(dir_name, page, provider):
    for ext in provider['CORRECT_EXT']:
        file = "{location}/{name}.{ext}".format(location=dir_name, name=page, ext=ext)
        if exists(file):
            return True
    return False


def create_hash(file):
    """hash a file with the sha256 algo"""
    hasher = sha256()
    try:
        with open(file, "rb") as f:
            hasher.update(f.read())
            return hasher.hexdigest()

    except Exception:
        return None


def create_content_hash(content):
    """hash a file with the sha256 algo"""
    hasher = sha256()
    try:
        hasher.update(content)
        return hasher.hexdigest()

    except Exception:
        return None


def create_hash_list(target_dir):
    """Hash list of the files
    :param target_dir:
    :return: []

    calculate the digest of all the file which exist in the chap directory
    so before saving a file, check if it's hash already exist
    """
    hash_list = []  # store the hash in this array

    if exists(target_dir):
        files = scandir(target_dir)

        for file in files:
            if file.is_dir():  # ignore the directories
                continue
            digest = create_hash(file.path)  # create the hash of the current file
            if digest is not None:  # if the digest is None
                hash_list.append(digest)  # append the hash to the hash_list

    return hash_list
