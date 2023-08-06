# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import getpass
import io
import logging
import os
import re
import shutil
import tarfile
from collections import OrderedDict
from datetime import datetime
from distutils.spawn import find_executable

import click
from cookiecutter.main import cookiecutter
from jinja2 import Environment, FileSystemLoader
from plumbum import local
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from six import string_types

from frkl import load_string_from_url_or_path, FrklistContext
from frkl.exceptions import FrklistConfigException
from frkl.utils import get_url_parents
from frutils import can_passwordless_sudo, dict_merge, is_url_or_abbrev
from .defaults import (
    DEFAULT_ENV_TYPE,
    ADD_TYPE_TASK_LIST,
    ADD_TYPE_ROLE,
    ADD_TYPE_ACTION,
    ADD_TYPE_CALLBACK,
    ADD_TYPE_FILTER,
    ADD_TYPE_LIBRARY,
    ANSIBLE_ROLE_CACHE_DIR,
    ADD_TYPE_FILES,
    ADD_TYPE_MODULE_UTIL,
    ADD_TYPE_TASK_LIST_FILE,
    TEMPLATES_FOLDER,
    MITOGEN_VERSION,
)
from .exceptions import NsblException
from .inventory import NsblInventory
from .nsbl_tasklist import NsblTasklist

try:
    set
except NameError:
    from sets import Set as set

log = logging.getLogger("nsbl")

yaml = YAML()
yaml.default_flow_style = False
yaml.preserve_quotes = True
yaml.width = 4096
# class NsblContext(FrklistContext):
#
#     def __init__(self, **kwargs):
#
#         self.kwargs = kwargs


def create_single_host_nsbl_env_from_tasklist(
    task_list,
    context,
    user=None,
    host="localhost",
    host_ip=None,
    connection_type=None,
    ssh_port=22,
    ssh_key=None,
    python_interpreter=None,
    global_task_vars=None,
    pre_tasks=None,
    gather_facts=True,
    additional_files=None,
    task_marker="task",
    meta_marker="task",
    **kwargs
):

    if user is None:
        user = getpass.getuser()

    config_dict = [{host: {"meta": {"type": "host"}, "tasks": task_list}}]

    if connection_type is None:
        if host in ["localhost", "127.0.0.1"]:
            connection_type = "local"
        else:
            connection_type = "ssh"

    connection_vars = {
        "ansible_port": ssh_port,
        "ansible_connection": connection_type,
        "ansible_user": user,
    }
    if python_interpreter is not None:
        connection_vars["ansible_python_interpreter"] = python_interpreter
    if ssh_key is not None:
        connection_vars["ansible_ssh_private_key_file"] = ssh_key
    if host_ip is not None:
        connection_vars["ansible_host"] = host_ip

    config_dict[0][host]["vars"] = connection_vars

    config = Nsbl(
        [config_dict],
        context=context,
        base_path=None,
        global_task_vars=global_task_vars,
        pre_tasks=pre_tasks,
        gather_facts=gather_facts,
        additional_files=additional_files,
        task_marker=task_marker,
        meta_marker=meta_marker,
    )

    return config


def create_nsbl_env(
    urls,
    base_path=None,
    context=None,
    default_env_type=DEFAULT_ENV_TYPE,
    additional_files=None,
    global_task_vars=None,
    task_marker="task",
    meta_marker="task",
):

    if isinstance(urls, string_types):
        urls = [urls]  # we always want a list of lists as input for the Nsbl object

    if is_url_or_abbrev(urls[0]):
        click.echo("Downloading configuration: {}".format(urls[0]))
    config_dicts = load_string_from_url_or_path(
        urls, create_python_object=True, safe_load=False
    )

    if not base_path:
        parent = get_url_parents(urls, return_list=True)
        if len(parent) > 2:
            raise NsblException(
                "Multiple base paths calculated ({}). This is not allowed as it introduces unpredictable behaviour. Please specify the base path manually.".format(
                    parent
                )
            )
        base_path = list(parent)[0]

    config = Nsbl(
        config_dicts,
        base_path=base_path,
        context=context,
        default_env_type=default_env_type,
        additional_files=additional_files,
        global_task_vars=global_task_vars,
        task_marker=task_marker,
        meta_marker=meta_marker,
    )

    return config


# def expand_nsbl_config(configs):
#     """Expands the nsbl configuration.
#
#     Args:
#         configs (list): a list of configuration items
#     """
#
#     chain = [FrklProcessor(NSBL_INVENTORY_BOOTSTRAP_FORMAT)]
#     f = Frkl(configs, chain)
#     result = f.process()
#
#     return result

