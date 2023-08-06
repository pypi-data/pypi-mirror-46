# -*- coding: utf-8 -*-
# Copyright 2018 Markus Binsteiner <makkus@frkl.io>
# Copyright 2013 Dag Wieers <dag@wieers.com>
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

from ansible.module_utils.parsing.convert_bool import boolean
from ansible.module_utils.six import iteritems, string_types
from ansible.plugins.action import ActionBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display

    display = Display()
#
# CONDA_ALLOWED_KEYS = ["conda_environment", "upgrade", "conda_channels", "state", "name"]
# NIX_ALLOWED_KEYS = ["name", "state"]
# NPM_ALLOWED_KEYS = [
#     "executable",
#     "global",
#     "ignore_scripts",
#     "name",
#     "path",
#     "production",
#     "registry",
#     "state",
#     "version",
# ]
# VAGRANT_ALLOWED_KEYS = ["name", "update", "plugin_source", "version"]
# PIP_ALLOWED_KEYS = [
#     "chdir",
#     "editable",
#     "executable",
#     "extra_args",
#     "name",
#     "requirements",
#     "state",
#     "umask",
#     "version",
#     "virtualenv",
#     "virtualenv_command",
#     "virtualenv_python",
#     "virtualenv_site_packages",
# ]
# UNARCHIVE_ALLOWED_KEYS = [
#     "attr",
#     "attributes",
#     "copy",
#     "creates",
#     "decryt",
#     "dest",
#     "exclude",
#     "extra_opts",
#     "group",
#     "keep_newer",
#     "list_files",
#     "mode",
#     "owner",
#     "remote_src",
#     "selevel",
#     "serole",
#     "setype",
#     "seuser",
#     "src",
#     "unsafe_writes",
#     "validate_certs",
# ]
# GET_URL_ALLOWED_KEYS = [
#     "attributes",
#     "backup",
#     "checksum",
#     "client_cert",
#     "client_key",
#     "dest",
#     "force",
#     "force_basic_auth",
#     "group",
#     "headers",
#     "mode",
#     "others",
#     "owner",
#     "selevel",
#     "serole",
#     "setype",
#     "seuser",
#     "sha256sum",
#     "timeout",
#     "thirsty",
#     "tmp_dest",
#     "unsafe_writes",
#     "url",
#     "url_password",
#     "url_username",
#     "use_proxy",
#     "validate_certs",
# ]
# GIT_ALLOWED_KEYS = [
#     "accept_hostkey",
#     "archive",
#     "bare",
#     "clone",
#     "depth",
#     "dest",
#     "executable",
#     "force",
#     "key_file",
#     "name",
#     "recursive",
#     "reference",
#     "refspec",
#     "repo",
#     "ssh_opts",
#     "track_submodules",
#     "umask",
#     "update",
#     "verify_commit",
#     "version",
# ]
# YUM_ALLOWED_KEYS = [
#     "allow_downgrade",
#     "bugfix",
#     "conf_file",
#     "disable_gpg_check",
#     "disable_plugin",
#     "disablerepo",
#     "enable_plugin",
#     "enablerepo",
#     "exclude",
#     "expire-cache",
#     "installroot",
#     "list",
#     "name",
#     "pkg",
#     "security",
#     "skip_broken",
#     "state",
#     "update_cache",
#     "update_only",
#     "validate_certs",
# ]
# APT_ALLOWED_KEYS = [
#     "name",
#     "state",
#     "allow_unauthenticated",
#     "autoclean",
#     "autoremove",
#     "cache_valid_time",
#     "deb",
#     "default_release",
#     "dpkg_options",
#     "force",
#     "force_apt_get",
#     "install_recommends",
#     "only_upgrades",
#     "package",
#     "pkg",
#     "purge",
#     "state",
#     "update_cache",
#     "upgrade",
# ]
# APT_RESULT_KEYS = ["cache_updated", "cache_update_time", "stdout", "stderr"]
#
# PKG_MGR_DEFAULTS = {
#     "apt": {
#         "keys": APT_ALLOWED_KEYS,
#         "return_keys": APT_RESULT_KEYS,
#         "needs_become": True,
#         "needs_facts": True,
#     },
#     "conda": {"keys": CONDA_ALLOWED_KEYS, "become": False, "needs_facts": True},
#     "get_url": {"keys": GET_URL_ALLOWED_KEYS, "become": False, "needs_facts": False},
#     "git": {"keys": GIT_ALLOWED_KEYS, "become": False, "needs_facts": True},
#     "nix": {"keys": NIX_ALLOWED_KEYS, "become": False, "needs_facts": True},
#     "npm": {"keys": NPM_ALLOWED_KEYS, "become": False, "needs_facts": True},
#     "pip": {"keys": PIP_ALLOWED_KEYS, "become": False, "needs_facts": True},
#     "unarchive": {
#         "keys": UNARCHIVE_ALLOWED_KEYS,
#         "become": False,
#         "needs_facts": False,
#     },
#     "vagrant_plugin": {
#         "keys": VAGRANT_ALLOWED_KEYS,
#         "become": False,
#         "needs_facts": True,
#     },
#     "yum": {"keys": YUM_ALLOWED_KEYS, "become": True, "needs_facts": False},
# }


