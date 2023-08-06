import os
import hashlib
import argparse

# ctrl+]
def to_hash():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, help='file name with text')
    args = vars(parser.parse_args())

    # md5 = hashlib.md5()
    sha256 = hashlib.sha256()

    try:
        with open(args["file"], 'rb') as f:
            buf = f.read()
            # md5.update(buf)
            sha256.update(buf)
        print(sha256.hexdigest())
    except FileNotFoundError as e:
        print(e)