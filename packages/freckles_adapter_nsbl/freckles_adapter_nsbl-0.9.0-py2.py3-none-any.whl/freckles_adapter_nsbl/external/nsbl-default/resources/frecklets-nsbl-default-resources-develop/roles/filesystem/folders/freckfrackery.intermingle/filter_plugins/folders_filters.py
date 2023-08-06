#!/usr/bin/python
import os

from ansible.errors import AnsibleError

ARCHIVE_EXTENSIONS = ["zip", "rar", "tgz", "tar.gz", "tar", "tar.bz2"]


class FilterModule(object):
    def filters(self):
        return {
            "calculate_checkout_method": self.calculate_checkout_method,
            "cleanup_path": self.cleanup_path,
        }

    def cleanup_path(self, path, local_user_home):

        if path.endswith("/"):
            path = path[0:-1]

        if path.startswith("~"):
            path = path[1:]
            if path .startswith(os.path.sep):
                path = os.path.join(local_user_home, path[1:])
            else:
                path = os.path.join("/home/", path)

        return path

    def calculate_checkout_method(
        self,
        url,
        absolute_local_path,
        source_folder_exists,
        source_folder_is_local,
        rsync_available,
    ):

        for ext in ARCHIVE_EXTENSIONS:
            if url.endswith(".{}".format(ext)):
                return "unarchive"

        if url.startswith("git") or url.endswith(".git"):
            return "git"

        if source_folder_exists:
            if rsync_available:
                return "rsync"
            else:
                return "copy"

        else:
            if source_folder_is_local and not source_folder_exists:
                raise AnsibleError(
                    "Source folder '{}' does not exist.".format(absolute_local_path)
                )
