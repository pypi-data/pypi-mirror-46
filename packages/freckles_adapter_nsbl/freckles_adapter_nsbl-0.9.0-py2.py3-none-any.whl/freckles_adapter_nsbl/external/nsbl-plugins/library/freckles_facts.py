#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2018, Markus Binsteiner
#
# Licensed under The Parity Public license, Version 3.0.0 (the "license");
# and you may not use this file except in compliance with the license.
# You may obtain a copy of the License at
#
#  https://licensezero.com/licenses/parity


from ansible.module_utils.basic import *
from ansible.module_utils.basic import AnsibleModule


def can_passwordless_sudo():
    """Checks if the user can use passwordless sudo on this host."""

    if os.geteuid() == 0:
        return True

    FNULL = open(os.devnull, "w")
    # use -k to ignore any existing sudo token
    p = subprocess.Popen(
        "sudo -k -n true",
        shell=True,
        stdout=FNULL,
        stderr=subprocess.STDOUT,
        close_fds=True,
    )
    r = p.wait()
    return r == 0


def check_apt():

    has_python_apt = True
    try:
        import apt
        import apt.debfile
        import apt_pkg
    except ImportError:
        has_python_apt = False

    return {"has_python_apt": has_python_apt}


OTHER_PATHS_TO_CHECK = [
    os.path.expanduser("~/.local/bin"),
    os.path.expanduser("~/.local/share/inaugurate/bin"),
    os.path.expanduser("~/.local/share/inaugurate/conda/bin"),
]

PKG_MGRS_TO_CHECK = {
    "apt": {"executables": [["apt", "apt-get"]], "details_check": check_apt},
    "pip": {"executables": ["pip", "virtualenv"]},
    "vagrant_plugin": {"executables": ["vagrant"]},
    "git": {"executables": ["git"]},
    "conda": {"executables": ["conda"]},
    "homebrew": {"executables": ["brew"]},
    "nix": {"executables": ["nix", "nix-env"]},
}


def is_exe(fpath):
    """Checks whether the specified file is executable."""
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def which(module, program):
    """Tries to find all paths where the specified executable can be found."""

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return [program]
    else:
        paths = os.environ["PATH"].split(os.pathsep) + OTHER_PATHS_TO_CHECK

        result = []
        for path in paths:
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                if program == "git":
                    avail = check_git_available(module, exe_file)
                    if not avail:
                        continue
                result.append(os.path.join(path, program))

        if program == "git":
            temp = []
            for path in result:
                avail = check_git_available(module, path)
                if avail:
                    temp.append(path)
            result = temp

        return result


def check_git_available(module, path):
    """Git is a special case, as Mac OS X comes with a script that tells you that git is not available.

    Great idea, he?
    """

    try:
        rc, stdout, stderr = module.run_command([path, "--help"], check_rc=False)
        # git_output = "xcode-select"
        if "xcode-select" in stderr:
            return False
        else:
            return True
    except:
        return False


def check_pkg_mgrs(module):
    """Checks which ones of the package managers described in PKG_MGRS_TO_CHECK variable are available."""

    result = {}
    for pkg_mgr, details in iteritems(PKG_MGRS_TO_CHECK):

        executables = details.get("executables", [])
        pm_exes = {}
        pm_available = True
        for exe in executables:
            if isinstance(exe, (list, tuple)):
                # means only one of those needs to be available
                match = False
                for e in exe:
                    paths = which(module, e)
                    if paths:
                        match = True
                        pm_exes.setdefault(e, []).extend(paths)
                if not match:
                    pm_available = False
                    pm_exes.setdefault(e, [])
            else:
                paths = which(module, exe)
                if paths:
                    pm_exes.setdefault(exe, []).extend(paths)
                else:
                    pm_available = False
                    pm_exes.setdefault(exe, [])

        if "details_check" in PKG_MGRS_TO_CHECK.get(pkg_mgr, {}).keys():
            details = PKG_MGRS_TO_CHECK[pkg_mgr]["details_check"]()
        else:
            details = {}

        result[pkg_mgr] = {}
        result[pkg_mgr]["is_available"] = pm_available
        result[pkg_mgr]["executables"] = pm_exes
        result[pkg_mgr]["details"] = details

    return result


def main():
    module = AnsibleModule(
        argument_spec=dict(executables=dict(required=False, type="list")),
        supports_check_mode=False,
    )

    p = module.params

    result_facts = {}
    executables_to_check = p.get("executables", None)
    if executables_to_check is None:
        executables_to_check = []
    executables = {}
    for exe in executables_to_check:
        paths = which(module, exe)
        executables[exe] = {"available": bool(paths), "paths": paths}
    result_facts["executables"] = executables

    pkg_mgrs = check_pkg_mgrs(module)
    result_facts["pkg_mgrs"] = pkg_mgrs
    result_facts["can_passwordless_sudo"] = can_passwordless_sudo()
    module.exit_json(
        changed=False, ansible_facts=dict({"__freckles_facts__": result_facts})
    )


if __name__ == "__main__":
    main()
