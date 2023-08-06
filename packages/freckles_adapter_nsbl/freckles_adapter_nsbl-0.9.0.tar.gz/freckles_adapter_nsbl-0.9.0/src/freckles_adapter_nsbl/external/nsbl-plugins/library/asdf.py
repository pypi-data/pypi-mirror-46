#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Adam Frey
# Copyright (c) 2018 Markus Binsteiner

DOCUMENTATION = """
---
module: asdf
short_description: Manage packages with asdf
"""

EXAMPLES = """
# Install package foo
- asdf: name=foo state=present
"""

from ansible.module_utils.basic import *

ASDF_PATH = os.path.join(os.environ["HOME"], ".asdf")
ASDF_SOURCE_FILE = os.path.join(ASDF_PATH, "asdf.sh")
ASDF_EXE = os.path.join(ASDF_PATH, "bin", "asdf")

# whether to wrap the command in a 'source .asdf/asdf.sh' invocation
WRAP = True


def get_latest_version(module, plugin, all_versions=None):

    if all_versions is None:
        all_versions = list_available_versions(module, plugin)

    latest = None
    if plugin == "python":
        for v in all_versions:
            if v.startswith("3") and "dev" not in v:
                latest = v

    if not latest:
        return all_versions[-1]
    else:
        return latest


def list_plugins(module):
    if WRAP:
        cmd = 'bash -c "source {}; {} plugin-list"'.format(ASDF_SOURCE_FILE, ASDF_EXE)
    else:
        cmd = "{} plugin-list".format(ASDF_EXE)

    rc, stdout, stderr = module.run_command(cmd, check_rc=False)

    if "No plugins installed" in stderr:
        return []
    else:
        return stdout.split("\n")


def install_plugin(module, plugin):

    if module.check_mode:

        if plugin in list_plugins(module):
            return False

    if plugin in list_plugins(module):
        return False

    if WRAP:
        cmd = 'bash -c "source {}; {} plugin-add {}"'.format(
            ASDF_SOURCE_FILE, ASDF_EXE, plugin
        )
    else:
        cmd = "{} plugin-add {}".format(ASDF_EXE, plugin)

    rc, stdout, stderr = module.run_command(cmd, check_rc=False)

    if rc != 0:
        module.fail_json(
            msg="failed to install asdf plugin '{}': {}".format(plugin, stderr)
        )

    return True


def list_versions(module, plugin):

    if WRAP:
        cmd = 'bash -c "source {}; {} list {}"'.format(
            ASDF_SOURCE_FILE, ASDF_EXE, plugin
        )
    else:
        cmd = "{} list {}".format(ASDF_EXE, plugin)

    rc, stdout, stderr = module.run_command(cmd, check_rc=False)

    if "No versions installed" in stderr:
        return []
    else:
        return stdout.split("\n")


def list_available_versions(module, plugin):

    if WRAP:
        cmd = 'bash -c "source {}; {} list-all {}"'.format(
            ASDF_SOURCE_FILE, ASDF_EXE, plugin
        )
    else:
        cmd = "{} list {}".format(ASDF_EXE, plugin)

    rc, stdout, stderr = module.run_command(cmd, check_rc=True)

    return stdout.split("\n")


def install_version(module, plugin, version=None, set_global=True):

    installed_versions = list_versions(module, plugin)
    all_versions = list_available_versions(module, plugin)
    if version is None:
        version = "latest"

    if version == "latest":
        version = get_latest_version(module, plugin, all_versions=all_versions)

    if version not in all_versions:
        module.fail_json(
            msg="Version '{}' for asdf plugin '{}' not available.".format(
                version, plugin
            )
        )

    if module.check_mode:
        if version in installed_versions:
            return False
        else:
            return True

    if version in installed_versions:
        return False

    if WRAP:
        cmd = 'bash -c "source {}; {} install {} {}"'.format(
            ASDF_SOURCE_FILE, ASDF_EXE, plugin, version
        )
    else:
        cmd = "{} list {} {}".format(ASDF_EXE, plugin, version)

    rc, stdout, stderr = module.run_command(cmd, check_rc=False)

    if rc != 0:
        module.fail_json(
            msg="failed to install asdf runtime '{}', version '{}': {}".format(
                plugin, version, stderr
            )
        )

    if set_global:
        set_version(module, plugin, version)

    return version


