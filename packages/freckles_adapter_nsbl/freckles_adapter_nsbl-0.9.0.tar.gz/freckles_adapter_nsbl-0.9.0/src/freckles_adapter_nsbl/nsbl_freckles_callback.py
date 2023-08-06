# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from collections import Sequence

import click
from six import string_types

from freckles.defaults import FRECKLET_KEY_NAME
from frutils import readable
from nsbl.nsbl_callback import log


class NsblTaskDetail(object):
    def __init__(
        self,
        env_id,
        env_name,
        category,
        task,
        results,
        item,
        debug_data,
        role,
        tasklist,
    ):

        self._category = category
        self._env_id = env_id
        self._env_name = env_name
        self._task = task
        self._results = results
        self._item = item
        self._role = role
        self._tasklist = tasklist
        self._debug_data = debug_data

        self._stdout = None
        self._stderr = None
        self._processed_stdout_stderr = False

    @property
    def category(self):

        if not self._category:
            return "default"
        else:
            return self._category

    @property
    def env_id(self):

        return self._env_id

    @property
    def env_name(self):

        return self._env_name

    @property
    def task(self):

        return self._task

    @property
    def results(self):

        return self._results

    @property
    def role(self):

        return self._role

    @property
    def tasklist(self):

        return self._tasklist

    @property
    def item(self):

        return self._item

    @property
    def debug_data(self):

        return self._debug_data

    @property
    def action(self):

        if not self._task:
            return None

        return self._task.get("action", None)

    @property
    def msg(self):

        if not self._task:
            return None

        msg = self._task.get("name", None)
        if msg is None:
            msg = self.action
        if msg.startswith("[") and msg.endswith("]"):
            return msg[1:-1]
        else:
            return msg

    @property
    def stdout(self):

        if self._processed_stdout_stderr:
            return self._stdout

        else:
            self._stdout, self._stderr = self.calculate_stdout_stderr()
            return self._stdout

    @property
    def stderr(self):

        if self._processed_stdout_stderr:
            return self._stderr

        else:
            self._stdout, self._stderr = self.calculate_stdout_stderr()
            return self._stderr

    @property
    def detail_level(self):

        if not self._task:
            return 0

        msg = self._task.get("name", None)
        if not msg:
            return 0

        if msg.startswith("[") and msg.endswith("]"):
            return 1
        else:
            return 0

    def __repr__(self):

        d = {
            "category": self.category,
            "env_id": self.env_id,
            "env_name": self.env_name,
        }

        if self.task:
            d["task_id"] = (self.task.get("id"),)
            d["task_name"] = self.task.get("name")

        return readable(d, out="pformat")

    def is_same_task(self, other):

        if not self.task and other.task:
            return False
        if self.task and not other.task:
            return False

        self_list = [self.env_id, self.env_name, self.detail_level]
        other_list = [other.env_id, other.env_name, other.detail_level]

        if self.task:
            self_list.insert(0, self.task["id"])
            self_list.insert(1, self.task["name"])
            other_list.insert(0, other.task["id"])
            other_list.insert(1, other.task["name"])

        # print(self_list)
        # print(other_list)
        return self_list == other_list

    def calculate_stdout_stderr(self):

        if not self.results:
            return "", ""

        # changed = results.get("changed", None)
        stderr_lines = self.results.get("stderr_lines", [])
        stdout_lines = self.results.get("stdout_lines", [])
        module_stdout = self.results.get("module_stdout", "")
        module_stderr = self.results.get("module_stderr", "")
        # ansible_facts = results.get("ansible_facts", {})
        skip_reason = self.results.get("skip_reason", None)
        reason = self.results.get("reason", None)
        result_msg = self.results.get("msg", None)

        msg = None
        err = None
        if result_msg is not None:
            msg = "{}\n".format(result_msg)
        else:
            msg = None

        # TODO: change order, don't do unnecessary work, good enough for now

        if skip_reason:
            if msg is None:
                msg = ""
            for line in skip_reason.strip().split("\n"):
                msg += "{}\n".format(line)

        if module_stdout:
            module_stdout = module_stdout.split("\n")
            if len(module_stdout) == 1:
                msg = "stdout: {}\n".format(module_stdout[0])
            else:
                msg = "stdout:\n"
                for line in module_stdout:
                    msg += "  {}\n".format(line)

        if module_stderr:
            module_stderr = module_stderr.split("\n")
            if len(module_stderr) == 1:
                err = "stderr: {}\n".format(module_stderr[0])
            else:
                err = "stderr:\n"
                for line in module_stderr:
                    err += "  {}\n".format(line)

        if stdout_lines:
            if len(stdout_lines) == 1:
                msg = "stdout: {}\n".format(stdout_lines[0])
            else:
                msg = "stdout:\n"
                for line in stdout_lines:
                    msg += "  {}\n".format(line)

        if stderr_lines:
            if len(stderr_lines) == 1:
                err = "stderr: {}\n".format(stderr_lines[0])
            else:
                err = "stderr:\n"
                for line in stderr_lines:
                    err += "  {}\n".format(line)

        if reason is not None:
            if msg is None:
                msg = ""
            if len(reason.split("\n")) == 1:
                msg += "reason: {}\n".format(reason)
            else:
                msg += "reason:\n"
                for line in reason.split("\n"):
                    msg += "  {}\n".format(line)

        if msg is None:
            msg = ""
        if err is None:
            err = ""
        return msg.strip(), err.strip()


