#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os

from .workspace import create_new_workspace


#
# ========================================================
#                  create command
# ========================================================
#

MODULE_TEMPLATE_GIT_REPOSITORY_URI = (
    'http://git.kanzhun-inc.com/liulong/graph-parent.git'
)
MS_TEMPLATE_GIT_REPOSITORY_URI = (
    'http://git.kanzhun-inc.com/liulong/graph-oceanus-service.git'
)


def clone_repository(workspace, isfor_ms):
    """
    clone git项目(基准项目，提供cookiecutter模板)

    Args:
      isfor_ms: 是否为微服务项目

    """
    from .repository import git_clone

    cur_path = os.getcwd()
    os.chdir(workspace)

    if isfor_ms:
        repository_uri = MS_TEMPLATE_GIT_REPOSITORY_URI
    else:
        repository_uri = MODULE_TEMPLATE_GIT_REPOSITORY_URI

    git_clone(repository_uri)

    os.chdir(cur_path)


def run_cookiecutter(workspace, isfor_ms):
    from cookiecutter.main import cookiecutter

    if isfor_ms:
        tmpl_path = os.path.join(
            workspace,
            "graph-oceanus-service",
            "cookiecutter-graph-oceanus-service"
        )
    else:
        tmpl_path = os.path.join(
            workspace,
            "graph-parent",
            "cookiecutter-graph-module"
        )

    return cookiecutter(tmpl_path)


def create(isfor_ms):
    """
    创建项目

    Args:
      isfor_ms: 是否创建微服务项目

    Returns:
      创建好的项目路径

    """
    workspace = create_new_workspace()
    clone_repository(workspace, isfor_ms)
    return run_cookiecutter(workspace, isfor_ms)
