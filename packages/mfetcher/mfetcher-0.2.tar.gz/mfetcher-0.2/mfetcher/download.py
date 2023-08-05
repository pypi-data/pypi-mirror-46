import requests
from mfetcher.utils import create_content_hash
from mfetcher.Loader import Spinner

def download_and_save(link, location, page, hash_list, provider):
    req_hash = None
    loader = Spinner()
    tries = 1
    is_dowloaded = False
    is_connection_error = True

    while not is_dowloaded and is_connection_error:

        try:

            if tries > 1:
                print("({})Retrying Download {}".format(tries, page))
            else:
                print("Downloading {}".format(page))

            loader.spin()

            response = requests.get(link)

        except IndexError as error:
            print("index error" + error.__str__())
            is_connection_error = False
            continue
        except ConnectionError:
            print("Something went wrong with your internet connection. Retrying ...")
            is_connection_error = True
            continue
        except Exception as error:
            print("An Error occur : " + error.__str__())
            is_connection_error = False
            continue
        finally:
            return req_hash

    print("Complete " + str(page))
    loader.stop()

    mime_type = response.headers["content-type"]
    mime_type_parts = mime_type.split("/")

    file_ext = mime_type_parts[1]

    if file_ext not in provider['CORRECT_EXT']:
        print("incorrect file extension found :" + file_ext)

    else:
        # before saving th image, check if their is a file with the same content (md5)

        req_hash = create_content_hash(response.content)

        if req_hash in hash_list:
            print("File already downloaded")
            req_hash = None
            return

        # save the image
        with open("{location}/{name}.{ext}".format(location=location, name=page, ext=file_ext),
                "wb") as output_page:

            output_page.write(response.content)

        # return the req hash to be saved in the hash_list
        return req_hash