# -*- coding: utf-8 -*-

import copy
import json
import logging
import os
from distutils.spawn import find_executable

from plumbum import local
from six import string_types

from freckles.adapters import FrecklesAdapter
from freckles.defaults import (
    EXTERNAL_FOLDER as FRECKLES_EXTERNAL_FOLDER,
    FRECKLET_KEY_NAME,
    VARS_KEY,
    FRECKLES_VENV_ENV_PATH,
    FRECKLES_CONDA_ENV_PATH,
    TASK_KEY_NAME,
    FRECKLES_CONDA_INSTALL_PATH,
)
from freckles.exceptions import FrecklesConfigException
from nsbl.defaults import (
    ADD_TYPE_FILES,
    ADD_TYPE_CALLBACK,
    ADD_TYPE_ACTION,
    ADD_TYPE_LIBRARY,
    ADD_TYPE_FILTER,
    ADD_TYPE_TASK_LIST_FILE,
)
from nsbl.nsbl import create_single_host_nsbl_env_from_tasklist
from nsbl.nsbl_tasklist import NsblContext
from nsbl.runner import NsblRunner
from .defaults import (
    NSBL_CONFIG_SCHEMA,
    NSBL_DEFAULT_FRECKLET_REPO,
    NSBL_EXTRA_CALLBACKS,
    NSBL_EXTRA_PLUGINS,
    NSBL_INTERNAL_TASKLIST_REPO,
    NSBL_RUN_CONFIG_SCHEMA,
    NSBL_DEFAULT_ROLE_REPO,
    NSBL_DEFAULT_TASKLIST_REPO,
    NSBL_COMMUNITY_FRECKLET_REPO,
    NSBL_COMMUNITY_ROLE_REPO,
    NSBL_COMMUNITY_TASKLIST_REPO,
)
from .nsbl_freckles_callback import NsblPrintCallbackAdapter

log = logging.getLogger("freckles")

DEFAULT_ADDITIONAL_FILES = [
    {
        "path": os.path.join(FRECKLES_EXTERNAL_FOLDER, "scripts", "freckles_facts.sh"),
        "type": ADD_TYPE_FILES,
    },
    {
        "path": os.path.join(FRECKLES_EXTERNAL_FOLDER, "scripts", "freckle_folders.sh"),
        "type": ADD_TYPE_FILES,
    },
    {
        "path": os.path.join(NSBL_EXTRA_CALLBACKS, "default_to_file.py"),
        "type": ADD_TYPE_CALLBACK,
    },
    {
        "path": os.path.join(NSBL_EXTRA_CALLBACKS, "freckles_callback.py"),
        "type": ADD_TYPE_CALLBACK,
    },
    {
        "path": os.path.join(NSBL_EXTRA_PLUGINS, "action_plugins", "install.py"),
        "type": ADD_TYPE_ACTION,
    },
    {
        "path": os.path.join(NSBL_EXTRA_PLUGINS, "library", "install.py"),
        "type": ADD_TYPE_LIBRARY,
    },
    {
        "path": os.path.join(NSBL_EXTRA_PLUGINS, "library", "stow.py"),
        "type": ADD_TYPE_LIBRARY,
    },
    {
        "path": os.path.join(NSBL_EXTRA_PLUGINS, "library", "vagrant_plugin.py"),
        "type": ADD_TYPE_LIBRARY,
    },
    {
        "path": os.path.join(
            NSBL_EXTRA_PLUGINS, "action_plugins", "frecklet_result.py"
        ),
        "type": ADD_TYPE_ACTION,
    },
    {
        "path": os.path.join(NSBL_EXTRA_PLUGINS, "library", "frecklet_result.py"),
        "type": ADD_TYPE_LIBRARY,
    },
    {
        "path": os.path.join(
            NSBL_EXTRA_PLUGINS, "action_plugins", "set_platform_fact.py"
        ),
        "type": ADD_TYPE_ACTION,
    },
    {
        "path": os.path.join(NSBL_EXTRA_PLUGINS, "library", "set_platform_fact.py"),
        "type": ADD_TYPE_LIBRARY,
    },
    {
        "path": os.path.join(NSBL_EXTRA_PLUGINS, "library", "freckles_facts.py"),
        "type": ADD_TYPE_LIBRARY,
    },
    {
        "path": os.path.join(NSBL_EXTRA_PLUGINS, "action_plugins", "freckles_facts.py"),
        "type": ADD_TYPE_ACTION,
    },
    {
        "path": os.path.join(NSBL_EXTRA_PLUGINS, "library", "conda.py"),
        "type": ADD_TYPE_LIBRARY,
    },
    {
        "path": os.path.join(NSBL_EXTRA_PLUGINS, "library", "nix.py"),
        "type": ADD_TYPE_LIBRARY,
    },
    {
        "path": os.path.join(NSBL_EXTRA_PLUGINS, "library", "asdf.py"),
        "type": ADD_TYPE_LIBRARY,
    },
    # {
    #     "path": os.path.join(NSBL_EXTRA_PLUGINS, "module_utils", "freckles_utils.py"),
    #     "type": ADD_TYPE_MODULE_UTIL,
    # },
    # {
    #     "path": os.path.join(NSBL_ROLES, "package-management", "freckfrackery.install"),
    #     "type": ADD_TYPE_ROLE,
    # },
    # {
    #     "path": os.path.join(NSBL_ROLES, "package-management", "freckfrackery.install-pkg-mgrs"),
    #     "type": ADD_TYPE_ROLE,
    # },
    {
        "path": os.path.join(
            NSBL_EXTRA_PLUGINS, "filter_plugins", "freckles_filters.py"
        ),
        "type": ADD_TYPE_FILTER,
    },
    {
        "path": os.path.join(NSBL_INTERNAL_TASKLIST_REPO, "box_basics.yml"),
        "type": ADD_TYPE_TASK_LIST_FILE,
    },
    {
        "path": os.path.join(NSBL_INTERNAL_TASKLIST_REPO, "box_basics_root.yml"),
        "type": ADD_TYPE_TASK_LIST_FILE,
    },
    {
        "path": os.path.join(NSBL_INTERNAL_TASKLIST_REPO, "freckles_basic_facts.yml"),
        "type": ADD_TYPE_TASK_LIST_FILE,
    },
]


