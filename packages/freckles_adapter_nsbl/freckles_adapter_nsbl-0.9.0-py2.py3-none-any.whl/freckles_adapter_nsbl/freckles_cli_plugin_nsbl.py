# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import subprocess
import sys
import time
from collections import OrderedDict

import click
from ruamel.yaml import YAML

from freckles_adapter_nsbl.defaults import (
    NSBL_USER_ROLE_REPO,
    NSBL_DEFAULT_ROLE_REPO,
    NSBL_USER_TASKLIST_REPO,
    NSBL_DEFAULT_TASKLIST_REPO,
)
from frutils import reindent

yaml = YAML(typ="safe")


@click.group("nsbl")
@click.pass_context
def nsbl(ctx):
    """commands related to the 'nsbl' adapter"""

    # context = ctx.obj["context"]
    # control_dict = ctx.obj["control_dict"]
    #
    # # context.set_control_vars(control_vars=control_dict)


# @nsbl.command("list-role-repos")
# @click.pass_context
# def list_role_repos(ctx):
#     """Lists all available roles"""
#
#     context = ctx.obj["context"]
#     repo_manager = context.repo_manager
#
#     click.echo()
#
#     for r in repo_manager.get_repo_descs(only_content_types=["roles"]):
#
#         click.echo("{}".format(r["path"]), nl=False)
#         alias = r.get("alias", None)
#         if alias is not None and alias != r["path"]:
#             click.echo(" (from alias: {})".format(alias))
#         else:
#             click.echo()


@nsbl.command("log")
@click.option("--follow", "-f", help="follow the log file", is_flag=True, default=False)
@click.option(
    "--nsbl",
    "-n",
    help="use thensbl log file instead of the (more detailed) Ansible one",
    is_flag=True,
    default=False,
)
@click.pass_context
def last_log(ctx, follow, nsbl):
    """Prints out the last runs ansible log (verbose).

    The normal output of any 'freckles' command is short-form. Which helps see what's going on. This is not helpful when there is an issue or during development of roles, adapters, blueprints or frecklecutables.

    Instead of manually tailing that particular log-file, this commands lets you do that a tad quicker.
    """

    context = ctx.obj["context"]
    run_folder = os.path.expanduser(context.config_value(key="current_run_folder"))

    if not os.path.exists(run_folder):
        click.echo(
            "No current run folder exists (path: {}). Doing nothing.".format(run_folder)
        )
        sys.exit()

    last_run_folder = os.path.join(run_folder, "nsbl")

    last_run_log_folder = os.path.join(last_run_folder, "logs")
    if not os.path.exists(last_run_folder):
        click.echo(
            "No current Ansible run folder exists (path: {}). Doing nothing.".format(
                last_run_folder
            )
        )
        sys.exit()

    if nsbl:
        ansible_log_file = os.path.join(last_run_log_folder, "nsbl_run_log")
    else:
        ansible_log_file = os.path.join(last_run_log_folder, "ansible_run_log")

    if not os.path.exists(ansible_log_file):
        click.echo(
            "No current Ansible log file, doing nothing: {}".format(ansible_log_file)
        )
        sys.exit()

    if not follow:
        f = subprocess.Popen(["cat", ansible_log_file], shell=False)

    else:

        link_target = os.readlink(run_folder)

        f = None

        while True:

            if not os.path.exists(ansible_log_file):
                time.sleep(1)
                continue

            if not f:
                f = subprocess.Popen(["tail", "-F", ansible_log_file], shell=False)

            time.sleep(1)
            new_link_target = os.readlink(run_folder)
            if new_link_target != link_target:
                f.terminate()
                f = None
                link_target = new_link_target


