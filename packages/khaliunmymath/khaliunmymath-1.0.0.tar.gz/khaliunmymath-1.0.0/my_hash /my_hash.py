import os
import hashlib
import argparse


def to_hash():
    parses = argparse.ArgumentParser()
    parses.add_argument("-f", "--file", required=True,
                        help='file name with text')
    args = vars(parses.parse_args())
    shal256 = hashlib.sha256()

    try:
        with open(args[file], 'rb') as f:
            buf = f.read()

            sha256.update(buf)
        print(sha256.hexdigest())

    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    to_hash()
