# -*- coding: utf-8 -*-
import os

from freckles.defaults import FRECKLES_SHARE_DIR
from frutils import merge_list_of_dicts

FRECKLES_NSBL_CONNECTOR_MODULE_FOLDER = os.path.dirname(__file__)

NSBL_EXTRA_PLUGINS = os.path.join(
    FRECKLES_NSBL_CONNECTOR_MODULE_FOLDER, "external", "nsbl-plugins"
)
NSBL_EXTRA_CALLBACKS = os.path.join(NSBL_EXTRA_PLUGINS, "callback_plugins")
# NSBL_ROLES = os.path.join(
#     FRECKLES_NSBL_CONNECTOR_MODULE_FOLDER, "external", "default-nsbl", "resources", "roles"
# )
NSBL_RUN_DIR = os.path.expanduser("~/.local/share/nsbl/runs/archive")
NSBL_CURRENT_RUN_SYMLINK = os.path.expanduser("~/.local/share/nsbl/runs/current")
NSBL_DEFAULT_ROLE_REPO = os.path.join(
    FRECKLES_NSBL_CONNECTOR_MODULE_FOLDER, "external", "nsbl-default", "resources"
)
NSBL_DEFAULT_TASKLIST_REPO = os.path.join(
    FRECKLES_NSBL_CONNECTOR_MODULE_FOLDER, "external", "nsbl-default", "resources"
)
NSBL_COMMUNITY_ROLE_REPO = os.path.join(
    FRECKLES_NSBL_CONNECTOR_MODULE_FOLDER, "external", "nsbl-community", "resources"
)
NSBL_COMMUNITY_TASKLIST_REPO = os.path.join(
    FRECKLES_NSBL_CONNECTOR_MODULE_FOLDER, "external", "nsbl-community", "resources"
)

NSBL_INTERNAL_TASKLIST_REPO = os.path.join(
    FRECKLES_NSBL_CONNECTOR_MODULE_FOLDER, "external", "nsbl-tasklists"
)

NSBL_DEFAULT_FRECKLET_REPO = os.path.join(
    FRECKLES_NSBL_CONNECTOR_MODULE_FOLDER, "external", "nsbl-default", "frecklets"
)
NSBL_COMMUNITY_FRECKLET_REPO = os.path.join(
    FRECKLES_NSBL_CONNECTOR_MODULE_FOLDER, "external", "nsbl-community", "frecklets"
)

NSBL_USER_ROLE_REPO = os.path.join(FRECKLES_SHARE_DIR, "roles")
NSBL_USER_TASKLIST_REPO = os.path.join(FRECKLES_SHARE_DIR, "ansible-tasklists")

COMMUNITY_REPO_URL = "https://gitlab.com/freckles-io/community-nsbl.git"


NSBL_COMMUNITY_FRECKLETS_REPO_URL = (
    "https://gitlab.com/frecklets/frecklets-nsbl-community.git"
)
NSBL_COMMUNITY_RESOURCES_REPO_URL = (
    "https://gitlab.com/frecklets/frecklets-nsbl-community-resources.git"
)


# COMMUNITY_NSBL_FOLDER = os.path.join(COMMUNITY_FOLDER, "community-nsbl")


# COMMUNITY_REPO_DESC = {
#     "path": COMMUNITY_NSBL_FOLDER,
#     "url": COMMUNITY_REPO_URL,
#     "alias": "community",
#     "remote": True,
#     "content_type": "frecklets",
# }

# NSBL_DEFAULT_REPO_ALIASES = {
#     "default": {
#         "roles": [NSBL_DEFAULT_ROLE_REPO],
#         "frecklets": [NSBL_DEFAULT_FRECKLET_REPO],
#         "ansible-tasklists": [NSBL_DEFAULT_TASKLIST_REPO],
#     },
#     "user": {
#         "roles": [NSBL_USER_ROLE_REPO],
#         "ansible-tasklists": [NSBL_USER_TASKLIST_REPO],
#     },
#     "community": {
#         "frecklets": [COMMUNITY_REPO_URL],
#         "roles": [COMMUNITY_REPO_URL],
#         "ansible-tasklists": [COMMUNITY_REPO_URL],
#     },
# }


def PICK_ALL_NSBL_FILES_FUNCTION(path):
    """Default implementation of an 'is_*_file' method."""

    if path.endswith(".nsbl") or path.endswith(".yml"):
        return os.path.splitext(os.path.basename(path))[0]
    else:
        return


# NSBL_DEFAULT_READER_PROFILE = {
#     "use_files": True,
#     "use_metadata_files": True,
#     "use_parent_metadata_files": True,
#     "use_subfolders_as_tags": True,
#     "get_pkg_name_function": PICK_ALL_NSBL_FILES_FUNCTION,
#     "get_pkg_name_function_metadata": PICK_ALL_NSBL_FILES_FUNCTION,
#     "default_metadata_key": "frecklet",
#     "move_list_to_dict_key": FRECKLETS_KEY,
# }

