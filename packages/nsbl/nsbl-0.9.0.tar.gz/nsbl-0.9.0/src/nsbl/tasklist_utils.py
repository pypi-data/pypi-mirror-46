# -*- coding: utf-8 -*-

# python 3 compatibility
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os

from ruamel.yaml.comments import CommentedSeq
from six import string_types

from frkl import load_object_from_url_or_path
from frutils import StringYAML, DEFAULT_EXCLUDE_DIRS
from .exceptions import NsblException

log = logging.getLogger("nsbl")

yaml = StringYAML()
yaml.default_flow_style = False

ANSIBLE_TASK_KEYWORDS = [
    "any_errors_fatal",
    "async",
    "become",
    "become_flags",
    "become_method",
    "become_user",
    "changed_when",
    "check_mode",
    "connection",
    "debugger",
    "delay",
    "delegate_facts",
    "delegate_to",
    "diff",
    "environment",
    "failed_when",
    "ignore_errors",
    "loop",
    "loop_control",
    "name",
    "no_log",
    "notify",
    "poll",
    "port",
    "register",
    "remote_user",
    "retries",
    "run_once",
    "tags",
    "until",
    "when",
]

TASKLIST_CACHE = {}
TASKLIST_EXTENSIONS = ["yaml", "yml"]


def find_tasklists_in_repos(tasklist_repos, exclude_paths=None):

    if exclude_paths is None:
        exclude_paths = []

    if isinstance(tasklist_repos, string_types):
        tasklist_repos = [tasklist_repos]

    result = {}
    tasklists_per_repo = {}

    for tlr in tasklist_repos:
        tasklists = find_tasklists_in_repo(tlr, exclude_paths=exclude_paths)
        # we want tasklists to be found first to take precedence
        for tln, content in tasklists.items():
            if tln not in result.keys():
                result[tln] = content
                tasklists_per_repo.setdefault(tlr, []).append(tln)

    return result, tasklists_per_repo


def find_tasklists_in_repo(tasklist_repo, exclude_paths=None):

    if exclude_paths is None:
        exclude_paths = []

    if tasklist_repo in TASKLIST_CACHE.keys():
        return TASKLIST_CACHE[tasklist_repo]

    result = {}
    try:
        for root, dirnames, filenames in os.walk(
            os.path.realpath(tasklist_repo), topdown=True, followlinks=True
        ):
            dirnames[:] = [d for d in dirnames if d not in DEFAULT_EXCLUDE_DIRS]
            dirnames[:] = [
                d for d in dirnames if os.path.join(root, d) not in exclude_paths
            ]
            # check for extensions

            for filename in filenames:
                match = False
                for ext in TASKLIST_EXTENSIONS:
                    if filename.endswith(".{}".format(ext)):
                        match = True
                        break

                if not match:
                    continue

                tl_file = os.path.join(root, filename)

                try:
                    format, tasklist = get_tasklist_file_format(tl_file)
                    if format != "ansible":
                        log.debug(
                            "Not ansible tasklist format, ignoring: {} -> {}".format(
                                tl_file, format
                            )
                        )
                        continue

                    # tl_name = os.path.splitext(filename)[0]
                    result[filename] = tasklist

                except (Exception) as e:
                    log.warning(
                        ("Could not parse tasklist '{}': {}".format(tl_file, e))
                    )
                    log.debug(e, exc_info=1)

    except (UnicodeDecodeError):
        print(
            " X one or more filenames under '{}' can't be decoded, ignoring. This can cause problems later. ".format(
                root
            )
        )

    TASKLIST_CACHE[tasklist_repo] = result
    # import pp
    # print("TASKLISTS")
    # pp(result)
    return result


def get_tasklist_file_format(path):

    if not isinstance(path, string_types):
        raise NsblException("tasklist file needs to be string: {}".format(path))

    tasklist = load_object_from_url_or_path(path)

    return get_tasklist_format(tasklist), tasklist


def get_tasklist_format(task_list):
    """This is a not quite 100% method to check whether a task list is in ansbile format, or freckle.
    """

    if not task_list or not isinstance(task_list, (list, tuple, CommentedSeq)):
        return "unknown"

    for item in task_list:

        if isinstance(item, string_types):
            log.debug(
                "task item '{}' is string, determining this is a 'freckles' task list".format(
                    item
                )
            )
            return "freckles"
        elif isinstance(item, dict):
            keys = set(item.keys())
            if keys & set(ANSIBLE_TASK_KEYWORDS):
                log.debug(
                    "task item keys ({}) contain at least one known Ansible keyword , determining this is 'ansible' task list format".format(
                        keys
                    )
                )
                return "ansible"
        else:
            raise Exception("Not a valid task-list item: {}".format(item))

    # TODO: log outupt
    # could check for 'meta' key above, but 'meta' can be a keyword in ansible too,
    # so figured I check for everything else first
    for item in task_list:
        if "frecklet" in item.keys():
            log.debug(
                "task item '{}' has 'frecklet' key, determining this is a 'freckles' task list".format(
                    item["frecklet"].get("name", item)
                )
            )
            return "freckles"
        for key in item.keys():
            if key.isupper():
                log.debug(
                    "task item key '{}' is all uppercase, determining this is a 'freckles' task list".format(
                        key
                    )
                )
                return "freckles"
    return "unknown"


def convert_ansible_tasklist(
    tasklist_name,
    tasklist,
    import_type="import",
    convert_ansible_template_markers_to_freckles=False,
):

    if import_type not in ["import", "include"]:
        raise Exception("Invalid import type: {}".format(import_type))

    if convert_ansible_template_markers_to_freckles:
        raise NotImplementedError(
            "Converting ansible template markers not implemented yet."
        )

    result = {
        "name": tasklist_name,
        # "command": tasklist_name,
        "import_type": import_type,
        "type": "ansible-tasklist",
        "tasklist_content": tasklist,
        "tasklist_var": "ansible_tasklist_{}".format(tasklist_name),
    }

    return result
