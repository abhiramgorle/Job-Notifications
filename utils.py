import uuid
import os


def addHeader(num_cols):
    return "|" * (num_cols + 1) + "\n" + "|-" * num_cols + "|" + "\n"


def set_multiline_output(name, value):
    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
        delimiter = uuid.uuid1()
        print(f"{name}<<{delimiter}", file=fh)
        print(value, file=fh)
        print(delimiter, file=fh)
