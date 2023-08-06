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
from ansible.module_utils.six import iteritems
from ansible.plugins.action import ActionBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display

    display = Display()


class ActionModule(ActionBase):

    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        keys = self._task.args.pop("keys", None)
        if keys is None:
            return {"failed": True, "msg": "No 'keys' property provided"}

        default = self._task.args.pop("ignore_case", None)
        fail_if_empty = boolean(self._task.args.pop("fail_if_empty", False))
        # fail_if_not_defined = boolean(self._task.args.pop("fail_if_not_defined", True))

        # if isinstance(keys, (list, tuple)):
        #     temp = {}
        #     for key in keys:
        #         temp[key] = key
        #     keys = temp

        result_value = {}
        for k, v in iteritems(keys):
            if not v and fail_if_empty:
                return {"failed": True, "msg": "Value for '{}' is empty.".format(k)}
            elif not v:
                v = default
            result_value[k] = v

        result["frecklet_result"] = result_value

        result["_ansible_verbose_always"] = True
        result["changed"] = False
        return result
