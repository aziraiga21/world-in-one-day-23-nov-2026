#!/usr/bin/env python3
"""Entrypoint the grader runs: copy entry.png to $MAKEFUN_OUTPUT_DIR.

Standard library only (os, shutil, pathlib). No Pillow, no network.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(SRC, dest)
    print("copied %s -> %s" % (SRC, dest))


if __name__ == "__main__":
    main()