@nsbl.command("info")
@click.option("--play/--no--play", help="display play info", default=False)
@click.option("--path/--no-path", help="display path info", default=False)
@click.option("--config/--no-config", help="display ansible.cfg content", default=False)
@click.option("--roles/--no-roles", help="display role(s) info", default=False)
@click.option(
    "--tasklists/--no-tasklists", help="display tasklists info", default=False
)
@click.option("--all", help="display all information", is_flag=True, default=False)
@click.pass_context
def info(ctx, play, path, config, roles, tasklists, all):
    """prints details of the last run"""

    # output_format = "yaml"

    if all:
        play = True
        path = True
        config = True
        roles = True
        tasklists = True

    if not play and not path and not config and not roles and not tasklists:
        path = True
        play = True

    click.echo()

    context = ctx.obj["context"]
    run_folder = os.path.expanduser(context.config_value(key="current_run_folder"))

    last_run_folder = os.path.join(run_folder, "nsbl")

    base_folder = os.path.realpath(last_run_folder)
    plays_folder = os.path.join(base_folder, "plays")
    # inventory_folder = os.path.join(base_folder, "inventory")
    roles_folder = os.path.join(base_folder, "roles")
    tasklists_folder = os.path.join(base_folder, "task_lists")
    # debug_folder = os.path.join(base_folder, "debug")

    if path:
        click.secho("path", bold=True)
        click.echo()
        click.echo("  base folder: {}".format(base_folder))
        # click.echo("  plays: {}".format(plays_folder))
        # click.echo("  inventory: {}".format(inventory_folder))
        # click.echo("  roles: {}".format(roles_folder))
        # click.echo("  tasklists: {}".format(tasklists_folder))
        # click.echo("  debug: {}".format(debug_folder))
        # click.echo("  run script: {}".format(os.path.join(base_folder, "run_all_plays.sh")))
        # click.echo("  debug script: {}".format(os.path.join(debug_folder, "debug_all_plays.sh")))
        click.echo()
    if play:
        click.secho("plays", bold=True)
        click.echo()
        plays = [x for x in os.listdir(plays_folder) if x.startswith("play_")]
        for p in plays:
            click.secho("  {}".format(p), bold=True)
            click.echo("  ")
            with open(os.path.join(plays_folder, p)) as f:
                content = f.read()
            click.echo(reindent(content, 4))
        click.echo()
    if config:
        click.secho("ansible.cfg", bold=True)
        click.echo()
        with open(os.path.join(plays_folder, "ansible.cfg")) as f:
            content = f.read()
        click.echo(reindent(content, 2))
        click.echo()
    if roles:
        click.secho("roles", bold=True)
        click.echo()
        internal = [
            x
            for x in os.listdir(os.path.join(roles_folder, "internal"))
            if os.path.isdir(os.path.join(roles_folder, "internal", x))
        ]
        external = [
            x
            for x in os.listdir(os.path.join(roles_folder, "external"))
            if os.path.isdir(os.path.join(roles_folder, "external", x))
        ]
        if internal:
            click.secho("  internal", bold=True)
            click.echo()
            for i in internal:
                click.echo("    - {}".format(i))
            click.echo()
        if external:
            click.secho("  external", bold=True)
            click.echo()
            for i in external:
                click.echo("    - {}".format(i))
            click.echo()
    if tasklists:
        click.secho("task lists", bold=True)
        click.echo()
        tasklists = [
            x
            for x in os.listdir(tasklists_folder)
            if os.path.isfile(os.path.join(tasklists_folder, x))
        ]
        if tasklists:
            for tl in tasklists:
                click.echo("    - {}".format(tl))
            click.echo()


@nsbl.command("list-roles")
# @click.option(
#     "--guess-args",
#     "-g",
#     help="guess role arguments from defaults file",
#     is_flag=True,
#     default=False,
#     required=False,
# )
# @click.option(
#     "--details",
#     "-d",
#     help="display role details",
#     is_flag=True,
#     default=False,
#     required=False,
# )
@click.pass_context
def list_roles(ctx):
    """Lists all available roles"""

    context = ctx.obj["context"]

    nsbl_context = context._adapters["nsbl"].nsbl_context

    roles_available = nsbl_context.available_roles

    click.echo()
    # if not details:
    #     for name, path in sorted(roles.items()):
    #         click.echo(name)
    #     sys.exit()

    all_role_repos = nsbl_context.role_repo_paths

    roles_per_repo = OrderedDict()
    for role_name, role_path in roles_available.items():
        repo_path = None

        for r in all_role_repos:
            if role_path.startswith(r):
                repo_path = r
                break

        if not repo_path:
            raise Exception("Could not find repo for role: {}".format(role_name))

        rel_path = os.path.relpath(role_path, repo_path)

        roles_per_repo.setdefault(repo_path, OrderedDict())[role_name] = rel_path

    for repo, roles in roles_per_repo.items():

        if not roles:
            continue

        click.secho("Repository: ", bold=True, nl=False)
        if repo.startswith(NSBL_USER_ROLE_REPO):
            repo_name = "user"
        elif repo.startswith(NSBL_DEFAULT_ROLE_REPO):
            repo_name = "default (internal)"
        else:
            repo_name = repo
        click.echo(repo_name)
        click.echo()
        for r in sorted(roles.keys()):
            p = roles[r]
            click.echo("  - {} ({})".format(r, p))

        click.echo()


@nsbl.command("list-tasklists")
# @click.option(
#     "--guess-args",
#     "-g",
#     help="guess role arguments from defaults file",
#     is_flag=True,
#     default=False,
#     required=False,
# )
# @click.option(
#     "--details",
#     "-d",
#     help="display role details",
#     is_flag=True,
#     default=False,
#     required=False,
# )
@click.pass_context
def list_tasklists(ctx):
    """Lists all available roles"""

    context = ctx.obj["context"]

    nsbl_context = context._adapters["nsbl"].nsbl_context

    tasklists_available = nsbl_context.available_tasklists

    click.echo()
    # if not details:
    #     for name, path in sorted(roles.items()):
    #         click.echo(name)
    #     sys.exit()

    tasklists_per_repo = OrderedDict()
    for tasklist_name in tasklists_available.keys():

        repo_path = nsbl_context.get_repo_for_tasklist(tasklist_name)

        if not repo_path:
            raise Exception(
                "Could not find repo for tasklist: {}".format(tasklist_name)
            )

        tasklists_per_repo.setdefault(repo_path, []).append(tasklist_name)

    for repo, tasklists in tasklists_per_repo.items():

        if not tasklists:
            continue

        click.secho("Repository: ", bold=True, nl=False)
        if repo.startswith(NSBL_USER_TASKLIST_REPO):
            repo_name = "user"
        elif repo.startswith(NSBL_DEFAULT_TASKLIST_REPO):
            repo_name = "default (internal)"
        else:
            repo_name = repo
        click.echo(repo_name)
        click.echo()
        for tl in sorted(tasklists):
            click.echo("  - {}".format(tl))

        click.echo()
