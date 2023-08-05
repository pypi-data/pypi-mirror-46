from docopt import docopt
from mfetcher import fetcher


def main():
    args = docopt(fetcher.__doc__)
    try:
        fetcher.main(args)
    except KeyboardInterrupt:
        pass
