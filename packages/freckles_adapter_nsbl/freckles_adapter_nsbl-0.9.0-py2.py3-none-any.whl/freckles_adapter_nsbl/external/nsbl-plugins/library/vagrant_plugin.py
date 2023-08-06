#!/usr/bin/python -tt
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


DOCUMENTATION = """
---
module: vagrant-plugin
short_description: Manage vagrant plugins
"""

EXAMPLES = """
# Install package foo
- vagrant-plugin: name=foo state=present
"""

from ansible.module_utils.basic import *


def update_plugins(module):
    cmd = "vagrant plugin update"
    rc, stdout, stderr = module.run_command(cmd, check_rc=False)
    if rc != 0:
        module.fail_json(msg="failed to update vagrant plugins: {}".format(stderr))

    module.exit_json(changed=True, msg="Upgraded vagrant packages.")


def list_plugins(module):

    cmd = ["vagrant", "plugin", "list"]
    rc, stdout, stderr = module.run_command(cmd)

    if rc != 0:
        return False
    else:
        return stdout


def plugin_installed(module, name, plugins_list):

    if name == "vagrant":
        return True

    return name in plugins_list


def check_for_missing_plugins(module, plugins, installed_plugins):
    if module.check_mode:
        for i, plugin in enumerate(plugins):
            if plugin_installed(module, plugin, installed_plugins):
                continue
            else:
                module.exit_json(changed=True, name=plugin)

        module.exit_json(changed=False, name=plugins)


def install_plugin(
    module, plugin, installed_plugins, plugin_version=None, plugin_source=None
):

    if (
        plugin_installed(module, plugin, installed_plugins)
        and not plugin_version
        and not plugin_source
    ):
        module.exit_json(changed=False, msg="package(s) already installed")

    options_string = ""
    if plugin_version:
        options_string = "--plugin-version {}".format(plugin_version)
    if plugin_source:
        options_string = "{} --plugin-source {}".format(plugin_source)

    cmd = "vagrant plugin install {} {}".format(options_string, plugin)
    rc, stdout, stderr = module.run_command(cmd, check_rc=False)

    if rc != 0:
        module.fail_json(msg="failed to install {}: {}".format(plugin, stderr))
    else:
        module.exit_json(
            changed=True, msg="installed vagrant plugin: '{}'".format(plugin)
        )


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(aliases=["plugin"]),
            update=dict(default=False, type="bool"),
            version=dict(default=None),
            plugin_source=dict(default=None),
            state=dict(
                default="present", choices=["present", "installed", "absent", "removed"]
            ),
        ),
        required_one_of=[["name", "update"]],
        mutually_exclusive=[
            ["name", "update"],
            ["update", "version"],
            ["update", "plugin_source"],
        ],
        supports_check_mode=False,
    )

    p = module.params

    # normalize the state parameter
    if p["state"] in ["present", "installed"]:
        p["state"] = "present"
    elif p["state"] in ["absent", "removed"]:
        p["state"] = "absent"

    if p["update"]:
        update_plugins(module)

    if p["name"]:
        installed_plugins = list_plugins(module)

        plugin = p["name"]
        version = p["version"]
        plugin_source = p["plugin_source"]
        if p["state"] == "present":
            install_plugin(module, plugin, installed_plugins, version, plugin_source)


if __name__ == "__main__":
    main()
