#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018 Markus Binsteiner (@makkus) <makkus@frkl.io>
# Copyright: (c) 2013, Dag Wieers (@dagwieers) <dag@wieers.com>
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
module: set_platform_fact
short_description: Set facts depending on platform
description:
    - This module is built on-top the M(set_fact) module, and it enables setting of facts using a dictionary that uses platform-matcher strings as
      keys, and the platform-specific vars as values
    - This module checks platform strings from the most to least specific. Use the I(add_match_facts) option to print out platform strings for the
      system you are currently working on.
    - This module allows setting new variables.  Variables are set on a host-by-host basis just like facts discovered by the setup module.
    - These variables will be available to subsequent plays during an ansible-playbook run, but will not be saved across executions even if you use
      a fact cache.
    - Per the standard Ansible variable precedence rules, many other types of variables have a higher priority, so this value may be overridden.
      See U(http://docs.ansible.com/ansible/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable) for more information.
options:
  key_value:
    description:
      - The C(set_platform_fact) module takes key=platform_value_dict pairs as variables to set
        in the playbook scope.
      - In addition to platform string matchers, the keyword 'default' can be specified. This will be used in case no other match is found.
    default: null
  skip_non_matches:
    description:
      - Skip variables where no match is found, instead of erroring out.
    default: false
  ignore_case:
    description:
      - Whether to ignore case when matching platform strings.
    default: true
  add_match_facts:
    description:
      - Adds a '_platform_strings', and, if applicable, '_platform_match_*' variables to the returned facts.
      - This is useful mainly for debug purposes, but can be used on it's own (without actually adding any other facts).
    default: false
  cacheable:
    description:
      - This boolean indicates if the facts set will also be added to the
        fact cache, if fact caching is enabled.
    type: bool
    default: false
version_added: "2.6"


"""

EXAMPLES = """
# Example setting host facts using complex arguments
- set_platform_fact:
     one_fact:
       ubuntu-18.04: something
       ubuntu-bionic: something other
       ubuntu-18: something else again
       debian: true
       redhat: false
       default: 0

"""
