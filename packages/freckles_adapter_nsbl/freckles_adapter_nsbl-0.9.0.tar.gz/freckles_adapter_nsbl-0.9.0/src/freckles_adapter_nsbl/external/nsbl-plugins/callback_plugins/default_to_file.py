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

from __future__ import absolute_import, division, print_function

import io
import os

from ansible.plugins.callback.default import CallbackModule as CallbackModule_default
from ansible.utils.display import Display

__metaclass__ = type


class FileWriter(Display):
    def __init__(self, log_file, verbosity=4):
        self.log_file = log_file
        super(FileWriter, self).__init__(verbosity)

    def display(self, msg, color=None, stderr=False, screen_only=False, log_only=False):
        """ Display a message to the user
        Note: msg *must* be a unicode string to prevent UnicodeError tracebacks.
        """

        try:
            # msg2 = msg.lstrip(u"\n")

            # msg2 = to_bytes(msg2)

            # We first convert to a byte string so that we get rid of
            # characters that are invalid in the user's locale
            # msg2 = to_text(msg2, self._output_encoding(stderr=stderr))

            # print(msg2, file=self.log_file)
            # with io.open(self.log_file, "ab+", encoding="utf-8") as fd:
            with io.open(self.log_file, "a", encoding="utf-8") as fd:
                m = "n/a"
                try:
                    m = u"{}\n".format(msg)
                    # if hasattr(m, "encode"):
                    #     m = m.encode('utf-8')
                except (Exception) as e:
                    m = str(e)
                fd.write(m)
        except:
            pass


class CallbackModule(
    CallbackModule_default
):  # pylint: disable=too-few-public-methods,no-init
    """
    Override for the default callback module.
    Render std err/out outside of the rest of the result which it prints with
    indentation.
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "notification"
    CALLBACK_NAME = "default_to_file"

    def __init__(self):
        self._play = None
        self._last_task_banner = None
        super(CallbackModule, self).__init__()

        log_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "..",
            "logs",
            "ansible_run_log",
        )

        self._display = FileWriter(log_file)