NSBL_INDEX_SCHEMA = {
    "allow_remote": {
        "type": "boolean",
        "default": False,
        "doc": {
            "short_help": "whether to allow remote roles and/or tasklists, can be overwritten by 'allow_remote_roles' and 'allow_remote_tasklists'"
        },
    },
    "force_show_log": {
        "required": False,
        "doc": {
            "short_help": "disable the hiding of task details when those contain secret variables, only use this for debugging purposes"
        },
        "type": "boolean",
        "default": False,
    },
    "allow_remote_roles": {
        "type": "boolean",
        "doc": {"short_help": "whether to allow remote roles"},
    },
    "allow_remote_tasklists": {
        "type": "boolean",
        "doc": {"short_help": "whether to allow remote tasklists"},
    },
    # "generate_role_frecklets": {
    #     "type": "boolean",
    #     "default": False,
    #     "doc": {
    #         "short_help": "whether to auto-generate frecklets from all available Ansible roles"
    #     },
    # },
    # "generate_tasklist_frecklets": {
    #     "type": "boolean",
    #     "default": False,
    #     "doc": {
    #         "short_help": "whether to auto-generate frecklets from all available Ansible roles"
    #     },
    # },
    # "convert_ansible_template_markers": {
    #     "type": "boolean",
    #     "default": False,
    #     "doc": {
    #         "help": "Converts template markers in Ansible-type tasklists to freckles ones ('{{' to '{{::'. This is not implemented yet.",
    #         "short_help": "not implemented yet",
    #     },
    # },
    # "guess_args_for_roles": {
    #     "type": "boolean",
    #     "default": False,
    #     "doc": {
    #         "help": "Guesses arguments for Ansible roles from their default files and auto-generates commandline arguments from those guesses. This does not always work very well, so you might have to provide a vars file instead.",
    #         "short_help": "auto-generates cli arguments from role default/main.yml files",
    #     },
    # },
}

NSBL_RUN_PARAMETERS_CONFIG_SCHEMA = {
    # "nsbl_run_folder": {
    #     "type": "string",
    #     "default": NSBL_RUN_DIR + "_nsbl",
    #     "doc": {"short_help": "the target for the generated Ansible environment"},
    #     "target_key": "run_folder",
    # },
    # "show_tasks_with_password_in_log": {
    #     "type": "boolean",
    #     "default": False,
    #     "doc": {
    #         "short_help": "whether to show tasks that contain a password variable in logs (only enable for debugging!)"
    #     },
    # },
    # "nsbl_current_run_folder": {
    #     "type": "string",
    #     "default": NSBL_CURRENT_RUN_SYMLINK,
    #     "doc": {"short_help": "target of a symlink the current Ansible environment"},
    #     "target_key": "add_symlink_to_env",
    # },
    # "nsbl_force_run_folder": {
    #     "type": "boolean",
    #     "default": True,
    #     "target_key": "force",
    #     "doc": {
    #         "short_help": "overwrite a potentially already existing Ansible environment"
    #     },
    # },
    # "nsbl_add_timestamp_to_env": {
    #     "type": "boolean",
    #     "default": True,
    #     "doc": {
    #         "short_help": "whether to add a timestamp to the Ansible run environment folder name"
    #     },
    #     "target_key": "add_timestamp_to_env"
    # },
    "use_mitogen": {
        "type": "boolean",
        "default": False,
        "doc": {
            "short_help": "whether to use mitogen to speed up Ansible playbook execution"
        },
        "tags": ["safe"],
    },
    "use_ara": {
        "type": "boolean",
        "default": False,
        "doc": {"short_help": "whether to use ara (https://ara.readthedocs.io)"},
        "tags": ["safe"],
    },
}

NSBL_CONNECTION_CONFIG_SCHEMA = {
    "ssh_key": {
        "type": "string",
        "doc": {"short_help": "the path to a ssh key identity file"},
        # "target_key": "ansible_ssh_private_key_file",
    },
    "user": {
        "type": "string",
        "doc": {"short_help": "the user name to use for the connection"},
    },
    "connection_type": {
        "type": "string",
        "doc": {"short_help": "the connection type, probably 'ssh' or 'local'"},
        # "target_key": "ansible_connection",
    },
    "port": {
        "type": "integer",
        "default": 22,
        "doc": {"short_help": "the ssh port to connect to in case of a ssh connection"},
        "target_key": "ssh_port",
    },
    "host": {
        "type": "string",
        "doc": {"short_help": "the host to connect to"},
        "default": "localhost",
        # "target_key": "host"
    },
    "host_ip": {"type": "string", "doc": {"short_help": "the host ip, optional"}},
}

NSBL_CONTROL_SCHEMA = {
    "elevated": {
        "type": "boolean",
        "doc": {"short_help": "this run needs elevated permissions"},
        "target_key": "elevated_permissions_required",
    },
    "passwordless_sudo": {
        "type": "boolean",
        "target_key": "passwordless_sudo_possible",
        "doc": {
            "short_help": "the user can do passwordless sudo on the host where those tasks are run"
        },
    },
    "run_callback": {
        "required": False,
        "doc": {"short_help": "the output callback to use"},
        "target_key": "callback",
    },
    "no_run": {
        "type": "boolean",
        "coerce": bool,
        "doc": {
            "short_help": "only create the Ansible environment, don't execute any playbooks"
        },
    },
    "output": {"type": "string", "doc": {"short_help": "the callback name"}},
    "minimal_facts_only": {
        "type": "boolean",
        "coerce": bool,
        "doc": {
            "short_help": "whether to not execute basic box tasks (install python, etc.). Most likely you want that set to False."
        },
        "default": False,
    },
}

NSBL_RUN_CONFIG_SCHEMA = merge_list_of_dicts(
    [
        NSBL_CONNECTION_CONFIG_SCHEMA,
        NSBL_CONTROL_SCHEMA,
        NSBL_RUN_PARAMETERS_CONFIG_SCHEMA,
    ]
)
NSBL_CONFIG_SCHEMA = merge_list_of_dicts([NSBL_INDEX_SCHEMA])