def set_version(module, plugin, version):

    if WRAP:
        cmd = 'bash -c "source {}; {} global {} {}"'.format(
            ASDF_SOURCE_FILE, ASDF_EXE, plugin, version
        )
    else:
        cmd = "{} global {} {}".format(ASDF_EXE, plugin, version)

    rc, stdout, stderr = module.run_command(cmd, check_rc=True)

    if rc != 0:
        module.fail_json(
            msg="failed to set asdf version '{}', for plugin '{}': {}".format(
                version, plugin, stderr
            )
        )


def remove_plugin(module, plugin):

    if module.check_mode:

        if plugin in list_plugins(module):
            return True

    if plugin not in list_plugins(module):
        return False

    if WRAP:
        cmd = 'bash -c "source {}; {} plugin-remove {}"'.format(
            ASDF_SOURCE_FILE, ASDF_EXE, plugin
        )
    else:
        cmd = "{} plugin-remove {}".format(ASDF_EXE, plugin)

    rc, stdout, stderr = module.run_command(cmd, check_rc=False)

    if rc != 0:
        module.fail_json(
            msg="failed to remove asdf plugin '{}': {}".format(plugin, stderr)
        )

    return True


def main():
    module = AnsibleModule(
        argument_spec=dict(
            plugin=dict(type="str"),
            state=dict(
                default="present", choices=["present", "installed", "absent", "removed"]
            ),
            version=dict(type="str"),
        ),
        # required_one_of=[["plugin"]],
        # mutually_exclusive=[["plugin"]],
        supports_check_mode=True,
    )

    if not os.path.exists(ASDF_SOURCE_FILE):
        module.fail_json(
            msg="cannot find asdf install, looking for %s" % (ASDF_SOURCE_FILE)
        )

    p = module.params

    # normalize the state parameter
    if p["state"] in ["present", "installed"]:
        p["state"] = "present"
    elif p["state"] in ["absent", "removed"]:
        p["state"] = "absent"

    version = p["version"]
    plugin = p["plugin"]
    if p["state"] == "present":
        installed = install_plugin(module, plugin)
        if not version and module.check_mode:
            if not installed:
                module.exit_json(changed=False, name=plugin)
            else:
                module.exit_json(changed=True, name=plugin)
        elif not version:
            if installed:
                module.exit_json(
                    changed=True, msg="installed asdf plugin '{}'".format(plugin)
                )
            else:
                module.exit_json(
                    changed=False,
                    msg="asdf runtime '{}', version '{}' already present".format(
                        plugin, version
                    ),
                )

    elif p["state"] == "absent":
        removed = remove_plugin(module, plugin)
        if not version and module.check_mode:
            if removed:
                module.exit_json(changed=True, name=plugin)
            else:
                module.exit_json(changed=False, name=plugin)
        elif not version:
            if removed:
                module.exit_json(
                    changed=True, msg="removed asdf plugin '{}'".format(plugin)
                )
            else:
                module.exit_json(
                    changed=False, msg="asdf plugin '{}' not installed".format(plugin)
                )

    if version:
        if p["state"] == "present":
            installed = install_version(module=module, plugin=plugin, version=version)
            if module.check_mode:
                if not installed:
                    module.exit_json(changed=False, name=version)
                else:
                    module.exit_json(changed=True, name=version)
            else:
                if installed:
                    module.exit_json(
                        changed=True,
                        msg="Installed version '{}' using asdf plugin '{}'.".format(
                            installed, plugin
                        ),
                    )
                else:
                    module.exit_json(
                        changed=False,
                        msg="Version '{}' for asdf plugin '{}' already present.".format(
                            version, plugin
                        ),
                    )


if __name__ == "__main__":
    main()
