#!/usr/bin/python

import copy
import os
from collections import OrderedDict
from ansible.errors import AnsibleFilterError

from frkl import frkl

try:
    set
except NameError:
    from sets import Set as set

METADATA_CONTENT_KEY = "freckle_metadata_file_content"


class FilterModule(object):

    def filters(self):
        return {
            # "join_folders_filter": self.join_folders_filter,
            # "parse_freckle_metadata": self.parse_freckle_metadata,

            # 'create_dotfiles_packages': self.create_dotfiles_packages,
            'get_subfolders': self.get_subfolders,
            'overlay_package_metadata': self.overlay_package_metadata,
            'overlay_stow_metadata': self.overlay_stow_metadata,
            # 'create_folder_packages': self.create_folder_packages,
            # 'create_stow_folders_metadata': self.create_stow_folders_metadata,
        }

    # def join_folders_filter(self, folders, token):
    #
    #     return token.join(folders)
    #
    # def parse_freckle_metadata(self, freckle_files):
    #
    #     profiles = OrderedDict()
    #     for path, f_files in freckle_files.items():
    #
    #         freckle_files = f_files["freckle_files"]
    #         invalid_freckle_files = f_files["freckle_files_invalid"]
    #
    #         for path, md in freckle_files.items():
    #
    #             if os.path.basename(path) != ".freckle":
    #                 continue
    #
    #             profiles.setdefault()

    def get_subfolders(self, files, base_path):

        subfolders = set()
        for path in files:

            if not path.startswith(base_path):
                continue

            rel_path = os.path.relpath(path, base_path)
            path_tokens = rel_path.split(os.path.sep)
            if len(path_tokens) < 2:
                continue
            subfolders.add(path_tokens[0])

        return list(sorted(subfolders))

    def overlay_package_metadata(self, packages, overlay):

        result = []
        for p in packages:
            install_metadata = overlay.get(p, {}).get("install", None)
            if install_metadata is None:
                result.append(p)
            elif install_metadata is False:
                result.append({"name": p, "no_install": True})
            elif install_metadata is True:
                result.append(p)
            elif not isinstance(install_metadata, dict):
                raise AnsibleFilterException("Invalid metadata for folder package 'p', needs to be dict (or boolean): {}".format(install_metadata))
            else:
                install_metadata["name"] = p
                result.append(install_metadata)

        return result

    def overlay_stow_metadata(self, packages, overlay):

        result = {}
        for p in packages:
            stow_metadata = overlay.get(p, {}).get("stow", None)
            if stow_metadata is None:
                result[p] = {}
            elif stow_metadata is False:
                result[p] = {"no_stow": True}
            elif stow_metadata is True:
                result[p] = {"no_stow": False}
            elif not isinstance(stow_metadata, dict):
                raise AnsibleFilterException("Invalid metadata for folder package 'p', needs to be dict (or boolean): {}".format(stow_metadata))
            else:
                result[p] = stow_metadata

        return result



    # def create_folder_packages(self, package_names, extra_vars):
    #
    #     result = []
    #
    #     for name in package_names:
    #         details = {"name": name}
    #         if name in extra_vars.keys():
    #             no_install = extra_vars.get(name, {}).get("no_install", False)
    #             if no_install:
    #                 continue
    #             package_md = extra_vars[name].get("package", None)
    #             if package_md:
    #                 frkl.dict_merge(details, package_md, copy_dct=False)
    #         result.append({"vars": details})
    #
    #     return result
    #
    # def create_stow_folders_metadata(self, subfolders, freckle_path, freckle_vars, extra_vars):
    #
    #     default_stow_target = freckle_vars.get("dotfiles_stow_target", None)
    #     default_delete_conflicts = freckle_vars.get("dotfiles_stow_delete_conflicts", None)
    #     default_no_stow = freckle_vars.get("dotfiles_no_stow", None)
    #     default_stow_become = freckle_vars.get("dotfiles_stow_become", None)
    #
    #     result = []
    #     for folder_name in subfolders:
    #
    #         folder_extra_vars = extra_vars.get(folder_name, {})
    #
    #         md = {}
    #         md["stow_folder_name"] = folder_name
    #         md["stow_folder_parent"] = freckle_path
    #         if "stow_target_dir" in folder_extra_vars.keys():
    #             md["stow_target_dir"] = folder_extra_vars["stow_target_dir"]
    #         elif default_stow_target is not None:
    #             md["stow_target_dir"] = default_stow_target
    #         if "stow_delete_conflicts" in folder_extra_vars.keys():
    #             md["stow_delete_conflicts"] = folder_extra_vars["stow_delete_conflicts"]
    #         elif default_delete_conflicts is not None:
    #             md["stow_delete_conflicts"] = dfault_delete_conflicts
    #         if "no_stow" in folder_extra_vars.keys():
    #             md["no_stow"] = folder_extra_vars["no_stow"]
    #         elif default_no_stow is not None:
    #             md["no_stow"] = default_no_stow
    #         if "stow_become" in folder_extra_vars.keys():
    #             md["stow_become"] = folder_extra_vars["stow_become"]
    #         elif default_stow_become is not None:
    #             md["stow_become"] = default_stow_become
    #
    #         result.append(md)
    #
    #     return result
    #
    # def create_dotfiles_packages(self, profile_vars):
    #
    #     result = []
    #     for folder, subfolder_list in profile_vars.items():
    #
    #         for subfolder_metadata in subfolder_list:
    #
    #             md = {}
    #             md["stow_source"] = subfolder_metadata['freckles_app_dotfile_folder_path']
    #             md["stow_folder_name"] = subfolder_metadata['freckles_app_dotfile_folder_name']
    #             md["name"] = subfolder_metadata['freckles_app_dotfile_folder_name']
    #             md["stow_folder_parent"] = subfolder_metadata['freckles_app_dotfile_parent_path']
    #
    #             parent_details = subfolder_metadata.get('freckles_app_dotfile_parent_details', {})
    #
    #             extra_vars = copy.deepcopy(parent_details.get("extra_vars", {}).get(md["name"], {}))
    #
    #             package_md = extra_vars.pop("package", None)
    #             overlay = frkl.dict_merge(md, extra_vars)
    #             if package_md:
    #                 frkl.dict_merge(overlay, package_md, copy_dct=False)
    #
    #             result.append({"vars": overlay})
    #
    #     return result
