# -*- coding: utf-8 -*-
# Copyright 2018 Markus Binsteiner <makkus@frkl.io>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy
import os
from collections import OrderedDict, Mapping
from ansible.module_utils.six import iteritems, string_types
from ansible.plugins.action import ActionBase
from ansible.module_utils.parsing.convert_bool import boolean

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display

    display = Display()


def dict_merge(dct, merge_dct, copy_dct=True):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.

    Copied from: https://gist.github.com/angstwad/bf22d1822c38a92ec0a9

    Args:
      dct (dict): dict onto which the merge is executed
      merge_dct (dict): dct merged into dct
      copy_dct (bool): whether to (deep-)copy dct before merging (and leaving it unchanged), or not (default: copy)

    Returns:
      dict: the merged dict (original or copied)
    """

    if copy_dct:
        dct = copy.deepcopy(dct)

    for k, v in merge_dct.items():
        if k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], Mapping):
            dict_merge(dct[k], merge_dct[k], copy_dct=False)
        else:
            dct[k] = merge_dct[k]

    return dct


def find_first_match(v, string_matchers, ignore_case=True):

    result_value = None
    result_matcher = None
    for platform_string, value in iteritems(v):

        for matcher in string_matchers:

            if ignore_case:
                platform_string = platform_string.lower()

            if platform_string in matcher:
                result_value = value
                result_matcher = matcher
                break

        if result_value is not None:
            break

    if result_value is None:
        for value_key, value_value in iteritems(v):
            if ignore_case:
                value_key = value_key.lower()
            if "default" == value_key:
                result_value = value_value
                result_matcher = "default"

    if isinstance(result_value, string_types) and result_value.lower() in (
        "true",
        "false",
        "yes",
        "no",
    ):
        result_value = boolean(v)

    return (result_value, result_matcher)


# install downstream modules
# ==========================


def filter_module_keys(pkg_dict, allowed_keys):

    if "*" in allowed_keys:
        return pkg_dict

    result = {}
    for k, v in iteritems(pkg_dict):

        if k in allowed_keys:
            result[k] = v

    return result


def generate_default_install_conf(pkg):

    return pkg


# ansible_role
# -------------

ANSIBLE_ROLE_ALLOWED_KEYS = ["*"]
ANSIBLE_ROLE_NAME_ALIASES = ["role", "name"]


def ansible_role_config_generate(pkg, become, pkg_mgr_facts):

    name = pkg.get("role", None)
    if name is None:
        name = pkg.get("name", None)
        pkg["role"] = name
    else:
        if not pkg.get("name", False):
            pkg["name"] = name

    if not name:
        raise Exception(
            "No role name specified, needs either 'role' or 'name' key: {}".format(pkg)
        )

    temp = copy.deepcopy(pkg)
    temp.pop("name", None)
    temp.pop("pkg_mgr", None)
    temp.pop("role", None)

    if "become" not in pkg.keys():
        pkg["become"] = False
    # if "become_user" not in pkg.keys():
    #     pkg["become_user"] = None

    pkg["vars"] = temp

    return pkg


# apt
# ---
APT_ALLOWED_KEYS = [
    "name",
    "state",
    "allow_unauthenticated",
    "autoclean",
    "autoremove",
    "cache_valid_time",
    "deb",
    "default_release",
    "dpkg_options",
    "force",
    "force_apt_get",
    "install_recommends",
    "only_upgrades",
    "package",
    "pkg",
    "purge",
    "state",
    "update_cache",
    "upgrade",
]

APT_RESULT_KEYS = ["cache_updated", "cache_update_time", "stdout", "stderr"]
APT_NAME_ALIAS_KEYS = ["name", "package", "pkg", "deb"]


def apt_config_generate(pkg, become, pkg_mgr_facts):

    name = pkg.pop("name", None)
    if name is None:
        name = pkg.pop("package", None)
        if name is None:
            name = pkg.pop("pkg", None)

    if name is not None and "deb" in pkg.keys():
        raise Exception(
            "Apt module doesn't allow specifying keys 'name' and 'deb' at the same time: {}".format(
                pkg
            )
        )

    if name is None and "deb" not in pkg.keys():
        raise Exception("Apt module needs one of 'name' or 'deb' keys: {}".format(pkg))

    if name is not None:

        if name.endswith(".deb"):
            pkg["deb"] = name
        else:
            pkg["name"] = name

    return pkg


def apt_can_handle(pkg):

    if "deb" in pkg.keys():
        return True

    name = None
    if "name" in pkg.keys():
        name = pkg["name"]

    if name is None and "package" in pkg.keys():
        name = pkg["package"]

    if name is None and "pkg" in pkg.keys():
        name = pkg["pkg"]

    if name is not None and name.endswith(".deb"):
        return True

    return False


YUM_ALLOWED_KEYS = [
    "allow_downgrade",
    "bugfix",
    "conf_file",
    "disable_gpg_check",
    "disable_plugin",
    "disablerepo",
    "enable_plugin",
    "enablerepo",
    "exclude",
    "expire-cache",
    "installroot",
    "list",
    "name",
    "pkg",
    "security",
    "skip_broken",
    "state",
    "update_cache",
    "update_only",
    "validate_certs",
]
YUM_NAME_ALIAS_KEYS = ["pkg", "name"]


def yum_can_handle(pkg):

    name = pkg.get("name", None)
    if name is None:
        name = pkg.get("pkg", None)

    if name is not None:

        if name.endswith(".rpm"):

            return True

    return False


GIT_ALLOWED_KEYS = [
    "accept_hostkey",
    "archive",
    "bare",
    "clone",
    "depth",
    "dest",
    "executable",
    "force",
    "key_file",
    "name",
    "recursive",
    "reference",
    "refspec",
    "repo",
    "ssh_opts",
    "track_submodules",
    "umask",
    "update",
    "verify_commit",
    "version",
]


GIT_NAME_ALIAS_KEYS = ["repo"]


def git_can_handle(pkg):

    name = pkg.get("name", None)
    if name is None:
        name = pkg.get("repo", None)

    if name is None:
        return False

    if name.endswith(".git"):
        return True
    if name.startswith("git@"):
        return True

    return False


def git_config_generate(pkg, become, pkg_mgr_facts):

    name = pkg.pop("name", None)
    repo = pkg.pop("repo", None)

    if repo is not None:
        n = repo
    elif name is not None:
        n = name
    else:
        raise Exception(
            "Neither 'name' nor 'repo' specified for git module: {}".format(pkg)
        )

    if "dest" not in pkg.keys():
        raise Exception("No 'dest' key specified for git module: {}".format(pkg))

    pkg["repo"] = n

    return pkg


GET_URL_ALLOWED_KEYS = [
    "attributes",
    "backup",
    "checksum",
    "client_cert",
    "client_key",
    "dest",
    "force",
    "force_basic_auth",
    "group",
    "headers",
    "mode",
    "others",
    "owner",
    "selevel",
    "serole",
    "setype",
    "seuser",
    "sha256sum",
    "timeout",
    "thirsty",
    "tmp_dest",
    "unsafe_writes",
    "url",
    "url_password",
    "url_username",
    "use_proxy",
    "validate_certs",
]
GET_URL_NAME_ALIAS_KEYS = ["url"]


def get_url_config_generate(pkg, become, pkg_mgr_facts):

    name = pkg.pop("name", None)
    url = pkg.pop("url", None)
    if url is None and name is None:
        raise Exception("No 'url' specified for get_url module: {}".format(url))
    elif url is not None and name is not None and url != name:
        raise Exception(
            "Both 'name' and 'url' specified, with different values: {}".format(pkg)
        )

    if url:
        u = url
    else:
        u = name

    if (
        not u.startswith("http://")
        and not u.startswith("https://")
        and not u.startswith("ftp://")
    ):
        raise Exception(
            "Invalid url for get_url module (only supports 'http/https/ftp': {})".format(
                u
            )
        )
    pkg["url"] = u

    dest = pkg.get("dest", None)
    if dest is None:
        dest = "~/.local/bin"
        pkg["dest"] = dest
    mode = pkg.get("mode", None)
    if mode is None:
        mode = "0775"
        pkg["mode"] = mode

    dest_dir = os.path.dirname(dest)
    task_msg = "creating folder: {}".format(dest_dir)
    module_args = {"path": dest_dir, "recurse": True, "state": "directory"}

    pre_tasks = OrderedDict()
    pre_tasks[task_msg] = {"module_name": "file", "module_args": module_args}

    return (pkg, pre_tasks)


HOMEBREW_ALLOWED_KEYS = [
    "forumla",
    "install_options",
    "name",
    "options",
    "path",
    "package",
    "pkg",
    "state",
    "update_brew",
    "update_homebrew",
    "upgrade",
    "upgrade_all",
]
HOMEBREW_NAME_ALIAS_KEYS = ["formula", "name", "package", "pkg"]


def homebrew_config_generate(pkg, become, pkg_mgr_facts):

    name = pkg.pop("name", None)
    if name is None:
        name = pkg.pop("pkg", None)
        if name is None:
            name = pkg.pop("package", None)
            if name is None:
                name = pkg.pop("formula", None)

    if name is None:
        raise Exception("No package specified to install with homebrew: {}".format(pkg))
    pkg["name"] = name
    return pkg


UNARCHIVE_ALLOWED_KEYS = [
    "attr",
    "attributes",
    "copy",
    "creates",
    "decryt",
    "dest",
    "exclude",
    "extra_opts",
    "group",
    "keep_newer",
    "list_files",
    "mode",
    "owner",
    "remote_src",
    "selevel",
    "serole",
    "setype",
    "seuser",
    "src",
    "unsafe_writes",
    "validate_certs",
]
UNARCHIVE_NAME_ALIAS_KEYS = ["src"]


def unarchive_config_generate(pkg, become, pkg_mgr_facts):

    name = pkg.pop("name", None)
    src = pkg.pop("src", None)
    if src is None and name is None:
        raise Exception("No 'src' specified for unarchive module: {}".format(url))
    elif src is not None and name is not None and src != name:
        raise Exception(
            "Both 'name' and 'src' specified, with different values: {}".format(pkg)
        )

    if src:
        s = src
    else:
        s = name

    pkg["src"] = s
    if (
        s.startswith("http://")
        or s.startswith("https://")
        or s.startswith("ftp://")
        and "remote_src" not in pkg.keys()
    ):
        pkg["remote_src"] = True

    dest = pkg.get("dest", None)
    if dest is None:
        raise Exception("No 'dest' key specified for unarchive module: {}".format(pkg))

    task_msg = "creating folder: {}".format(dest)
    module_args = {"path": dest, "recurse": True, "state": "directory"}

    pre_tasks = OrderedDict()
    pre_tasks[task_msg] = {"module_name": "file", "module_args": module_args}

    return (pkg, pre_tasks)


def unarchive_can_handle(pkg):

    src = pkg.get("src", None)
    if src is None:
        src = pkg.get("name", None)
        if src is None:
            return False

    extensions = [".zip", ".tar", ".tar.gz", ".tar.bz2," ".tar.xz"]
    for ext in extensions:
        if src.endswith(ext):
            return True

    return False


PIP_ALLOWED_KEYS = [
    "chdir",
    "editable",
    "executable",
    "extra_args",
    "name",
    "requirements",
    "state",
    "umask",
    "version",
    "virtualenv",
    "virtualenv_command",
    "virtualenv_python",
    "virtualenv_site_packages",
]
PIP_NAME_ALIAS_KEYS = ["requirements"]


def pip_config_generate(pkg, become, freckles_facts):

    name = pkg.pop("name", None)
    requirements = pkg.pop("requirements", None)

    if name is None and requirements is None:
        raise Exception(
            "Neither 'name' nor 'requirements' key specified for pip module: {}".format(
                pkg
            )
        )

    if name is not None and requirements is not None and name != requirements:
        raise Exception(
            "Both 'name' and 'requirements' keys specified in pip module: {}".format(
                pkg
            )
        )

    if name:
        if name.endswith(".txt"):
            pkg["requirements"] = name
        else:
            pkg["name"] = name
    else:
        pkg["requirements"] = requirements

    # pf = freckles_facts["pkg_mgrs"].get("pip", {})
    #
    # exes = pf.get("executables", {}).get("pip", [])
    #
    # if not exes:
    #     raise Exception("pip not available")

    # if not "virtualenv" in pkg.keys():
    #
    #     if not "/usr/bin/pip" in exes and "executable" not in pkg.keys():
    #         pkg["executable"] = exes[0]

    return pkg


def pip_can_handle(pkg):

    name = pkg.get("name", None)
    if name is None:
        name = pkg.get("requirements", None)
        if name is None:
            return False

    if os.path.basename(name).startswith("requirements") and name.endswith(".txt"):
        return True

    return False


CONDA_ALLOWED_KEYS = ["conda_environment", "upgrade", "conda_channels", "state", "name"]
CONDA_NAME_ALIAS_KEYS = []
NIX_ALLOWED_KEYS = ["name", "state"]
NIX_NAME_ALIAS_KEYS = []
NPM_ALLOWED_KEYS = [
    "executable",
    "global",
    "ignore_scripts",
    "name",
    "path",
    "production",
    "registry",
    "state",
    "version",
]
NPM_NAME_ALIAS_KEYS = ["path"]

VAGRANT_ALLOWED_KEYS = ["name", "update", "plugin_source", "version"]
VAGRANT_NAME_ALIAS_KEYS = []

PKG_MGR_DEFAULTS = {
    "ansible_role": {
        "keys": ANSIBLE_ROLE_ALLOWED_KEYS,
        "become": False,
        "config_generate": ansible_role_config_generate,
        "needs_facts": False,
        "name_aliases": ANSIBLE_ROLE_NAME_ALIASES,
    },
    "apt": {
        "keys": APT_ALLOWED_KEYS,
        "return_keys": APT_RESULT_KEYS,
        "become": True,
        "config_generate": apt_config_generate,
        "can_handle_package": apt_can_handle,
        "needs_facts": True,
        "name_aliases": APT_NAME_ALIAS_KEYS,
    },
    "conda": {
        "keys": CONDA_ALLOWED_KEYS,
        "become": False,
        "needs_facts": True,
        "name_aliases": CONDA_NAME_ALIAS_KEYS,
    },
    "get_url": {
        "keys": GET_URL_ALLOWED_KEYS,
        "config_generate": get_url_config_generate,
        "become": False,
        "needs_facts": False,
        "name_aliases": GET_URL_NAME_ALIAS_KEYS,
    },
    "git": {
        "keys": GIT_ALLOWED_KEYS,
        "can_handle_package": git_can_handle,
        "become": False,
        "config_generate": git_config_generate,
        "needs_facts": True,
        "name_aliases": GIT_NAME_ALIAS_KEYS,
    },
    "homebrew": {
        "keys": HOMEBREW_ALLOWED_KEYS,
        "become": False,
        "config_generate": homebrew_config_generate,
        "needs_facts": True,
        "name_aliases": HOMEBREW_NAME_ALIAS_KEYS,
    },
    "nix": {
        "keys": NIX_ALLOWED_KEYS,
        "become": False,
        "needs_facts": True,
        "name_aliases": NIX_NAME_ALIAS_KEYS,
    },
    "npm": {
        "keys": NPM_ALLOWED_KEYS,
        "become": False,
        "needs_facts": True,
        "name_aliases": NPM_NAME_ALIAS_KEYS,
    },
    "pip": {
        "keys": PIP_ALLOWED_KEYS,
        "become": False,
        "can_handle_package": pip_can_handle,
        "config_generate": pip_config_generate,
        "needs_facts": True,
        "name_aliases": PIP_NAME_ALIAS_KEYS,
    },
    "unarchive": {
        "keys": UNARCHIVE_ALLOWED_KEYS,
        "config_generate": unarchive_config_generate,
        "become": False,
        "can_handle_package": unarchive_can_handle,
        "needs_facts": False,
        "name_aliases": UNARCHIVE_NAME_ALIAS_KEYS,
    },
    "vagrant_plugin": {
        "keys": VAGRANT_ALLOWED_KEYS,
        "become": False,
        "needs_facts": True,
        "name_aliases": VAGRANT_NAME_ALIAS_KEYS,
    },
    "yum": {
        "keys": YUM_ALLOWED_KEYS,
        "become": True,
        "can_handle_package": yum_can_handle,
        "needs_facts": False,
        "name_aliases": YUM_NAME_ALIAS_KEYS,
    },
}


class ActionModule(ActionBase):

    TRANSFERS_FILES = False

    def parse_package(
        self,
        package_item,
        default_pkg_mgr,
        default_become,
        default_become_user,
        freckles_facts,
        ignore_case,
        filter_keys,
    ):

        if isinstance(package_item, string_types):
            package_item = {"name": package_item}

        no_install = package_item.pop("no_install", None)
        if no_install:
            return ([], [])
        pkg_name = package_item.pop("name", None)

        pkg_become = package_item.pop("become", None)
        pkg_become_user = package_item.pop("become_user", None)
        pkg_pkg_mgr = package_item.pop("pkg_mgr", None)
        platforms = package_item.pop("pkgs", None)
        other_args = package_item

        if isinstance(platforms, (list, tuple)):
            platforms = {"default": platforms}

        if platforms is not None and not isinstance(platforms, dict):
            raise Exception("'platforms' variable needs to be of type dict")

        string_matchers = freckles_facts["platform_matchers"]

        if ignore_case:
            temp = []
            for sm in string_matchers:
                temp.append(sm.lower())
            string_matchers = temp

        if pkg_pkg_mgr == None:
            pkg_pkg_mgr = "auto"

        if platforms is None:

            if pkg_pkg_mgr != "auto":
                for n in PKG_MGR_DEFAULTS.get(pkg_pkg_mgr)["name_aliases"]:
                    if n in package_item.keys():
                        pkg_name = package_item[n]
                        break

            p = {"name": pkg_name, "pkg_mgr": pkg_pkg_mgr, "become": pkg_become}
            if pkg_become_user is not None:
                p["become_user"] = pkg_become_user

            # npm can have
            # if pkg_name is None and pkg_pkg_mgr != "npm":
            #     raise Exception("No 'name' key provided in package description (pkg_mgr: {}): {}".format(pkg_pkg_mgr, package_item))
            # else:
            #     if pkg_name is not None:
            #         p["name"] = pkg_name

            pkgs = [p]
        else:
            (pkg_details, result_matcher) = find_first_match(
                platforms, string_matchers, ignore_case=ignore_case
            )

            if pkg_details in ["no-install", "ignore", "omit"]:
                return ([], [])

                if pkg_details is None:
                    p = {"name": pkg_name, "pkg_mgr": pkg_pkg_mgr, "become": pkg_become}
                    if pkg_become_user is not None:
                        p["become_user"] = pkg_become_user
                    pkg_details = [p]

            else:
                if not isinstance(pkg_details, (list, tuple)):
                    if isinstance(pkg_details, string_types):
                        p = {
                            "name": pkg_details,
                            "pkg_mgr": pkg_pkg_mgr,
                            "become": pkg_become,
                        }
                        if pkg_become_user is not None:
                            p["become_user"] = pkg_become_user
                        pkg_details = [p]

                    elif isinstance(pkg_details, dict):
                        pkg_details = [pkg_details]
                        for p in pkg_details:
                            if "pkg_mgr" not in p.keys():
                                p["pkg_mgr"] = pkg_pkg_mgr
                            if "become" not in p.keys():
                                p["become"] = pkg_become
                            if (
                                "become_user" not in p.keys()
                                and pkg_become_user is not None
                            ):
                                p["become_user"] = pkg_become_user

            pkgs = []
            for item in pkg_details:
                if isinstance(item, string_types):
                    p = {"name": item, "pkg_mgr": pkg_pkg_mgr, "become": pkg_become}
                    if pkg_become_user is not None:
                        p["become_user"] = pkg_become_user
                    pkgs.append(p)
                elif isinstance(item, dict):
                    pkgs.append(item)
                else:
                    raise Exception(
                        "Invalid type '{}' for platform package description (needs to be 'string' or 'dict'): {}".format(
                            type(item), item
                        )
                    )

        pre_tasks = []
        result = []
        for pkg in pkgs:

            this_pkg_mgr = pkg.pop("pkg_mgr", None)
            if this_pkg_mgr is None or this_pkg_mgr == "auto":

                this_pkg_mgr = None
                for pm, cnf in iteritems(PKG_MGR_DEFAULTS):
                    if "can_handle_package" in cnf.keys():
                        can_handle = PKG_MGR_DEFAULTS[pm]["can_handle_package"](pkg)
                        if can_handle:
                            this_pkg_mgr = pm
                            break
                if this_pkg_mgr is None:
                    this_pkg_mgr = default_pkg_mgr

            pkg_become = pkg.pop("become", None)
            this_become_user = pkg.pop("become_user", None)
            if pkg_become is not None:
                this_become = pkg_become
            else:
                if this_pkg_mgr in PKG_MGR_DEFAULTS.keys():
                    this_become = PKG_MGR_DEFAULTS[this_pkg_mgr].get(
                        "become", default_become
                    )
                else:
                    this_become = default_become

            pkg = dict_merge(other_args, pkg, copy_dct=True)

            if this_pkg_mgr not in PKG_MGR_DEFAULTS.keys():
                config = generate_default_install_conf(pkg)
            elif "config_generate" in PKG_MGR_DEFAULTS[this_pkg_mgr].keys():
                config = PKG_MGR_DEFAULTS[this_pkg_mgr]["config_generate"](
                    pkg, this_become, freckles_facts
                )
            else:
                config = generate_default_install_conf(pkg)

            if this_pkg_mgr is None:
                this_pkg_mgr = "auto"

            if isinstance(config, tuple):
                if not isinstance(config[1], (list, tuple)):
                    pt = [config[1]]
                else:
                    pt = config[1]

                pre_tasks = pre_tasks + pt
                config = config[0]

            config["become"] = this_become
            if this_become_user is not None:
                config["become_user"] = this_become_user
            config["pkg_mgr"] = this_pkg_mgr
            result.append(config)

        return (result, pre_tasks)

    def run(self, tmp=None, task_vars=None):

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        skip_non_matches = boolean(self._task.args.pop("skip_non_matches", False))
        ignore_case = boolean(self._task.args.pop("ignore_case", True))
        filter_keys = boolean(self._task.args.pop("filter_keys", True))
        package_list_var = self._task.args.pop("package_list_var", None)
        no_run = self._task.args.pop("no_run", False)

        packages = self._task.args.pop("packages", None)

        package_names = []

        if packages is None:
            result["failed"] = True
            result["msg"] = "No 'packages' key provided."
            return result

        if "__freckles_facts__" not in task_vars.keys():
            result["failed"] = True
            result["msg"] = "No freckles facts available, can't continue"
            return result

        freckles_facts = task_vars["__freckles_facts__"]
        module_pkg_mgr = freckles_facts["host_pkg_mgr"]
        default_become = self._play_context.become

        pkgs = []
        tasks = []
        for package_item in packages:
            try:
                item_pkgs, item_pre_tasks = self.parse_package(
                    package_item,
                    default_pkg_mgr=module_pkg_mgr,
                    default_become=default_become,
                    default_become_user=None,
                    freckles_facts=freckles_facts,
                    ignore_case=ignore_case,
                    filter_keys=filter_keys,
                )
                if not item_pkgs:
                    continue

                pkgs.extend(item_pkgs)
                tasks.append((item_pre_tasks, item_pkgs))
                for pkg in item_pkgs:
                    name = pkg.get("name", None)
                    if name is None:
                        name = pkg.get("requirements", None)
                    if name is None:
                        name = pkg.get("repo", None)
                    if name is None:
                        name = pkg.get("url", None)
                    if name is None:
                        name = pkg.get("src", None)
                    if name is None:
                        name = pkg.get("path", None)
                    if name is None:
                        name = "n/a"
                    package_names.append(name)
            except (Exception) as e:
                result["failed"] = True
                result["msg"] = str(e)
                return result

        if no_run:
            result["changed"] = False
            result["failed"] = False
            if package_list_var is not None:
                result["ansible_facts"] = {package_list_var: pkgs}
            return result

        all_run_results = []
        pkg_run_results = []
        failed_pkgs = []
        failed = False
        changed = False
        skipped = True

        pkgs_copy = copy.deepcopy(pkgs)

        for task in tasks:

            # display.vvvv(str(task))

            pre_tasks = task[0]
            pkgs = task[1]

            # TODO: pre_tasks
            # if pre_tasks is not None:
            #     for msg, run_details in iteritems(pre_tasks):
            #         module_name = run_details["module_name"]
            #         module_become = run_details.get("module_become", False)
            #         module_vars = run_details.get("module_vars", {})
            #         module_args = run_details.get("module_args", {})
            #         temp_become = self._play_context.become
            #         self._play_context.become = module_become
            #         run = self._execute_module(module_name=module_name, module_args=module_args, task_vars=module_vars, wrap_async=self._task.async)
            #         self._play_context.become = temp_become
            #         if run["failed"]:
            #             return run
            if not pkgs:
                result["failed"] = False
                result["changed"] = False
                result["skipped"] = True
                return result

            for pkg in pkgs:

                this_pkg_mgr = pkg.pop("pkg_mgr")

                if this_pkg_mgr == "ansible_role":
                    result["failed"] = True
                    result[
                        "msg"
                    ] = "Can't use the 'ansible_role' as package manager in this module, use the 'freckfrackery.install-pkgs' role instead."
                    return result

                this_become = pkg.pop("become")
                this_become_user = pkg.pop("become_user", None)
                if filter_keys and this_pkg_mgr in PKG_MGR_DEFAULTS.keys():
                    pkg = filter_module_keys(
                        pkg, PKG_MGR_DEFAULTS[this_pkg_mgr].get("keys", [])
                    )

                temp_become = self._play_context.become
                temp_become_user = self._play_context.become_user

                self._play_context.become = this_become
                if this_become_user is not None:
                    self._play_context.become_user = this_become_user

                r = self._execute_module(
                    module_name=this_pkg_mgr,
                    module_args=pkg,
                    task_vars=task_vars,
                    wrap_async=self._task.async_val,
                )

                self._play_context.become = temp_become
                self._play_context.become_user = temp_become_user
                if not r.get("skipped", True):
                    skipped = False
                if r.get("changed", False):
                    changed = True
                if r.get("failed", False):
                    failed = True
                    msg = r["msg"]
                    if msg.strip() == "MODULE FAILURE":
                        msg = ""
                    if "stdout" in msg and "stderr" in msg:
                        stdout = ["stdout:"]
                        stderr = ["stderr:"]
                        match = stdout
                        for line in msg.split("\n"):
                            # this is a bit silly
                            if not line.strip():
                                continue
                            if "stdout" in line:
                                match = stdout
                                se, so = line.split("stdout", 2)
                                if se.strip(":"):
                                    stderr.append(se)
                                so = so.strip(":").strip()
                                match.append(so)
                            elif "stderr" in line:
                                match = stderr
                                so, se = line.split("stderr", 2)
                                if so.strip(":"):
                                    stdout.append(so)
                                se = se.strip(":").strip()
                                match.append(se)
                            else:
                                match.append(line)
                        msg = "\n".join(stdout + stderr)
                    module_stdout = r.get("module_stdout", None)
                    if module_stdout:
                        msg += "\n{}".format(module_stdout)
                    module_stderr = r.get("module_stderr", None)
                    if module_stderr:
                        msg += "\n{}".format(module_stderr)
                    failed_pkgs.append(msg.strip())

                all_run_results.append(r)
                pkg_run_results.append(r)

        result["failed"] = failed
        result["changed"] = changed
        # result["skipped"] = skipped
        msg = None
        if failed:
            msg = ""
            for m in failed_pkgs:
                msg += "{}\n".format(m)
        else:
            pkg_list = "\n".join([" - {}".format(n) for n in package_names])
            msg = "Successfully installed packages:\n{}".format(pkg_list)
        result["msg"] = msg
        if package_list_var is not None:
            result["ansible_facts"] = {package_list_var: pkgs}
        result["results"] = all_run_results
        return result