def generate_pre_tasks(
    minimal_facts=True, box_basics=True, box_basics_non_sudo=False, freckles_facts=True
):
    """Generates a list of tasks that will end up in a playbooks pre_tasks variable.

    Args:
        minimal_facts (bool): whether to run a basic shell script to gather some basic facts (this doesn't require Python on the target machine, but can find out whether Python is available.
        box_basics (bool): whether to install a minimal set to be able to run common Ansible modules on this machine
        box_basics_non_sudo (bool): whether to run the 'non-sudo' version of box basics (not implemented yet)
        freckles_facts (bool): whether to run the freckles facts module

    Returns:
        tuple: a tuple in the form: (task_list, gather_facts_included), gather_facts_included indicates whether the pre_tasks will run gather_facts at some stage (so it doesn't need to be executed twice.
    """

    gather_facts_included = False
    pre_tasks = []

    # check_script_location = os.path.join(
    #     "{{ playbook_dir }}", "..", "files", "freckles_facts.sh"
    # )

    # TODO: this doesn't really do anything at the moment, vars are hardcoded in freckles_facts.sh
    # check_executables = [
    #     "cat",
    #     "wget",
    #     "curl",
    #     "python",
    #     "python2",
    #     "python2.7",
    #     "python3",
    #     "python3.6",
    #     "vagrant",
    #     "pip",
    #     "conda",
    #     "nix",
    #     "asdf",
    #     "rsync",
    # ]
    # check_python_modules = ["zipfile"]
    # pre_path = []
    # post_path = []
    # check_freckle_files = []
    # check_directories = []
    # freckles_facts_environment = (
    #     {
    #         "FRECKLES_CHECK_EXECUTABLES": ":".join(check_executables),
    #         "FRECKLES_CHECK_DIRECTORIES": ":".join(check_directories),
    #         "FRECKLES_PRE_PATH": ":".join(pre_path),
    #         "FRECKLES_POST_PATH": ":".join(post_path),
    #         "FRECKLES_CHECK_FRECKLE_FILES": ":".join(check_freckle_files),
    #         "FRECKLES_CHECK_PYTHON_MODULES": ":".join(check_python_modules),
    #     },
    # )

    if minimal_facts or box_basics or freckles_facts:
        temp = [
            {
                "name": "[-1000][testing connectivity]",
                "raw": 'sh -c "true"',
                "ignore_errors": False,
                "changed_when": False,
            },
            # {
            #     "name": "[-1000][checking whether box already prepared]",
            #     "raw": 'sh -c "test -e $HOME/.local/share/freckles/.box_basics && echo 1 || echo 0"',
            #     "ignore_errors": True,
            #     "register": "box_basics_exists",
            # },
            # {
            #     "name": "[setting box_basics var]",
            #     "set_fact": {
            #         "box_basics": "{{ box_basics_exists.stdout_lines[0] | bool }}",
            #         "freckles_environment": freckles_facts_environment,
            #     },
            # },
            {
                "name": "[getting box basic facts]",
                "include_tasks": "{{ playbook_dir }}/../task_lists/freckles_basic_facts.yml",
            },
        ]
        pre_tasks.extend(temp)

    if box_basics or freckles_facts:

        gather_facts_included = True
        temp = [
            {
                "name": "[preparing box basics]",
                "include_tasks": "{{ playbook_dir }}/../task_lists/box_basics.yml",
                # "when": "not box_very_basics['root_init_done']",
            },
            # {
            #     "name": "[gathering facts]",
            #     "setup": {},
            #     "tags": "always",
            #     "when": "box_very_basics['root_init_done']",
            # },
        ]
        pre_tasks.extend(temp)

    if freckles_facts:

        pre_tasks.append(
            {
                "name": "[gathering freckles-specific facts]",
                "freckles_facts": {"executables": ["unzip"]},
            }
        )

    return {"pre_tasks": pre_tasks, "gather_facts": not gather_facts_included}