class NsblPrintCallbackAdapter(object):
    def __init__(self, root_task):

        self.root_task = root_task
        self.current_task = root_task

        self.current_nsbl_task = None
        self.current_tasklist = None
        self.current_role = None

        self.play_task = None
        self.env_task = None
        self.current_env_name = None

        self.last_error_msg = []
        self.replace_strings = True
        self.replacment_strings = {}

        # self.prepare_started = False
        # self.prepare_finished = False

    def set_environment_parameters(self, parameters):

        # print("ENVIRONMENT")
        # import pp
        # pp(parameters)
        self.environment_parameters = parameters

    def add_error_message(self, line):

        click.echo(line.strip())

    def add_log_message(self, line):

        try:
            if not line:
                return

            if line.strip():
                if self.replace_strings:

                    for key, value in self.replacment_strings.items():
                        line = line.replace(key, value)

                details_raw = json.loads(line)
            else:
                return
        except (Exception, ValueError) as e:
            if not line:
                return
            self.last_error_msg.append(line.rstrip())
            log.debug(e, exc_info=1)
            log.debug("Line: {}".format(line))
            return

        if self.last_error_msg:
            msg = " ".join(self.last_error_msg)
            print("SYSTEM MSG: {}".format(msg))
            # self.output_callback.add_system_message(msg)
            self.last_error_msg = []

        category = details_raw["category"]
        task = details_raw[FRECKLET_KEY_NAME]

        env_name = details_raw["env_name"]
        env_id = details_raw["env_id"]

        item = details_raw["item"]
        debug_data = details_raw["debug_data"]
        results = details_raw["results"]

        if task is not None:
            tasklist_path = task["task_path"]
            role_params = task.get("role_params", None)
        else:
            tasklist_path = None
            role_params = None

        self.current_tasklist = tasklist_path
        self.current_role = role_params

        # print("----")
        details = NsblTaskDetail(
            env_id=env_id,
            env_name=env_name,
            category=category,
            task=task,
            results=results,
            item=item,
            debug_data=debug_data,
            role=role_params,
            tasklist=tasklist_path,
        )

        if category == "play_start":
            if self.play_task is not None:
                return
            self.current_task = self.root_task.add_subtask(
                task_name="playbook", msg="starting Ansible run", category="playbook"
            )
            self.play_task = self.current_task
            return

        if not task:
            return

        if category.startswith("item"):
            if category in ["item_ok", "item_skipped", "item_failed"]:
                self.task_started(details)
                self.task_finished(details)
            else:
                raise Exception("CATEGORY: {}".format(category))
        elif category == "task_start":
            if details.action in ["include_tasks", "include_role"]:
                #     we are not interested in that, as the next item will be 'ok', so we use that to start a new task level
                return
            self.task_started(details)
        else:
            if details.action in ["include_tasks", "include_role"]:
                if category in ["failed", "unreachable"]:

                    self.task_started(details)
                    self.task_finished(details)
                    return

                return

            if self.current_task is None:
                # probably a handler
                log.debug("No task started for details: {}".format(details))
            else:
                self.task_finished(details)

    def task_started(self, details):

        if details.category.startswith("item"):
            name = self.pretty_print_item(details.item)
            msg = name
            base_task = self.current_task
        else:
            name = details.action
            msg = self.pretty_print_item(details.msg)
            base_task = self.play_task

        ignore_errors = details.task.get("ignore_errors", None)
        if ignore_errors is not True:
            ignore_errors = False

        self.current_task = base_task.add_subtask(
            task_name=name,
            msg=msg,
            category=details.category,
            reference=details.task.get("task_id"),
            detail_level=details.detail_level,
            ignore_errors=ignore_errors,
        )

        if not details.category.startswith("item"):
            self.current_nsbl_task = details

    def task_finished(self, details):

        # TODO: check if that is ok
        if not self.current_nsbl_task:
            self.current_nsbl_task = details
        if not details.is_same_task(self.current_nsbl_task):
            raise Exception("Task not started yet")

        if (
            details.category == "ok"
            or details.category == "skipped"
            or details.category == "item_ok"
            or details.category == "item_skipped"
        ):
            success = True
        else:
            success = False

        changed = details.results.get("changed", None)
        skip_reason = details.results.get("skip_reason", None)
        if skip_reason:
            skipped = True
        else:
            skipped = False

        msg = None
        error_msg = None
        if success and details.task.get("action", None) == "debug":
            if details.debug_data:
                debug_msg = readable(details.debug_data, out="yaml")
                self.current_task.add_result_msg(debug_msg, detail_level=0)
                changed = True
        else:
            if details.stdout:
                msg = details.stdout
            if details.stderr:
                error_msg = details.stderr

        if self.current_task is None:
            # TODO: this  is typically a handler, but need to investigate
            import pp

            print("NO CURRENT TASK")
            pp(details)
            pass
        else:
            self.current_task = self.current_task.finish(
                success=success,
                changed=changed,
                skipped=skipped,
                msg=msg,
                error_msg=error_msg,
            )

        if not details.category.startswith("item"):
            self.current_nsbl_task = None

    def write(self, line):

        if line.strip():
            # self.current_lines.append(line)
            self.add_log_message(line)

    def flush(self):

        print("FLUSH")

        pass

    def finish_up(self):

        # if self.play_task:
        #
        #     if not self.play_task.finished:
        #         self.play_task.finish()

        if self.last_error_msg:
            self.root_task.add_result_error(self.last_error_msg)

            self.root_task.finish(success=False)
        #
        # else:
        #     if not self.root_task.finished:
        #         self.root_task.finish(success=True)

        # self.root_task.finish(success=False)
        # else:
        #     self.root_task.finish(success=True)

    def pretty_print_item(self, item):

        if isinstance(item, string_types):
            try:
                item = json.loads(item)
            except (Exception):
                return item

        if isinstance(item, dict):
            name = item
            if item.get("name", None):
                name = item["name"]
            elif item.get("repo", None):
                name = item["repo"]
            elif item.get("vars", {}).get("name", None):
                name = item["vars"]["name"]
            elif item.get("vars", {}).get("repo", None):
                name = item["vars"]["name"]
            elif item.get("url", None) and item.get("path", None):
                name = "{} -> {}".format(item["url"], item["path"])
            elif item.get("stow_folder_name", None):
                name = item["stow_folder_name"]
            elif item.get("key", None):
                name = item["key"]

            if item.get("pkg_mgr", None):
                name = "{} (using '{}')".format(name, item["pkg_mgr"])
            return str(name)

        elif isinstance(item, Sequence):
            items = []
            for i in item:
                t = self.pretty_print_item(i)
                items.append(t)

            return ", ".join(items)

        if not isinstance(item, string_types):
            item = str(item)
        return item


