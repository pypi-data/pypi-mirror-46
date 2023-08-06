# -*- coding: utf-8 -*-

import copy

from ansible.module_utils.six import iteritems

ARCHIVE_ENDINGS = ["zip", "tar.bz2", "tar.gz", "rar"]

ARCHIVE_UNARCHIVER_MAPPINGS = {
    "zip": {
        "pkg_desc": {"pkg": {"name": "unzip", "pkgs": {"debian": ["unzip"]}}},
        "executable": "unzip",
    }
}


class FilterModule(object):
    def filters(self):
        return {
            "filter_required_pkg_mgrs": self.filter_required_pkg_mgrs,
            "get_archive_formats": self.get_archive_formats_filter,
            "get_missing_unarchivers": self.get_missing_unarchivers,
        }

    def get_missing_unarchivers(self, archive_formats, executables):

        result = []
        for af in archive_formats:
            ua = ARCHIVE_UNARCHIVER_MAPPINGS.get(af, None)
            if ua is None:
                # we'll just hope the unarchiver is available
                continue

            executable = ua["executable"]
            available_executables = executables.get(executable, [])
            if available_executables:
                continue

            if ua["pkg_desc"] not in result:
                result.append(ua["pkg_desc"]["pkg"])

        return result

    def get_archive_formats_filter(self, pkg_list):

        result = set()
        for pkg in pkg_list:
            src = pkg.get("src", None)
            if not src:
                continue

            for end in ARCHIVE_ENDINGS:
                if src.endswith("." + end):
                    result.add(end)
                    break

        return list(result)

    def filter_existing_pkg_mgrs(self, pkg_mgrs, freckles_facts):

        result = {}
        for pkg_mgr, details in iteritems(pkg_mgrs):

            fpm = freckles_facts["pkg_mgrs"].get(pkg_mgr, None)
            if fpm is None:
                result[pkg_mgr] = details
            elif not fpm["is_available"]:
                result[pkg_mgr] = details

            # TODO: check package manager dependencies, like python-apt

        return result

    def filter_required_pkg_mgrs(
        self, package_list, init_pkg_mgrs={}, freckles_facts=None
    ):
        if isinstance(init_pkg_mgrs, (list, tuple)):
            temp = {}
            for p in init_pkg_mgrs:
                temp[p] = {}
            init_pkg_mgrs = temp

        result = copy.deepcopy(init_pkg_mgrs)
        for pkg_item in package_list:
            pkg_mgr = pkg_item["pkg_mgr"]
            pkg_become = pkg_item["become"]

            # in case pkg_mgr needs both become and not become, we go
            # with become
            if pkg_mgr not in result.keys() or result[pkg_mgr]["become"] == False:
                result[pkg_mgr] = {"become": pkg_become}
            result[pkg_mgr].setdefault("packages", []).append(pkg_item)

        if freckles_facts is not None:
            result = self.filter_existing_pkg_mgrs(
                result, freckles_facts=freckles_facts
            )
        return result