def generate_additional_files_dict():

    additional_files = {}

    for f in DEFAULT_ADDITIONAL_FILES:

        path = f["path"]
        if not os.path.exists(path):
            raise FrecklesConfigException("File '{}' not available".format(path))

        f_type = f["type"]
        target_name = f.get("target_name", os.path.basename(path))

        additional_files[path] = {"type": f_type, "target_name": target_name}

        license_path = path + ".license"
        if os.path.exists(license_path):
            target_name_license = target_name + ".license"
            additional_files[license_path] = {
                "type": f["type"],
                "target_name": target_name_license,
            }

    return additional_files


class FrecklesAdapterNsbl(FrecklesAdapter):
    def __init__(self, name, context):

        super(FrecklesAdapterNsbl, self).__init__(
            adapter_name=name,
            context=context,
            config_schema=NSBL_CONFIG_SCHEMA,
            run_config_schema=NSBL_RUN_CONFIG_SCHEMA,
        )

        self._nsbl_context = None

    def get_resources_for_task(self, task):

        # output(task, output_type="yaml")

        role_paths = []
        if task[FRECKLET_KEY_NAME]["type"] == "ansible-role":
            role_name = task[TASK_KEY_NAME]["command"]
            path = self.nsbl_context.get_role_path(role_name)
            role_paths.append(path)

        roles = task.get(TASK_KEY_NAME, {}).get("roles", [])

        for role_name in roles:
            path = self.nsbl_context.get_role_path(role_name)
            if path not in role_paths:
                role_paths.append(path)

        tasklist_paths = []
        if task[FRECKLET_KEY_NAME]["type"] == "ansible-tasklist":
            tasklist_name = task[TASK_KEY_NAME]["command"]
            path = self.nsbl_context.get_tasklist(tasklist_name)
            tasklist_paths.append(path)

        tasklists = task.get(TASK_KEY_NAME, {}).get("ansible-tasklists", [])
        for tasklist_name in tasklists:
            path = self.nsbl_context.get_tasklist(tasklist_name)
            if path not in tasklist_paths:
                tasklist_paths.append(path)

        return {"roles": role_paths, "ansible-tasklists": tasklist_paths}

    def prepare_execution_requirements(self, run_config, parent_task):

        frkl_pkg = self.context.frkl_pkg

        ansible_exe = find_executable(
            "ansible-playbook",
            path=":".join(
                frkl_pkg.lookup_paths(incl_system_path=False, include_frozen=False)
            ),
        )

        if ansible_exe:
            # Test whether it works, could be a pyenv shim
            a_ex = local[ansible_exe]

            works = False
            try:
                rc, stdout, stderr = a_ex.run(["--version"])
                works = rc == 0
            except (Exception):
                log.debug(
                    "Can't use included ansible*pex file, wrong python version most likley..."
                )
                pass

            if not works:
                ansible_exe = None

        # if not ansible_exe:
        #     ansible_exe_pex = find_executable(
        #         "ansible-playbook",
        #         path=":".join(
        #             frkl_pkg.lookup_paths(incl_system_path=True, include_frozen=False)
        #         ),
        #     )
        #
        #     if ansible_exe_pex:
        #
        #         a_pex = local[ansible_exe_pex]
        #
        #         works = False
        #         try:
        #             rc, stdout, stderr = a_pex.run(["--version"])
        #             works = rc == 0
        #         except (Exception):
        #             log.debug(
        #                 "Can't use included ansible*pex file, wrong python version most likley..."
        #             )
        #             pass
        #
        #         if works:
        #             ansible_exe = ansible_exe_pex

        if ansible_exe:
            # check whether it works, could be it is a pex file for the wrong version of python

            return

        prepare_task = parent_task.add_subtask(
            task_name="preparing Ansible environment",
            msg="preparing Ansible environment",
            category="adapter_prepare",
        )

        use_env = True
        if use_env:
            package_list = [
                "ansible==2.8.0",
                "jmespath==0.9.4",
                "pywinrm==0.3.0",
                "hcloud",
            ]
            if run_config.get("use_mitogen", False):
                package_list.append("mitogen==0.2.6")

            frkl_pkg.ensure_python_packages(
                package_list=package_list,
                allow_current=False,
                venv_path=FRECKLES_VENV_ENV_PATH,
                conda_path=FRECKLES_CONDA_ENV_PATH,
                conda_install_path=FRECKLES_CONDA_INSTALL_PATH,
                env_type="auto",
                parent_task=prepare_task,
                system_site_packages=True,
            )

        prepare_task.finish()

    @property
    def nsbl_context(self):
        """Calculate the context from the available repositories and config."""

        if self._nsbl_context is None:
            role_repos = self.resource_folder_map.get("roles", [])
            tasklist_repos = self.resource_folder_map.get("ansible-tasklists", [])

            urls = {}
            role_paths = []
            for rr in role_repos:
                path = rr["path"]
                if path not in role_paths:
                    role_paths.append(path)
            urls["roles"] = role_paths
            tasklist_paths = []
            for tlr in tasklist_repos:
                path = tlr["path"]
                if path not in tasklist_paths:
                    tasklist_paths.append(path)
            urls["tasklists"] = tasklist_paths

            try:
                allow_remote = self.config_value("allow_remote")
            except (Exception):
                allow_remote = False
            try:
                allow_remote_roles = self.config_value("allow_remote_roles")
            except (Exception):
                allow_remote_roles = False
            try:
                allow_remote_tasklists = self.config_value("allow_remote_tasklists")
            except (Exception):
                allow_remote_tasklists = False

            if allow_remote_roles is None:
                allow_remote_roles = allow_remote
            if allow_remote_tasklists is None:
                allow_remote_tasklists = allow_remote

            self._nsbl_context = NsblContext(
                urls=urls,
                allow_external_roles=allow_remote_roles,
                allow_external_tasklists=allow_remote_tasklists,
            )

        return self._nsbl_context

    # def get_config_schema(self):
    #
    #     return NSBL_CONFIG_SCHEMA
    #
    # def get_run_config_schema(self):
    #
    #     return NSBL_RUN_CONFIG_SCHEMA

    def get_folders_for_alias(self, alias):

        if alias == "default":

            return [
                "frecklets::{}".format(NSBL_DEFAULT_FRECKLET_REPO),
                "roles::{}".format(NSBL_DEFAULT_ROLE_REPO),
                "ansible-tasklists::{}".format(NSBL_DEFAULT_TASKLIST_REPO),
            ]

        elif alias == "community":

            return [
                "frecklets::{}".format(NSBL_COMMUNITY_FRECKLET_REPO),
                "roles::{}".format(NSBL_COMMUNITY_ROLE_REPO),
                "ansible-tasklists::{}".format(NSBL_COMMUNITY_TASKLIST_REPO),
            ]

        else:
            return []

    def get_supported_resource_types(self):

        return ["roles", "ansible-tasklists"]

    def get_supported_task_types(self):

        return ["ansible-module", "ansible-role", "ansible-tasklist", "ansible-meta"]

    def run(
        self,
        tasklist,
        run_vars,
        run_config,
        run_secrets,
        run_env,
        result_callback,
        parent_task,
    ):

        if parent_task is None:
            raise Exception("No parent task provided")

        minimal_facts_only = run_config["minimal_facts_only"]

        if minimal_facts_only:
            pre_tasks = generate_pre_tasks(
                minimal_facts=True,
                box_basics=False,
                box_basics_non_sudo=False,
                freckles_facts=False,
            )
        else:
            pre_tasks = generate_pre_tasks(
                minimal_facts=True,
                box_basics=True,
                box_basics_non_sudo=False,
                freckles_facts=True,
            )
        additional_files = generate_additional_files_dict()

        final_config = copy.deepcopy(run_config)

        # adding execution path

        nsbl_run_dir = os.path.join(run_env["env_dir"], "nsbl")

        final_config["add_symlink_to_env"] = False
        final_config["add_timestamp_to_env"] = False
        final_config["force"] = False
        final_config["run_folder"] = nsbl_run_dir

        secure_vars = {}

        tasklist_new = []

        for task in tasklist:

            if task[FRECKLET_KEY_NAME]["type"] == "ansible-meta":
                new_task = copy.deepcopy(task)
                vars = new_task.pop(VARS_KEY)
                f_type = task[FRECKLET_KEY_NAME]["name"]
                module_name = vars["name"]
                vars_vars = vars.get("vars", {})

                new_task[FRECKLET_KEY_NAME]["type"] = f_type
                new_task[FRECKLET_KEY_NAME]["name"] = module_name
                new_task[TASK_KEY_NAME]["command"] = module_name
                new_task[VARS_KEY] = vars_vars

                task = new_task

            tasklist_new.append(task)

            secret_task_vars = task[FRECKLET_KEY_NAME]["secret_vars"]

            if not secret_task_vars:
                continue

            task_id = task[FRECKLET_KEY_NAME]["_task_id"]
            force_log = self.config_value("force_show_log")

            for var_name, var_value in task.get(VARS_KEY, {}).items():
                if var_name not in secret_task_vars:
                    continue
                var_alias = "task_{}_pw_{}".format(task_id, var_name)

                if isinstance(var_value, string_types):
                    val = var_value
                    repl = "{{{{ lookup('env', '{}') }}}}".format(var_alias)
                else:
                    val = json.dumps(var_value)
                    repl = "{{{{ lookup('env', '{}') | from_json }}}}".format(var_alias)

                secure_vars[var_alias] = {"type": "environment", "value": val}
                task[VARS_KEY][var_name] = repl
                if not force_log:
                    task["task"]["no_log"] = True

        # run_resources = run_env["resource_path"]
        # urls = {
        #     "ansible-tasklists": os.path.join(run_resources, "ansible-tasklists"),
        #     "roles": os.path.join(run_resources, "roles"),
        # }
        # run_nsbl_context = NsblContext(
        #     urls=urls,
        #     allow_external_roles=self.nsbl_context.allow_external_roles,
        #     allow_external_tasklists=self.nsbl_context.allow_external_tasklists,
        # )
        run_nsbl_context = self.nsbl_context

        nsbl_env = create_single_host_nsbl_env_from_tasklist(
            tasklist_new,
            run_nsbl_context,
            pre_tasks=pre_tasks["pre_tasks"],
            gather_facts=pre_tasks["gather_facts"],
            additional_files=additional_files,
            task_marker="task",
            meta_marker="frecklet",
            **final_config
        )

        # callback_adapter = NsblFrecklesCallbackAdapter(
        #     nsbl_env, parent_task=parent_task, result_callback=result_callback
        # )
        final_config["callback"] = "freckles_callback"
        callback_adapter = NsblPrintCallbackAdapter(root_task=parent_task)
        # callback_adapter = NsblFrecklesCallbackAdapter(nsbl=nsbl_env, parent_task=parent_task, result_callback=result_callback)

        sudo_password = run_secrets.get("become_pass", None)
        ssh_password = run_secrets.get("ssh_pass", None)

        extra_env_vars = {}
        if "pwd" in run_vars["__freckles_run__"].keys():
            extra_env_vars["NSBL_RUN_PWD"] = run_vars["__freckles_run__"]["pwd"]

        nsbl_runner = NsblRunner(nsbl_env)

        result = nsbl_runner.run(
            callback_adapter=callback_adapter,
            sudo_password=sudo_password,
            ssh_password=ssh_password,
            extra_env_vars=extra_env_vars,
            secure_vars=secure_vars,
            extra_paths=reversed(
                self.context.frkl_pkg.lookup_paths(
                    incl_system_path=False, include_frozen=False
                )
            ),
            parent_task=parent_task,
            **final_config
        )

        return result