#
# class NsblFrecklesCallbackAdapter(object):
#     """This is a much bigger shit-show than I'd like it to be.
#
#     It seems to be nearly impossible to get any kind of structured, hierarchical
#     task order out of an ansible callback.
#     """
#
#     def __init__(self, nsbl, parent_task, result_callback=None):
#
#         self.nsbl = nsbl
#         # self.output_callback = output_callback
#         self.result_callback = result_callback
#
#         self.replace_strings = True
#         self.replacment_strings = {}
#
#         self.last_error_msg = []
#
#         self.current_env = None
#         self.current_env_id = None
#
#         self.parent_task = parent_task
#         self.latest_task = parent_task
#         self.current_task_id = None
#         self.current_play = None
#         self.current_play_base_path = None
#         self.latest_task_path = None
#         self.latest_task_path_full = None
#         self.latest_task_id = None
#         self.current_role_task = None
#         self.role_started = False
#         self.current_tasklist_task = None
#         self.tasklist_started = False
#         self.tasks_archive = []
#         self.path_stack = []
#         self.new_task = False
#         self.new_tasklist = False
#         self.tasklist_finished = False
#         self.tasklist_open = False
#
#         self.playlist_started = False
#         self.still_preparing = None
#
#     def set_environment_parameters(self, parameters):
#
#         self.environment_parameters = parameters
#
#         env_dir = parameters.get("env_dir", None)
#         if env_dir is not None:
#             self.replacment_strings[env_dir] = "<< run_dir >>"
#
#     def add_error_message(self, line):
#         click.echo(line.strip())
#
#     def calculate_msg(self, results):
#
#         # changed = results.get("changed", None)
#         stderr_lines = results.get("stderr_lines", [])
#         stdout_lines = results.get("stdout_lines", [])
#         module_stdout = results.get("module_stdout", "")
#         module_stderr = results.get("module_stderr", "")
#         # ansible_facts = results.get("ansible_facts", {})
#         skip_reason = results.get("skip_reason", None)
#         reason = results.get("reason", None)
#         result_msg = results.get("msg", None)
#         msg = None
#         if result_msg is not None:
#             msg = "{}\n".format(result_msg)
#
#         else:
#             msg = None
#
#         if skip_reason:
#             if msg is None:
#                 msg = ""
#             for line in skip_reason.strip().split("\n"):
#                 msg += "{}\n".format(line)
#
#         if module_stdout and module_stderr:
#             if msg is None:
#                 msg = ""
#             module_stdout = module_stdout.split("\n")
#             if len(module_stdout) == 1:
#                 msg += "stdout: {}\n".format(module_stdout[0])
#             else:
#                 msg += "stdout:\n"
#                 for line in module_stdout:
#                     msg += "  {}\n".format(line)
#             module_stderr = module_stderr.split("\n")
#             if len(module_stderr) == 1:
#                 msg += "stderr: {}\n".format(module_stderr[0])
#             else:
#                 msg += "stderr:\n"
#                 for line in module_stderr:
#                     msg += "  {}\n".format(line)
#         elif module_stdout:
#             module_stdout = module_stdout.split("\n")
#             if len(module_stdout) == 1:
#                 msg = "stdout: {}\n".format(module_stdout[0])
#             else:
#                 msg = "stdout:\n"
#                 for line in module_stdout:
#                     msg += "  {}\n".format(line)
#         elif module_stderr:
#             module_stderr = module_stderr.split("\n")
#             if len(module_stderr) == 1:
#                 msg = "stderr: {}\n".format(module_stderr[0])
#             else:
#                 msg = "stderr:\n"
#                 for line in module_stderr:
#                     msg += "  {}\n".format(line)
#
#         if stdout_lines and stderr_lines:
#             if msg is None:
#                 msg = ""
#             if len(stdout_lines) == 1:
#                 msg += "stdout: {}\n".format(stdout_lines[0])
#             else:
#                 msg += "stdout:\n"
#                 for line in stdout_lines:
#                     msg += "  {}\n".format(line)
#             if len(stderr_lines) == 1:
#                 msg += "stderr: {}\n".format(stderr_lines[0])
#             else:
#                 msg += "stderr:\n"
#                 for line in stderr_lines:
#                     msg += "  {}\n".format(line)
#         elif stdout_lines:
#             if len(stdout_lines) == 1:
#                 msg = "stdout: {}\n".format(stdout_lines[0])
#             else:
#                 msg = "stdout:\n"
#                 for line in stdout_lines:
#                     msg += "  {}\n".format(line)
#         elif stderr_lines:
#             if len(stderr_lines) == 1:
#                 msg = "stderr: {}\n".format(stderr_lines[0])
#             else:
#                 msg = "stderr:\n"
#                 for line in stderr_lines:
#                     msg += "  {}\n".format(line)
#
#         if reason is not None:
#             if msg is None:
#                 msg = ""
#             if len(reason.split("\n")) == 1:
#                 msg += "reason: {}\n".format(reason)
#             else:
#                 msg += "reason:\n"
#                 for line in reason.split("\n"):
#                     msg += "  {}\n".format(line)
#
#         if msg is None:
#             msg = ""
#         return msg.strip()
#
#     def pretty_print_item(self, item):
#
#         if isinstance(item, string_types):
#             try:
#                 item = json.loads(item)
#             except (Exception):
#                 return item
#
#         if isinstance(item, dict):
#             name = item
#             if item.get("name", None):
#                 name = item["name"]
#             elif item.get("repo", None):
#                 name = item["repo"]
#             elif item.get("vars", {}).get("name", None):
#                 name = item["vars"]["name"]
#             elif item.get("vars", {}).get("repo", None):
#                 name = item["vars"]["name"]
#             elif item.get("url", None) and item.get("path", None):
#                 name = "{} -> {}".format(item["url"], item["path"])
#             elif item.get("stow_folder_name", None):
#                 name = item["stow_folder_name"]
#             elif item.get("key", None):
#                 name = item["key"]
#
#             if item.get("pkg_mgr", None):
#                 name = "{} (using '{}')".format(name, item["pkg_mgr"])
#             return name
#
#         return item
#
#     def finish_up(self):
#
#         if self.last_error_msg:
#             # known bug in Python, ignore...
#             if (
#                 "Exception ignored in: <function WeakValueDictionary.__init__."
#                 in "\n".join(self.last_error_msg)
#             ):
#                 log.debug("Suppressing error msg:")
#                 log.debug("\n".join(self.last_error_msg))
#                 return
#             raise Exception("\n".join(self.last_error_msg))
#
#     def add_log_message(self, line):
#
#         try:
#             if not line:
#                 return
#
#             # print("XXX")
#             # print(type(line))
#             # print(line)
#             # line = line.decode("utf-8")
#             # print(type(line))
#             # print(line)
#             if line.strip():
#                 # if line.startswith("RUNNIN")
#                 if self.replace_strings:
#
#                     for key, value in self.replacment_strings.items():
#                         line = line.replace(key, value)
#                         # print("XXX")
#                         # print(line)
#                 details = json.loads(line)
#             else:
#                 return
#         except (Exception, ValueError) as e:
#             if not line:
#                 return
#             self.last_error_msg.append(line.rstrip())
#             log.debug(e, exc_info=1)
#             log.debug("Line: {}".format(line))
#             return
#
#         if self.last_error_msg:
#             msg = " ".join(self.last_error_msg)
#             print("SYSTEM MSG: {}".format(msg))
#             # self.output_callback.add_system_message(msg)
#             self.last_error_msg = []
#
#         category = details["category"]
#         task = details[FRECKLET_KEY_NAME]
#
#         env_name = details["env_name"]
#         env_id = details["env_id"]
#
#         if env_id != self.current_env_id:
#
#             if self.current_env is not None:
#                 self.current_env.finish()
#             log.debug("New env: {}".format(env_name))
#             # self.current_tasklist = self.nsbl.get_tasklist(env_name, env_id)
#             self.current_env_id = env_id
#             self.current_env = self.parent_task.add_subtask(
#                 task_name=env_name,
#                 msg="host: {}".format(env_name),
#                 category="ansible-env",
#             )
#             self.latest_task = self.current_env
#
#         # env_details = {"id": env_id, "name": env_name}
#
#         item = details["item"]
#         debug_data = details["debug_data"]
#         results = details["results"]
#
#         if category == "play_start":
#
#             # td = TaskDetail(
#             #     task_name="play",
#             #     task_title="starting playbook",
#             #     task_type="ansible-play",
#             #     task_parent=self.current_env,
#             # )
#             self.current_play = self.current_env.add_subtask(
#                 task_name="play", msg="running Ansible", category="ansible-play"
#             )
#             self.latest_task = self.current_play
#             return
#         elif category == "play_end":
#             self.current_play.finish()
#             self.current_play = None
#             self.latest_task = self.current_env
#             self.current_play_base_path = None
#             return
#
#         parent = task.pop("parent", None)
#         action = task.get("action", None)
#
#         task_name = task.get("name", None)
#         if not task_name and action:
#             task_name = action
#
#         if action == "frecklet_result" and category in ["ok", "item_ok"]:
#             result_data = results["frecklet_result"]
#             if self.result_callback is not None:
#                 self.result_callback.add_result(result_data)
#             result_data = {"result": result_data}
#         else:
#             result_data = {}
#
#         if (
#             task_name is not None
#             and task_name.startswith("[")
#             and task_name.endswith("]")
#         ):
#             task_name = task_name[1:-1]
#             task_is_detail = True
#             task["command"] = task_name
#         else:
#             task_is_detail = False
#
#         if task_is_detail:
#             detail_level = 2
#         else:
#             detail_level = 0
#
#         ignore_errors = task.get("ignore_errors", None)
#
#         role_params = task.get("role_params", {})
#         task_id = task.get("id", None)
#
#         # we consider the freckles preparation tasks as one task
#         if task_id is None or task_id < 0 and not self.playlist_started:
#             # means we are still preparing the run
#             if self.still_preparing is None:
#                 self.still_preparing = True
#                 self.latest_task = self.current_play.add_subtask(
#                     task_name="init-target",
#                     msg="doing freckly init stuff, may take a while",
#                     category="ansible-task",
#                 )
#                 self.current_task_id = task_id
#                 return
#             else:
#                 if category in ["failed", "item_failed", "unreachable"]:
#                     if not ignore_errors:
#                         msg = self.calculate_msg(results=results)
#                         self.latest_task.finish(success=False, error_msg=msg)
#                 return
#
#         if not self.playlist_started:
#             self.playlist_started = True
#             self.latest_task.finish(success=True, skipped=False)
#             self.latest_task = self.current_play
#
#         # current_path_full = task["task_path"]
#         current_path = task["task_path"].rsplit(":", 1)[0]
#         if "handlers" in current_path:
#             # otherwise everything gets messed up
#             return
#         if self.current_play_base_path is None:
#             self.current_play_base_path = current_path
#
#         if self.latest_task_id is None:
#             self.latest_task_id = task_id
#
#         if self.latest_task_id != task_id and task_id >= 0:
#             self.latest_task_id = task_id
#
#         # if parent is None and self.latest_task != self.current_play:
#         #     start = self.latest_task
#         #     while start != self.current_play:
#         #         self.output_callback.task_finished(self.latest_task)
#         #         self.latest_task = self.latest_task.task_parent
#
#         if category == "task_start":
#
#             if parent:
#                 # no idea why that is necessary
#                 p1 = parent.get("task_path", None)
#                 if p1 is None:
#                     p = parent.get("parent", None)
#                     if p is not None:
#                         p1 = p.get("task_path", None)
#
#                 p2 = self.latest_task.data.get("task_path", None)
#
#                 if p1 != p2:
#
#                     if self.latest_task is None:
#                         self.latest_task = self.current_env
#
#                     start = self.latest_task
#                     match = False
#
#                     if start != self.current_env:
#
#                         while start.parent != self.current_env:
#
#                             if start.data.get("task_path") == p1:
#                                 match = True
#                                 break
#                             start = start.parent
#                             if start is None:
#                                 start = self.current_env
#                                 break
#
#                     if match:
#                         # TODO: add 'skipped' status where appropriate
#                         while start.task_details.get("task_path", None) != p1:
#                             start = self.latest_task.finish()
#                             self.tasks_archive = self.tasks_archive[0:-1]
#
#                     self.latest_task = start
#
#             if action in ["include_role", "include_tasks"]:
#                 # we are only interested in the 'ok' or skipped status
#                 return
#
#             self.latest_task = self.latest_task.add_subtask(
#                 task_name=task_name,
#                 msg=task_name,
#                 category="ansible-task",
#                 ignore_errors=ignore_errors,
#                 detail_level=detail_level,
#                 reference=self.latest_task_id,
#                 data={"task_path": current_path, "action": action},
#             )
#
#         elif category in ["ok", "failed", "skipped", "unreachable"]:
#
#             if action in ["include_role", "include_tasks"]:
#
#                 if action == "include_role":
#                     t = "ansible-role"
#                 else:
#                     t = "ansible-tasklist"
#
#                 self.latest_task = self.latest_task.add_subtask(
#                     task_name=task_name,
#                     msg=task_name,
#                     category=t,
#                     detail_level=detail_level,
#                     reference=self.latest_task_id,
#                     ignore_errors=task["ignore_errors"],
#                     data={"task_path": task["task_path"]},
#                 )
#                 if category == "ok":
#                     self.tasks_archive.append(task["task_path"])
#                 elif category in ["unreachable", "failed"]:
#                     msg = self.calculate_msg(results=results)
#                     self.latest_task = self.latest_task.finish(success=False, msg=msg)
#
#             else:
#
#                 msg = self.calculate_msg(results=results)
#                 td = self.latest_task
#                 if category == "ok":
#
#                     skip_reason = results.get("skip_reason", None)
#                     if skip_reason:
#                         skipped = True
#                     else:
#                         skipped = False
#
#                     changed = results.get("changed", None)
#
#                     if debug_data:
#                         result_data = dict_merge(
#                             {"debug": debug_data}, result_data, copy_dct=True
#                         )
#                         changed = True
#
#                     td.finish(
#                         success=True,
#                         msg=msg,
#                         changed=changed,
#                         skipped=skipped,
#                         result=result_data,
#                     )
#                     if self.latest_task.parent is not None:
#                         self.latest_task = self.latest_task.parent
#                     return
#                 elif category in ["failed", "unreachable"]:
#                     self.latest_task = td.finish(success=False, error_msg=msg)
#                     return
#                 elif category == "skipped":
#                     self.latest_task = td.finish(success=True, skipped=True)
#
#                 return
#
#         elif category in ["item_ok", "item_skipped", "item_failed"]:
#
#             item_title = self.pretty_print_item(item)
#
#             td = self.latest_task
#
#             msg = self.calculate_msg(results=results)
#
#             if category == "item_ok":
#
#                 if debug_data:
#                     result_data = dict_merge(
#                         {"debug": result_data}, result_data, copy_dct=True
#                     )
#
#                 changed = results.get("changed", None)
#                 temp = self.latest_task.add_subtask(
#                     task_name=item,
#                     msg=item_title,
#                     category="ansible-task-item",
#                     ignore_errors=ignore_errors,
#                     detail_level=detail_level,
#                     reference=task_id,
#                 )
#                 temp.finish(
#                     success=True,
#                     changed=changed,
#                     skipped=False,
#                     msg=msg,
#                     result=result_data,
#                 )
#             elif category == "item_skipped":
#                 temp = self.latest_task.add_subtask(
#                     task_name=item,
#                     category="ansible-task-item",
#                     ignore_errors=ignore_errors,
#                     detail_level=detail_level,
#                     msg=item_title,
#                     data={"action": action},
#                     action=action,
#                     reference=task_id,
#                 )
#                 temp.finish(success=True, skipped=True, msg=msg)
#
#             elif category == "item_failed":
#                 temp = self.latest_task.add_subtask(
#                     task_name=item,
#                     category="ansible-task-item",
#                     ignore_errors=ignore_errors,
#                     detail_level=detail_level,
#                     msg=item_title,
#                     data={"action": action},
#                     reference=task_id,
#                 )
#                 temp.finish(success=False, skipped=False, error_msg=msg)
#
#             return
#
#         else:
#
#             import pp
#
#             print(category)
#             pp(task)
#             pp(task["task_path"])
#             pp(role_params)
#             print("-----------------------")
#
#     def new_task(self, new_task_id):
#
#         # print("NEW TASK")
#         # print("OLD TASK: {}".format(self.current_task_id))
#         # print("NEW_TASK: {}".format(new_task_id))
#         self.current_task_id = new_task_id
