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

from __future__ import absolute_import, division, print_function, unicode_literals

__metaclass__ = type

import json

from ansible.playbook.task_include import TaskInclude
from ansible.plugins.callback import CallbackBase
from ansible.module_utils import six
import re

FRECKLET_NAME = "frecklet"


def find_role_params(role):

    # if not role._attributes:
    #     parents = role._parents
    #     for p in parents:
    #         params = find_role_params(p)
    #         if params:
    #             return params
    #
    # else:
    temp = {}
    temp["vars"] = role._attributes.get("vars", {})
    temp["task_id"] = role._attributes.get("vars", {}).get("_task_id", -4)
    temp["default_vars"] = role._default_vars
    temp["name"] = role._role_name
    temp["uuid"] = role._uuid
    temp["path"] = role._role_path
    return temp

    # return {"task_id": -5, "vars": {}, "default_vars": {}}


def get_task_serialized(task):

    if task is None:
        return None

    if not hasattr(task, "name"):
        temp = None
    else:
        temp = task.name

    if not hasattr(task, "_role") or not task._role:
        role_params = {}
    else:
        role_params = find_role_params(task._role)

    if not temp:
        id = -2
        name = None
    else:
        match = re.match(r"\[(-?\d+)\](.*)", temp)

        if not match:
            id = role_params.get("task_id", -1)
            name = temp.strip()
            # name = role_params.get("name", "n/a")
        else:
            id = int(match.group(1))
            name = match.group(2).strip()

    task_dict = {}
    task_dict["name"] = name
    task_dict["id"] = id
    if hasattr(task, "uuid"):
        task_dict["uuid"] = task.uuid
    else:
        task_dict["uuid"] = None
    if hasattr(task, "ignore_errors"):
        task_dict["ignore_errors"] = task.ignore_errors
    else:
        task_dict["ignore_errors"] = None
    if hasattr(task, "action"):
        task_dict["action"] = task.action
    else:
        task_dict["action"] = None

    task_dict["role_params"] = role_params
    if hasattr(task, "get_path"):
        task_dict["task_path"] = task.get_path()
    else:
        # task_dict["task_path"] = task.__dict__.keys()
        task_dict["task_path"] = None
    # task_dict["details"] = task.__dict__.keys()
    if hasattr(task, "_parent") and task._parent:
        parent = get_task_serialized(task._parent)
        if parent:
            task_dict["parent"] = parent
        else:
            task_dict["parent"] = None
    else:
        task_dict["parent"] = None

    # if hasattr(task, "_attributes"):
    #     task_dict["attributes"] = task._attributes
    # else:
    #     task_dict["attributes"] = None

    return task_dict


class CallbackModule(CallbackBase):
    """
    Forward task, play and result objects to freckles.
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "stdout"
    CALLBACK_NAME = "freckles_callback"
    CALLBACK_NEEDS_WHITELIST = False

    def __init__(self, *args, **kwargs):
        super(CallbackModule, self).__init__(*args, **kwargs)
        self.task = None
        self.play = None
        self.task_serialized = False
        self.play_serialized = False

    def display(self, msg):

        if isinstance(msg, six.string_types):

            self._display.display(msg)

        else:

            dump = json.dumps(msg, ensure_ascii=False)
            self._display.display(dump)

    def get_task_serialized(self):

        if not self.task_serialized:

            self.task_serialized = get_task_serialized(self.task)

        return self.task_serialized

    def get_play_serialized(self):

        if not self.play_serialized:
            self.play_serialized = self.play.serialize()

        return self.play_serialized

    def get_task_detail(self, detail_key):

        if not self.task:
            return {"id": -3, "name": None, "action": None, "ignore_errors": None}

        return self.get_task_serialized().get(detail_key, None)

    def get_task_name(self):

        name = self.get_task_detail("name")
        return name

    def print_output(self, category, result, item=None):

        try:
            output = {}
            output["category"] = category

            play = self.get_play_serialized()
            env_id = play["vars"].get("_env_id", -100)
            env_name = play["vars"].get("_env_name", "n/a")

            output["env_id"] = env_id
            output["env_name"] = env_name

            if category == "play_start":
                output[FRECKLET_NAME] = None
                output["results"] = None
                output["item"] = None
                output["debug_data"] = None
                self.display(output)
                return

            task_details = self.get_task_serialized()
            output[FRECKLET_NAME] = task_details

            if item:
                output["item"] = item
            else:
                output["item"] = None

            if category == "task_start":
                output["debug_data"] = None
                output["results"] = None
            else:
                results = json.loads(self._dump_results(result._result))
                output["results"] = results
                # output["results"] = {}

                action = task_details.get("action", None)
                output["debug_data"] = None
                if action == "debug":
                    results.pop("item", None)
                    results.pop("failed", None)
                    results.pop("changed", None)
                    # we don't need the data again if it was a loop
                    if results.get("msg", None) != "All items completed":
                        output["debug_data"] = {"debug_vars": results}

            self.display(output)
        except (Exception) as e:
            import traceback

            tb = traceback.format_exc()
            self.display(tb)

    def v2_runner_on_ok(self, result, **kwargs):

        self.print_output("ok", result)

    def v2_runner_on_failed(self, result, **kwargs):

        self.print_output("failed", result)

    def v2_runner_on_unreachable(self, result, **kwargs):

        self.print_output("unreachable", result)

    def v2_runner_on_skipped(self, result, **kwargs):

        self.print_output("skipped", result)

    def v2_playbook_on_play_start(self, play):
        self.play = play
        self.play_serialized = False
        self.print_output("play_start", None)

    def v2_playbook_on_task_start(self, task, is_conditional):

        self.task = task
        self.task_serialized = False
        self.print_output("task_start", None)

    def v2_playbook_on_handler_task_start(self, task):

        self.task = task
        self.task_serialized = False
        self.print_output("task_start", None)

    def v2_playbook_on_notify(self, handler, host):

        self.task = handler
        self.task_serialized = False
        self.print_output("task_start", None)

    def v2_runner_item_on_ok(self, result):

        delegated_vars = result._result.get("_ansible_delegated_vars", None)
        if isinstance(result._task, TaskInclude):
            return
        elif result._result.get("changed", False):
            status = "changed"
        else:
            status = "ok"

        item = self._get_item(result._result)

        self.print_output("item_ok", result, item)

    def v2_runner_item_on_failed(self, result):
        item = self._get_item(result._result)
        self.print_output("item_failed", result, item)

    def v2_runner_item_on_skipped(self, result):
        item = self._get_item(result._result)
        self.print_output("item_skipped", result, item)

    def v2_on_any(self, *args, **kwargs):

        # pprint.pprint(args)
        pass
