# -*- coding: utf-8 -*-


class FilterModule(object):

    def filters(self):

        return {
            "filter_non_ansible_role": self.filter_non_ansible_role,
            "filter_ansible_role": self.filter_ansible_role
        }

    def filter_ansible_role(self, package_list):

        result = []
        for p in package_list:
            if p["pkg_mgr"] == "ansible_role":
                result.append(p)
        return result

    def filter_non_ansible_role(self, package_list):

        result = []
        for p in package_list:
            if p["pkg_mgr"] != "ansible_role":
                result.append(p)
        return result
