#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
执行jcake工作空间的支持

"""

import os
import random

__all__ = ['create_new_workspace']


ROOT_DIR_NAME = '.jcake'
_POPULATION = ('abcdefghigklmnopqrstuvwxzy'
               'ABCDEFGHIGKLMNOPQRSTUVWXYZ' 
               '0123456789')


def get_user_home():
    from os.path import expanduser
    return expanduser('~')


def get_or_create_root_dir():
    home = get_user_home()
    root_dir = os.path.join(home, ROOT_DIR_NAME)

    os.makedirs(root_dir, exist_ok=True)
    return root_dir


def next_workspace_name():
    """
    生成工作空间名称

    生成机制为获取当前所处目录名称 + 随机生成的
    """

    cur_dir = os.path.basename(os.getcwd())
    random_name = ''.join(random.sample(_POPULATION, 8))
    return cur_dir + '-' + random_name


def create_new_workspace():
    """
    创建新的工作空间

    使用当前操作系统用户目录作为父目录，其中.jcake作为整个工作目录的根目录

    Returns:
      工作空间目录路径

    """

    root_dir_path = get_or_create_root_dir()
    space_name = next_workspace_name()

    workspace_dir_path = os.path.join(root_dir_path, space_name)
    os.makedirs(workspace_dir_path)
    return workspace_dir_path
