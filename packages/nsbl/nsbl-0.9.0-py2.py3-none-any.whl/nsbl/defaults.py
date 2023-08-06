# -*- coding: utf-8 -*-
import os

NSBL_MODULE_FOLDER = os.path.dirname(__file__)

TEMPLATES_FOLDER = os.path.join(NSBL_MODULE_FOLDER, "templates")

# stem key for inventory
ENVS_KEY = "envs"
# meta info for groups/hosts (contains for example 'hosts' for groups)
ENV_META_KEY = "meta"
# name of the group/host
ENV_NAME_KEY = "name"
# type of the environemnt (either group or host)
ENV_TYPE_KEY = "type"
# under meta key, lists hosts of a group
ENV_HOSTS_KEY = "hosts"
# under meta key, lists sub-groups of a group, or which groups a host is member is
ENV_GROUPS_KEY = "groups"
# vars for a host/group
VARS_KEY = "vars"
# tasks for a hosts/group, used to create playbooks
TASKS_KEY = "tasks"

ENV_TYPE_HOST = "host"
ENV_TYPE_GROUP = "group"
DEFAULT_ENV_TYPE = ENV_TYPE_GROUP

# id of the environment tasks are run in
ENV_ID_KEY = "_env_id"

TASKS_META_KEY = "meta"

# whether to 'import_*' or 'include_*' roles & tasks if not specified
DEFAULT_INCLUDE_TYPE = "include"

ADD_TYPE_TASK_LIST = "TASK_LIST"
ADD_TYPE_TASK_LIST_FILE = "TASK_LIST_FILE"
ADD_TYPE_ROLE = "ROLE"
ADD_TYPE_CALLBACK = "CALLBACK_PLUGIN"
ADD_TYPE_ACTION = "ACTION_PLUGIN"
ADD_TYPE_LIBRARY = "LIBRARY_PLUGIN"
ADD_TYPE_FILTER = "FILTER_PLUGIN"
ADD_TYPE_MODULE_UTIL = "MODULE_UTIL"
ADD_TYPE_FILES = "FILES"
ADD_FILE_TYPES = [
    ADD_TYPE_TASK_LIST,
    ADD_TYPE_ROLE,
    ADD_TYPE_CALLBACK,
    ADD_TYPE_ACTION,
    ADD_TYPE_LIBRARY,
    ADD_TYPE_FILTER,
    ADD_TYPE_MODULE_UTIL,
    ADD_TYPE_FILES,
    ADD_TYPE_TASK_LIST_FILE,
]

ANSIBLE_ROLE_CACHE_DIR = os.path.expanduser("~/.cache/ansible-roles")

# only used for output
ROLE_ID_KEY = "_role_id"
TASK_META_NAME_KEY = "name"
DYN_TASK_ID_KEY = "_dyn_task_id"
DYN_ROLE_TYPE = "dyn_role"

MITOGEN_VERSION = "0.2.6"
