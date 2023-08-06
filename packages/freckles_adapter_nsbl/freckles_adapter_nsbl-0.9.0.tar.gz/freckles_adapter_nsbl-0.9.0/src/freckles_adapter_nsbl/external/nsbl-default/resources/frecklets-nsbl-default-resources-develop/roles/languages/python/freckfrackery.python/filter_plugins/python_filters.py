import os

from ansible.errors import AnsibleError

PYTHON_PACKAGE_MAP = {
    "2": {
        "Debian": [
            "python",
            "python-dev",
            "python-setuptools",
            "python-pip",
            "python-virtualenv",
            "virtualenv"
        ]
    },
    "3": {
        "Debian": [
            "python3",
            "python3-dev",
            "python3-venv",
            "python3-setuptools",
            "python3-pip",
            "python3-virtualenv",
            "virtualenv"
        ]
    },
}

PYTHON_PACKAGE_MAP_3 = {}


class FilterModule(object):
    def filters(self):
        return {
            "calculate_virtualenv_path": self.calculate_virtualenv_path,
            "calculate_python_version": self.calculate_python_version,
            "get_python_packages": self.get_python_packages,
        }

    def calculate_virtualenv_path(
        self, venv_name, venv_base_path, python_type, user, user_home
    ):

        if python_type == "pyenv":

            if user == "root":
                return os.path.join("/usr", "local", "pyenv", "versions", venv_name)
            else:
                if user_home:
                    return os.path.join(user_home, ".pyenv", "versions", venv_name)
                else:
                    return os.path.join("/home", user, ".pyenv", "versions", venv_name)
        else:
            if venv_base_path:
                return os.path.join(venv_base_path, venv_name)

            if user == "root":
                return os.path.join("/usr", "local", "virtualenvs")
            else:
                if user_home:
                    return os.path.join(user_home, ".virtualenvs", venv_name)
                else:
                    return os.path.join("/home", user, ".virtualenvs", venv_name)

    def calculate_python_version(self, python_version, python_type):

        if python_type == "system":

            if python_version == "latest":
                return "3"

            if python_version not in ["2", "3"]:
                raise AnsibleError("Used Python version: {}, but only major version numbers supported for 'system' install: use '2' or '3'".format(python_version))

            # if len(python_version.split(".")) > 2:
            #     raise AnsibleError("Can't use 3-digit Python version for 'system' Python type.")

            # TODO: dist/platform dependent checks

            return python_version
        else:
            if python_version == "latest":
                return "3.7.3"
            else:
                return python_version

    def get_python_packages(self, python_version, platform_matchers):

        if python_version not in ["2", "3"]:
            raise AnsibleError("Used Python version: {}, but only major version numbers supported for 'system' install: use '2' or '3'".format(python_version))

        if "Debian" not in platform_matchers:
            raise AnsibleError("Other platforms than Debian currently not supported.")

        result = None
        for pm in platform_matchers:
            result = PYTHON_PACKAGE_MAP[python_version].get(pm)
            if result is not None:
                break

        if result is None:
            raise AnsibleError("Could not find any python {} packages for the current platform.".format(python_version))

        return {
            "name": "python packages",
            "pkg_mgr": "auto",
            "pkgs": result
        }
