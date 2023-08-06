#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import subprocess


def git_clone(repository_uri):
    return subprocess.run(
        ["git", "clone", repository_uri],
        shell=True,
        check=True,
        universal_newlines=True
    )