def create_platform_strings(setup_facts, ignore_case):

    platform = setup_facts["ansible_facts"].get("ansible_system", None)
    os_family = setup_facts["ansible_facts"].get("ansible_os_family", None)
    distribution = setup_facts["ansible_facts"].get("ansible_distribution", None)
    distribution_major_version = setup_facts["ansible_facts"].get(
        "ansible_distribution_major_version", None
    )
    distribution_version = setup_facts["ansible_facts"].get(
        "ansible_distribution_version", None
    )
    distribution_release = setup_facts["ansible_facts"].get(
        "ansible_distribution_release", None
    )

    if distribution_version:
        full_version_string = "{0}-{1}".format(distribution, distribution_version)
        if ignore_case:
            full_version_string = full_version_string.lower()
    else:
        full_version_string = None

    if distribution_release:
        full_release_string = "{0}-{1}".format(distribution, distribution_release)
        if ignore_case:
            full_release_string = full_release_string.lower()
    else:
        full_release_string = None

    if distribution_major_version:
        distribution_major_string = "{0}-{1}".format(
            distribution, distribution_major_version
        )
        if ignore_case:
            distribution_major_string = distribution_major_string.lower()
    else:
        distribution_major_string = None

    if ignore_case:
        distribution = distribution.lower()
        os_family = os_family.lower()
        platform = platform.lower()

    string_matchers = [
        full_version_string,
        full_release_string,
        distribution_major_string,
        distribution,
        os_family,
        platform,
    ]

    return string_matchers


def find_first_match(v, string_matchers, ignore_case=True):

    result_value = None
    result_matcher = None
    for platform_string, value in iteritems(v):

        for matcher in string_matchers:

            if ignore_case:
                platform_string = platform_string.lower()

            if matcher in platform_string:
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


DEFAULT_HOST_FACTS = []


class ActionModule(ActionBase):

    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        cacheable = boolean(self._task.args.pop("cacheable", False))
        ignore_case = boolean(self._task.args.pop("ignore_case", False))
        ansible_fact_keys = self._task.args.pop("ansible_fact_keys", DEFAULT_HOST_FACTS)

        if "ansible_distribution_major_version" not in task_vars.keys():
            setup_facts = self._execute_module(
                module_name="setup",
                module_args=dict(gather_subset="!all"),
                task_vars=task_vars,
            )
        else:
            setup_facts = {"ansible_facts": task_vars}

        string_matchers = create_platform_strings(setup_facts, ignore_case=ignore_case)
        facts_run = self._execute_module(
            module_name="freckles_facts",
            module_args=dict({"executables": []}),
            task_vars=task_vars,
        )

        if facts_run.get("failed", False) == True:
            return facts_run

        result.update(facts_run)

        freckles_facts = result.setdefault("ansible_facts", {})["__freckles_facts__"]
        freckles_facts["platform_matchers"] = string_matchers
        pkg_mgr = task_vars.get("ansible_pkg_mgr", None)
        if pkg_mgr is None or pkg_mgr == "unknown":
            if "Darwin" in string_matchers:
                pkg_mgr = "homebrew"
        freckles_facts["host_pkg_mgr"] = pkg_mgr
        freckles_facts["host_service_mgr"] = task_vars.get("ansible_host_mgr", None)
        host_facts = {}
        for key in ansible_fact_keys:
            value = task_vars.get(key, None)
            host_facts[key] = value
        freckles_facts["ansible_host_facts"] = host_facts

        return result
