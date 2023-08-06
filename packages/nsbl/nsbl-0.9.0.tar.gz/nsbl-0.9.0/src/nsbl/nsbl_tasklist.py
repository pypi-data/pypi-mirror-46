# -*- coding: utf-8 -*-

# python 3 compatibility
from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import logging

from ruamel.yaml.comments import CommentedMap
from six import string_types

from frkl import Frklist, FrklistContext
from frutils import StringYAML
from .defaults import ADD_TYPE_ROLE, ADD_TYPE_TASK_LIST, DEFAULT_INCLUDE_TYPE
from .exceptions import NsblException
from .role_utils import find_roles_in_repos
from .tasklist_utils import ANSIBLE_TASK_KEYWORDS, find_tasklists_in_repos

GLOBAL_ENV_ID_COUNTER = 1110
GLOBAL_TASKLIST_ID_COUNTER = 1110


def GLOBAL_TASKLIST_ID():
    global GLOBAL_TASKLIST_ID_COUNTER
    GLOBAL_TASKLIST_ID_COUNTER = GLOBAL_TASKLIST_ID_COUNTER + 1
    return GLOBAL_TASKLIST_ID_COUNTER


def GLOBAL_ENV_ID():
    global GLOBAL_ENV_ID_COUNTER
    GLOBAL_ENV_ID_COUNTER = GLOBAL_ENV_ID_COUNTER + 1
    return GLOBAL_ENV_ID_COUNTER


yaml = StringYAML()
yaml.default_flow_style = False

log = logging.getLogger("nsbl")


class NsblContext(FrklistContext):
    def __init__(
        self, allow_external_roles=None, allow_external_tasklists=None, **kwargs
    ):
        super(NsblContext, self).__init__(**kwargs)

        if allow_external_roles is None:
            allow_external_roles = self.allow_remote
        self.allow_external_roles = allow_external_roles

        if allow_external_tasklists is None:
            allow_external_tasklists = self.allow_remote
        self.allow_external_tasklists = allow_external_tasklists

        self.role_repo_paths = self.urls.get("roles", [])
        self.tasklist_paths = self.urls.get("tasklists", [])

        self.available_roles, all_role_paths = find_roles_in_repos(self.role_repo_paths)
        self.available_tasklists, self.tasklists_per_repo = find_tasklists_in_repos(
            self.tasklist_paths, exclude_paths=all_role_paths
        )  # we don't want tasklists from any roles

    def get_role_path(self, role_name):

        if role_name in self.available_roles.keys():
            return self.available_roles[role_name]
        else:
            if self.allow_external_roles:
                return role_name
            else:
                raise Exception(
                    "External roles not allowed, and role '{}' not in role paths: {}".format(
                        role_name, self.role_repo_paths
                    )
                )

    def get_tasklist(self, tasklist_name):

        if tasklist_name in self.available_tasklists.keys():
            return self.available_tasklists[tasklist_name]
        else:
            raise Exception(
                "Could not find Ansible tasklist '{}' in tasklist paths: {}".format(
                    tasklist_name, self.tasklist_paths
                )
            )

    def get_repo_for_tasklist(self, tasklist_name):

        for repo, tlns in self.tasklists_per_repo.items():

            if tasklist_name in tlns:
                return repo

        return None


