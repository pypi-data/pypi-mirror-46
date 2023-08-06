#!/usr/bin/python
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

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}


DOCUMENTATION = """
---
author: "Markus Binsteiner (@makkus)"
module: frecklet_result
short_description: Register key/value pairs as results to freckles
description:
    - This module/action plugin is really only useful in combination with freckles (https://freckles.io)
options:
  keys:
    description:
      - dict indicating the variable names to register, key: result key, value: ansible var or expression
    required: true
  default:
    description:
      - the default value if the key is not present, or empty
    required: false
  fail_if_empty:
    description:
      - fail if the value for the variable is empty
    default: false
    type: bool
version_added: "2.6"


"""

EXAMPLES = """
# Example setting host facts using complex arguments
- frecklet_result:
     keys:
       user: "{{ ansible_env.USER }}"

"""
