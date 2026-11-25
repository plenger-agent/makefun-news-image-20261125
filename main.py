#!/usr/bin/env python3
"""Hand-in program for make.fun competition news-image-20261125.

Copies the committed front-page image (entry.png, rendered by gen.py)
into the output directory as entry.png. Standard library only, so it
runs in the grader's bare Python 3.13 image. Deterministic: both runs
write exactly the same bytes.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main() -> int:
    if not os.path.isfile(SOURCE):
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    # The output directory is a mount point: never remove it, only
    # write the file into it.
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