class NsblTasklist(Frklist):
    def __init__(
        self,
        itemlist,
        context,
        meta=None,
        vars=None,
        task_marker="task",
        meta_marker="task",
    ):

        if not isinstance(context, NsblContext):
            raise Exception("Context needs to be of type NsblContext")

        self.internal_roles = set()
        self.external_roles = set()
        self.modules_used = set()
        self.tasklist_files = {}
        self.children = []
        self.additional_files = {}

        self.task_lookup = {}

        self.task_marker = task_marker
        self.meta_marker = meta_marker

        super(NsblTasklist, self).__init__(itemlist, context, meta=meta, vars=vars)

    def expand_and_augment_tasklist(self, tasklist):

        result = []
        for task in tasklist:

            index = task[self.meta_marker]["_task_id"]

            self.task_lookup[index] = task

            name = task[self.meta_marker].get("name", None)
            command = task[self.task_marker].get("command", None)
            if name is None:
                if command is None:
                    raise Exception(
                        "Task doesn't have 'name' nor 'command' key: {}".format(task)
                    )
                name = command
                task[self.meta_marker]["name"] = command
            if command is None:
                command = name
                task[self.task_marker]["command"] = command

            temp = {
                self.task_marker: copy.deepcopy(task[self.task_marker]),
                "vars": task.get("vars", {}),
            }

            task_type = task[self.meta_marker]["type"]
            temp[self.task_marker]["type"] = task_type

            msg = task.get(self.meta_marker, {}).get("msg", None)

            # msg = temp[self.task_marker].get("__msg__", None)
            if msg is None:
                msg = task.get("doc", {}).get("msg", None)
            if msg is not None:
                temp[self.task_marker]["name"] = "[{}] {}".format(index, msg)
            else:
                temp[self.task_marker]["name"] = "[{}] {}".format(index, name)

            if temp[self.task_marker]["type"] == "ansible-role":

                if "include-type" not in temp[self.task_marker].keys():
                    temp[self.task_marker]["include-type"] = DEFAULT_INCLUDE_TYPE

                remote_role = False
                if "role_path" in temp[self.task_marker].keys():
                    path = temp[self.task_marker]["role_path"]
                else:
                    path = self.context.get_role_path(command)
                    if path == command:
                        remote_role = True
                    temp[self.task_marker]["role_path"] = path
                temp.setdefault("vars", {})["_task_id"] = index
                if not remote_role:
                    self.additional_files[path] = {
                        "type": ADD_TYPE_ROLE,
                        "target_name": command,
                    }
                else:
                    self.external_roles.add(command)

            if temp[self.task_marker]["type"] == "ansible-tasklist":
                include_type = temp[self.task_marker].get("include-type", None)
                if include_type is None:
                    include_type = DEFAULT_INCLUDE_TYPE
                    temp[self.task_marker]["include-type"] = include_type

                temp.setdefault("vars", {})["_task_id"] = index
                tasklist_var = temp[self.task_marker].get("tasklist_var", None)
                if tasklist_var is None:
                    tasklist_var = "tasklist_{}".format(command)

                tasklist_var = tasklist_var.replace("-", "_")
                tasklist_var = tasklist_var.replace(".", "_")
                temp[self.task_marker]["tasklist_var"] = tasklist_var

                # if include_type == "import":
                #     # can't think of another easy way to notify the callback
                #     # that this task has started
                #     debug_task = {}
                #     debug_task["name"] = temp[self.task_marker]["name"]
                #     debug_task["debug"] = {
                #         "msg": "Starting imported tasklist: {}".format(name)
                #     }
                #     temp[self.task_marker]["tasklist"].insert(0, debug_task)

                # temp[self.task_marker]["command"] = "{}_tasks".format(include_type)

                tasklist = self.context.get_tasklist(command)

                self.additional_files[temp[self.task_marker]["tasklist_var"]] = {
                    "type": ADD_TYPE_TASK_LIST,
                    "target_name": "{}".format(temp[self.task_marker]["tasklist_var"]),
                    "var_name": temp[self.task_marker]["tasklist_var"],
                    "tasklist": tasklist,
                }

            if "roles" in temp[self.task_marker].keys():
                roles = temp[self.task_marker]["roles"]
                if isinstance(roles, string_types):
                    roles = [roles]

                for role in roles:
                    path = self.context.get_role_path(role)
                    self.additional_files[path] = {
                        "type": ADD_TYPE_ROLE,
                        "target_name": role,
                    }
            result.append(temp)

        return result

    def get_task(self, index):

        return self.task_lookup.get(index, None)

    def render_tasklist(self, secure_vars=None, show_tasks_with_password_in_log=False):
        """Renders the playbook into a file."""

        result = []

        for t in self.itemlist:

            task = copy.deepcopy(t)
            log.debug("Task item: {}".format(task))
            name = task[self.task_marker].pop("name")
            command = task[self.task_marker].pop("command", None)
            task_type = task[self.task_marker].pop("type")
            desc = task[self.task_marker].pop("msg", None)
            # legacy
            task_desc = task[self.task_marker].pop("task-desc", None)
            if desc is None:
                desc = task_desc
            if desc is None:
                desc = name

            vars = CommentedMap()
            task_has_password = False

            for key, value in task.pop("vars").items():

                # for alias in secure_vars.keys():
                #
                #     pw_wrap_method = secure_vars[alias]["type"]
                #     if pw_wrap_method != "environment":
                #         raise NsblException(
                #             "Password-wrap method '{}' not supported in nsbl.".format(
                #                 pw_wrap_method
                #             )
                #         )
                #     value, changed = simple_replace_string_in_obj(
                #         value, alias, "{{{{ lookup('env', '{}') }}}}".format(alias)
                #     )
                #     if changed:
                #         task_has_password = True

                vars[key] = value

            task_item = CommentedMap()
            task_item["name"] = desc

            if task_type == "ansible-module":
                if command is None:
                    raise NsblException(
                        "No 'command' key specified in task: {}".format(task)
                    )
                if "free_form" in vars.keys():
                    temp = copy.deepcopy(vars)
                    free_form = temp.pop("free_form")
                    task_item[command] = free_form
                    task_item["args"] = temp
                else:
                    task_item[command] = vars
            elif task_type == "ansible-tasklist":
                include_type = task[self.task_marker]["include-type"]
                task_key = "{}_tasks".format(include_type)
                task_item[task_key] = "{{{{ {} }}}}".format(
                    task[self.task_marker]["tasklist_var"]
                )
                task_item["vars"] = vars
            elif task_type == "ansible-role":
                if command is None:
                    raise NsblException(
                        "No 'command' key specified in task: {}".format(task)
                    )
                include_type = task[self.task_marker]["include-type"]
                task_key = "{}_role".format(include_type)
                task_item[task_key] = {"name": command}
                task_item["vars"] = vars

                for additional in [
                    "allow_duplicates",
                    "defaults_from",
                    "tasks_from",
                    "vars_from",
                ]:
                    value = task[self.task_marker].get(additional, None)
                    if value is not None:
                        task_item[task_key][additional] = value

            # add the remaining key/value pairs
            unknown_keys = []
            for key, value in task[self.task_marker].items():
                if key in ANSIBLE_TASK_KEYWORDS:
                    task_item[key] = value
                else:
                    unknown_keys.append(key)

            if task_has_password and not show_tasks_with_password_in_log:
                if "no_log" not in task_item.keys():
                    task_item["no_log"] = True

            # adding 'skip' conditions
            skip_internal_list = t[self.task_marker].get("__skip_internal__", [])
            if skip_internal_list:
                when_list = []
                when = task_item.get("when", None)
                if when:
                    when_list.append("( {} )".format(when))
                for skip_item in skip_internal_list:
                    when_list.append("( not {} )".format(skip_item))

                when_string = " and ".join(when_list)
                task_item["when"] = when_string

            result.append(task_item)

        return result