DEFAULT_ELEVATED_PERMISSIONS_REQUIRED = True
DEFAULT_PASSWORDLESS_SUDO_POSSIBLE = False


class Nsbl(object):
    """Holds and parses configuration to generate Ansible task lists and inventories.

    Args:
        config (list): a list of configuration items
        base_path (str): the base path to use for relative task list imports etc.
        context (NsblContext): the context for this environment
        default_env_type (str): the type a environment is if it is not explicitely specified, either ENV_TYPE_HOST or ENV_TYPE_GROUP
        additional_files (dict): a dict of additional files to copy into the Ansible environment
        # allow_external_roles (bool): whether to allow the downloading of external roles
        global_task_vars (dict): global variables for all tasks (will still be overwritten by task-list specific task vars if present)
        pre_tasks (list): a list of tasks that will be inserted into every playbook
        gather_facts (boolean): whether the gather_facts step should be enabled/disabled
        task_marker (string): the marker string that indicates a task metadata key
        meta_marker (string): the maker string that indicates a 'meta' metadata key (for getting the description of a task)
    """

    def __init__(
        self,
        config,
        base_path=None,
        context=None,
        default_env_type=DEFAULT_ENV_TYPE,
        additional_files=None,
        global_task_vars=None,
        pre_tasks=None,
        gather_facts=True,
        task_marker="task",
        meta_marker="task",
    ):

        self.base_path = base_path
        self.plays = CommentedMap()
        self.internal_roles = set()
        self.external_roles = set()

        self.task_marker = task_marker
        self.meta_marker = meta_marker

        self.pre_tasks = pre_tasks
        self.gather_facts = gather_facts

        if global_task_vars is None:
            global_task_vars = {}
        self.global_task_vars = global_task_vars

        self.config = config
        if context is None:
            context = FrklistContext()
        elif isinstance(context, (dict, CommentedMap, OrderedDict)):
            context = FrklistContext(**context)
        elif not isinstance(context, FrklistContext):
            raise FrklistConfigException(
                "Invalid type for context: {}".format(type(context))
            )
        self.context = context

        self.default_env_type = default_env_type

        if additional_files is None:
            additional_files = {}
        self.additional_files = copy.deepcopy(additional_files)

        self.inventory = NsblInventory.create(
            self.config, default_env_type=self.default_env_type, pre_chain=[]
        )

        tl_id = 0
        for tasks in self.inventory.tasks:

            task_list_meta = tasks["meta"]
            env_name = task_list_meta["name"]
            env_id = task_list_meta["_env_id"]

            # task_list_vars = tasks.get("vars", {})
            # print(task_list_vars)
            # dict_merge(task_list_vars, self.global_task_vars, copy_dct=False)
            task_list_vars = self.global_task_vars

            task_list = tasks["tasks"]

            meta = {}
            meta["tasklist_id"] = tl_id
            meta["env_id"] = env_id
            meta["env_name"] = env_name
            # meta["tasklist_parent"] = self.base_path

            tl = NsblTasklist(
                task_list,
                context=self.context,
                meta=meta,
                vars=task_list_vars,
                task_marker=self.task_marker,
                meta_marker=self.meta_marker,
            )
            self.plays["{}_{}".format(env_name, env_id)] = {
                "task_list": tl,
                "meta": task_list_meta,
                "env_id": env_id,
                "env_name": env_name,
            }

            tl_id = tl_id + 1
            self.internal_roles.update(tl.internal_roles)
            self.external_roles.update(tl.external_roles)

    def get_play(self, env_name, env_id):

        return self.plays.get("{}_{}".format(env_name, env_id), None)

    def get_tasklist(self, env_name, env_id):

        return self.get_play(env_name, env_id)["task_list"]

    def render(
        self,
        env_dir,
        global_vars=None,
        extract_vars=True,
        force=False,
        elevated_permissions_required=None,
        passwordless_sudo_possible=None,
        secure_vars=None,
        ansible_args="",
        callback="default",
        force_update_roles=False,
        add_timestamp_to_env=False,
        add_symlink_to_env=False,
        extra_paths=None,
        show_tasks_with_password_in_log=False,
        use_mitogen=False,
        use_ara=False,
        parent_task=None,
    ):
        """Creates the ansible environment in the folder provided.

        Args:
          env_dir (str): the folder where the environment should be created
          global_vars (dict): vars to be rendered as global on top of a playbook
          extract_vars (bool): whether to extract a hostvars and groupvars directory for the inventory (True), or render a dynamic inventory script for the environment (default, True) -- Not supported at the moment
          force (bool): overwrite environment if already present at the specified location, use with caution because this might delete an important folder if you get the 'target' dir wrong
          elevated_permissions_required (bool): whether to include the '--ask-become-pass' arg to the ansible-playbook call
          passwordless_sudo_possible (bool): whether the user executing this run does have passwordless sudo permissions
          secure_vars (dict): vars to keep in a vault (not implemented yet)
          ansible_args (str): parameters to give to ansible-playbook (like: "-vvv")
          callback (str): name of the callback to use, default: nsbl_internal
          force_update_roles (bool): whether to overwrite external roles that were already downloaded
          add_timestamp_to_env (bool): whether to add a timestamp to the env_dir -- useful for when this is called from other programs (e.g. freckles)
          add_symlink_to_env (str): whether to add a symlink to the current env from a fixed location (useful to archive all runs/logs)
          extra_paths (str): a list of of extra paths to be exported before the ansible playbook run
          show_tasks_with_password_in_log (bool): whether to show tasks that contain a password variable in the log (only enable for debugging!)
          use_mitogen (bool): use mitogen as a strategy plugin to speed up execution
          use_ara (bool): use ara (https://ara.readthedocs.io)
          parent_task (TaskDetail): parent task (for task callbacks, optional)
        """
        if elevated_permissions_required is None:
            elevated_permissions_required = DEFAULT_ELEVATED_PERMISSIONS_REQUIRED

        if not isinstance(elevated_permissions_required, bool):
            raise Exception("'ask_become_pass' needs to be boolean value")

        if extra_paths is None:
            extra_paths = []

        if passwordless_sudo_possible is None:
            if self.inventory.localhost_only:
                passwordless_sudo_possible = can_passwordless_sudo()
            else:
                passwordless_sudo_possible = DEFAULT_PASSWORDLESS_SUDO_POSSIBLE

        env_dir = os.path.expanduser(env_dir)
        if add_timestamp_to_env:
            start_date = datetime.now()
            date_string = start_date.strftime("%y%m%d_%H_%M_%S")
            dirname, basename = os.path.split(env_dir)
            env_dir = os.path.join(dirname, "{}_{}".format(basename, date_string))

        if global_vars is None:
            global_vars = {}

        result = {}
        result["env_dir"] = env_dir
        if os.path.exists(env_dir) and force:
            shutil.rmtree(env_dir)

        inventory_dir = os.path.join(env_dir, "inventory")
        result["inventory_dir"] = inventory_dir

        if extract_vars:
            inv_target = "../inventory/hosts"
        else:
            inv_target = "../inventory/inventory"

        result["extract_vars"] = extract_vars

        playbook_dir = os.path.join(env_dir, "plays")
        result["playbook_dir"] = playbook_dir
        # roles_base_dir = os.path.join(env_dir, "roles")
        result["roles_base_dir"] = playbook_dir

        # if password is None:
        #     if elevated_permissions_required:
        #         if passwordless_sudo_possible:
        #             ask_sudo = False
        #         else:
        #             ask_sudo = True
        #     else:
        #         ask_sudo = False
        # else:
        #     ask_sudo = True

        all_plays_name = "all_plays.yml"
        result["default_playbook_name"] = all_plays_name

        ansible_playbook_args = ansible_args
        result["ansible_playbook_cli_args"] = ansible_playbook_args
        result["run_playbooks_script"] = os.path.join(env_dir, "run_all_plays.sh")

        ara_base = None
        if use_ara:
            try:
                import ara

                ara_base = os.path.dirname(ara.__file__)
            except (Exception):
                ara_base = None
                log.warning("Did not find 'ara' in python env, not using it...")
                pass

        if ara_base:
            callback_plugins_list = "callback_plugins:{}/plugins/callbacks".format(
                ara_base
            )
            action_plugins_list = "action_plugins:{}/plugins/actions".format(ara_base)
            library_plugins_list = "library:{}/plugins/modules".format(ara_base)
            module_utils_list = "module_utils:{}/plugins/module_utils".format(ara_base)
        else:
            callback_plugins_list = "callback_plugins"
            action_plugins_list = "action_plugins"
            library_plugins_list = "library"
            module_utils_list = "module_utils"

        if not use_mitogen:
            mitogen = ""
        else:
            mitogen_path = "../opt/mitogen-{}".format(MITOGEN_VERSION)
            mitogen = os.path.join(
                mitogen_path, "ansible_mitogen", "plugins", "strategy"
            )

        cookiecutter_details = {
            "inventory": inv_target,
            "env_dir": env_dir,
            "extra_paths": extra_paths,
            "playbook_dir": playbook_dir,
            "ansible_playbook_args": ansible_playbook_args,
            "library_path": library_plugins_list,
            "action_plugins_path": action_plugins_list,
            "module_utils_path": module_utils_list,
            "extra_script_commands": "",
            "ask_sudo": "",
            "playbook": all_plays_name,
            "callback_plugins": callback_plugins_list,
            "callback_plugin_name": callback,
            "callback_whitelist": "default_to_file",
            "mitogen": mitogen,
        }

        log.debug("Creating build environment from template...")
        log.debug("Using cookiecutter details: {}".format(cookiecutter_details))

        template_path = os.path.join(
            os.path.dirname(__file__), "external", "nsbl-environment-template"
        )

        cookiecutter(template_path, extra_context=cookiecutter_details, no_input=True)

        if add_symlink_to_env:
            link_path = os.path.expanduser(add_symlink_to_env)
            if os.path.exists(link_path) or os.path.islink(link_path):
                os.unlink(link_path)
            link_parent = os.path.abspath(os.path.join(link_path, os.pardir))
            try:
                os.makedirs(link_parent)
            except (Exception):
                pass

            os.symlink(env_dir, link_path)

            result["env_dir_link"] = link_path

        # write inventory
        if extract_vars:
            self.inventory.extract_vars(inventory_dir)

        self.inventory.write_inventory_file_or_script(
            inventory_dir, extract_vars=extract_vars
        )

        # extract mitogen
        if use_mitogen:
            mitogen_archive_path = os.path.join(
                os.path.dirname(__file__),
                "external",
                "mitogen",
                "mitogen-{}.tar.gz".format(MITOGEN_VERSION),
            )
            opt_path = os.path.join(env_dir, "opt")
            if not os.path.exists(opt_path):
                os.makedirs(opt_path)
            mitogen_archive = tarfile.open(mitogen_archive_path)
            mitogen_archive.extractall(path=opt_path)
            mitogen_archive.close()

        # write roles
        all_playbooks = []
        all_playbook_names = []
        ext_roles = []
        task_details = []

        for play, task_list_details in self.plays.items():

            # td = copy.deepcopy(task_list_details)
            tasks = task_list_details["task_list"]
            id = task_list_details["env_id"]
            name = task_list_details["env_name"]
            playbook_name = "play_{}_{}.yml".format(name, id)
            playbook_file = os.path.join(playbook_dir, playbook_name)

            playbook_vars = {}
            dict_merge(playbook_vars, global_vars, copy_dct=False)
            dict_merge(playbook_vars, tasks.vars, copy_dct=False)
            playbook_vars["_env_id"] = id
            playbook_vars["_env_name"] = name

            task_list = tasks.render_tasklist(
                secure_vars=secure_vars,
                show_tasks_with_password_in_log=show_tasks_with_password_in_log,
            )

            if self.pre_tasks:
                # TODO: clean that up, tasks could now go directly into the playbook
                playbook_pre_file = os.path.join(
                    playbook_dir, "pre_{}".format(playbook_name)
                )
                tasklist_name = "pre_tasks_{}_{}".format(name, id)
                tasklist_name = re.sub(r"\W+", "", tasklist_name)
                tl_pre = {
                    "type": ADD_TYPE_TASK_LIST,
                    "target_name": "{}.yml".format(tasklist_name),
                    "tasklist": self.pre_tasks,
                    "var_name": tasklist_name,
                }
                self.additional_files[tasklist_name] = tl_pre
                import_pre_tasks = {
                    "name": "[importing host preparation tasks]",
                    "import_tasks": "{{{{ {} }}}}".format(tasklist_name),
                }
                playbook_dict_pre = CommentedMap()
                playbook_dict_pre["hosts"] = name
                playbook_dict_pre["strategy"] = "linear"
                playbook_dict_pre["gather_facts"] = False
                playbook_dict_pre["vars"] = playbook_vars
                playbook_dict_pre["tasks"] = [import_pre_tasks]
                all_playbooks.append(
                    {
                        "name": "pre_{}".format(playbook_name),
                        "dict": playbook_dict_pre,
                        "file": playbook_pre_file,
                    }
                )
                all_playbook_names.append("pre_{}".format(playbook_name))

            playbook_dict = CommentedMap()
            playbook_dict["hosts"] = name

            playbook_dict["gather_facts"] = self.gather_facts

            playbook_dict["vars"] = playbook_vars
            playbook_dict["tasks"] = task_list

            # td["playbook"] = playbook_dict
            all_playbooks.append(
                {"name": playbook_name, "dict": playbook_dict, "file": playbook_file}
            )
            all_playbook_names.append(playbook_name)

            dict_merge(self.additional_files, tasks.additional_files, copy_dct=False)

            if tasks.external_roles:
                for n in tasks.external_roles:
                    if n not in ext_roles:
                        ext_roles.append(n)

        # copy external files
        external_files_vars = {}

        action_plugins_target = os.path.join("plays", "action_plugins")
        callback_plugins_target = os.path.join("plays", "callback_plugins")
        filter_plugins_target = os.path.join("plays", "filter_plugins")
        library_plugins_target = os.path.join("plays", "library")
        module_utils_target = os.path.join("plays", "module_utils")
        roles_target = os.path.join("roles", "internal")
        task_lists_target = "task_lists"
        files_target = "files"

        additional_files = copy.deepcopy(self.additional_files)

        for path, details in additional_files.items():

            file_type = details["type"]

            # if not os.path.exists(path):
            #     import pp
            #     print(path)
            #     pp(details)
            #     raise NsblException(
            #         "Resource '{}' not available: {}".format(file_type, path)
            #     )

            playbook_var_name = details.get("var_name", None)
            file_name = details["target_name"]

            skip_copy = False
            if file_type == ADD_TYPE_TASK_LIST:
                # content = details["tasklist"]
                target = os.path.join(env_dir, task_lists_target, file_name)
                log.debug("Render 'ansible'-type tasklist: {}".format(path))

                target_parent = os.path.dirname(target)
                if not os.path.exists(target_parent):
                    os.makedirs(target_parent)

                with io.open(target, "w", encoding="utf-8") as tlf:
                    yaml.dump(details["tasklist"], tlf)

                skip_copy = True
                playbook_var_value = os.path.join(
                    "{{ playbook_dir }}", "..", task_lists_target, file_name
                )

            elif file_type == ADD_TYPE_ROLE:
                target = os.path.join(env_dir, roles_target, file_name)
                playbook_var_value = None
                copy_source_type = "dir"
            elif file_type == ADD_TYPE_ACTION:
                target = os.path.join(env_dir, action_plugins_target, file_name)
                playbook_var_value = None
                copy_source_type = "file"
            elif file_type == ADD_TYPE_CALLBACK:
                target = os.path.join(env_dir, callback_plugins_target, file_name)
                playbook_var_value = None
                copy_source_type = "file"
            elif file_type == ADD_TYPE_FILTER:
                target = os.path.join(env_dir, filter_plugins_target, file_name)
                playbook_var_value = None
                copy_source_type = "file"
            elif file_type == ADD_TYPE_LIBRARY:
                target = os.path.join(env_dir, library_plugins_target, file_name)
                playbook_var_value = None
                copy_source_type = "file"
            elif file_type == ADD_TYPE_MODULE_UTIL:
                target = os.path.join(env_dir, module_utils_target, file_name)
                copy_source_type = "file"
                playbook_var_value = None
            elif file_type == ADD_TYPE_FILES:
                target = os.path.join(env_dir, files_target, file_name)
                copy_source_type = "file"
                playbook_var_value = None
            elif file_type == ADD_TYPE_TASK_LIST_FILE:
                target = os.path.join(env_dir, task_lists_target, file_name)
                copy_source_type = "file"
                playbook_var_value = None
            else:
                raise NsblException("Invalid external file type: {}".format(file_type))

            if not skip_copy:
                log.debug("Copying {} '{}': {}".format(file_type, file_name, target))
                target_parent = os.path.dirname(target)
                if not os.path.exists(target_parent):
                    os.makedirs(target_parent)
                if not os.path.isdir(os.path.realpath(target_parent)):
                    raise NsblException(
                        "Can't copy files to '{}': not a directory".format(
                            target_parent
                        )
                    )

                if copy_source_type == "file":
                    shutil.copyfile(path, target)
                else:
                    shutil.copytree(path, target)

            if playbook_var_value:
                if playbook_var_name in external_files_vars.keys():
                    raise NsblException(
                        "Duplicate key for external files: {}".format(playbook_var_name)
                    )
                log.debug(
                    "Setting variable '{}' to: {}".format(
                        playbook_var_name, playbook_var_value
                    )
                )
                external_files_vars[playbook_var_name] = playbook_var_value

        # render all playbooks
        for playbook in all_playbooks:

            playbook_file = playbook["file"]
            playbook_dict = playbook["dict"]

            # adding external files vars
            dict_merge(
                playbook_dict.setdefault("vars", {}),
                external_files_vars,
                copy_dct=False,
            )

            with io.open(playbook_file, "w", encoding="utf-8") as pf:
                yaml.dump([playbook_dict], pf)

        result["task_details"] = task_details
        result["additional_files"] = self.additional_files
        jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER))
        template = jinja_env.get_template("play.yml")
        output_text = template.render(playbooks=all_playbook_names)

        all_plays_file = os.path.join(env_dir, "plays", all_plays_name)
        result["all_plays_file"] = all_plays_file
        with io.open(all_plays_file, "w", encoding="utf-8") as text_file:
            text_file.write(output_text)

        if ext_roles:

            ext_roles_target = os.path.join(env_dir, "roles", "external")
            # render roles_requirements.yml
            jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER))
            roles_requirements_file = os.path.join(
                ext_roles_target, "roles_requirements.yml"
            )

            if not os.path.exists(ext_roles_target):
                os.makedirs(ext_roles_target)

            roles_to_copy = {}
            for role in ext_roles:
                role_src = os.path.join(ANSIBLE_ROLE_CACHE_DIR, role)
                target = os.path.join(ext_roles_target, role)
                roles_to_copy[role_src] = target

                template = jinja_env.get_template("external_role.yml")
                output_text = template.render(role={"src": role, "name": role})
                with io.open(roles_requirements_file, "a", encoding="utf-8") as myfile:
                    myfile.write(output_text)

            # download external roles
            role_requirement_file = os.path.join(
                env_dir, "roles", "external", "roles_requirements.yml"
            )

            if not os.path.exists(ANSIBLE_ROLE_CACHE_DIR):
                os.makedirs(ANSIBLE_ROLE_CACHE_DIR)

            command = [
                "install",
                "-r",
                role_requirement_file,
                "-p",
                ANSIBLE_ROLE_CACHE_DIR,
            ]
            if force_update_roles:
                command.append("--force")
            log.debug("Downloading and installing external roles...")

            if parent_task:
                download_task = parent_task.add_subtask(
                    task_name="download external roles",
                    msg="downloading role(s): {}".format(" ".join(ext_roles)),
                )
            else:
                download_task = None
                click.echo("Managing external roles...")

            path = os.environ["PATH"] + ":" + extra_paths
            galaxy_exe = find_executable("ansible-galaxy", path=path)
            if not galaxy_exe:
                raise Exception("Could not find 'ansible-galaxy' executable")
            ansible_galaxy = local[galaxy_exe]

            try:
                rc, stdout, stderr = ansible_galaxy.run(command)

                if download_task is None:
                    for line in stdout.split("\n"):
                        if (
                            "already installed" not in line
                            and "--force to change" not in line
                            and "unspecified" not in line
                        ):
                            # log.debug("Installing role: {}".format(line.encode('utf8')))

                            click.echo("  {}".format(line.encode("utf8")), nl=False)
                else:
                    if rc == 0:
                        success = True
                    else:
                        success = False

                    download_task.finish(
                        success=success,
                        msg=stdout,
                        error_msg=stderr,
                        skipped=False,
                        changed=True,
                    )

            except (Exception) as e:

                if download_task is not None:
                    download_task.finish(
                        success=False, error_msg=str(e), skipped=False, changed=True
                    )
                raise e

            if roles_to_copy:
                if parent_task is not None:
                    copy_task = parent_task.add_subtask(
                        task_name="copy roles",
                        msg="copying role(s) into Ansible environment",
                    )
                else:
                    copy_task = None
                    if len(ext_roles) == 1:

                        click.echo(
                            "Copying role from Ansible cache: {}".format(ext_roles[0])
                        )
                    else:
                        click.echo("Copying roles from Ansible cache:")
                        for r in ext_roles:
                            click.echo("  - {}".format(r))

                for src, target in roles_to_copy.items():
                    log.debug("Coping external role: {} -> {}".format(src, target))
                    shutil.copytree(src, target)

                if copy_task is not None:
                    copy_task.finish(success=True, skipped=False, changed=True)

        return result
