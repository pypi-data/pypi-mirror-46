# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import sys
from collections import OrderedDict, Mapping

import click

# from . import __version__ as VERSION
from jinja2 import Environment, Template, FileSystemLoader
from ruamel.yaml.comments import CommentedMap

from frutils import dict_merge, JINJA_DELIMITER_PROFILES

TEMPLATE_METADATA_SCHEMA = {
    "exec": {"type": "boolean"},
    "pip_extra_url": {"type": "string"},
    "prefix_command": {"type": "string"},
    "template_init_function": {"type": "string"},
    "default_profile": {
        "type": "dict",
        "schema": {
            "profile_name": {"type": "string"},
            "profile_env_name": {"type": "string"},
            "conda_python_version": {"type": "string"},
            "conda_dependencies": {"type": "string"},
            "executables_to_link": {"type": "list", "schema": {"type": "string"}},
            "extra_executables": {"type": "list", "schema": {"type": "string"}},
            "debian_dependencies": {"type": "list", "schema": {"type": "string"}},
            "rpm_dependencies": {"type": "list", "schema": {"type": "string"}},
            "pip_dependencies": {"type": "list", "schema": {"type": "string"}},
        },
    },
}

FRECKLES_PROFILE_METADATA_PY2 = {
    "exec": False,
    "pip_extra_url": "https://pkgs.frkl.io/frkl/dev",
    "pip_pre_release": True,
    "prefix_command": None,
    "template_init_function": None,
    "no_exec": False,
    "default_profile": {
        "profile_name": "freckles",
        "profile_env_name": "freckles",
        "conda_python_version": "2.7",
        "virtualenv_python_version": "2.7",
        "executables_to_link": [
            "frecklecute",
            # "freckelize",
            # "freckfreckfreck",
            "freckles",
            # "freckles-manager",
            # "templig",
        ],
        "extra_executables": [
            "ansible",
            "ansible-playbook",
            "ansible-galaxy",
            "git",
            "curl",
            "wget",
        ],
        "conda_dependencies": ["git", "curl", "wget"],
        "debian_dependencies": [
            "curl",
            "wget",
            "build-essential",
            "git",
            "python-dev",
            "python-pip",
            "python-virtualenv",
            "virtualenv",
            "libssl-dev",
            "libffi-dev",
            "rsync",
            "sshpass",
        ],
        "rpm_dependencies": [
            "wget",
            "curl",
            "git",
            "python-pip",
            "python-virtualenv",
            "openssl-devel",
            "gcc",
            "libffi-devel",
            "python-devel",
            "rsync",
        ],
        "pip_dependencies": [
            "frutils",
            "frkl",
            "freckles",
            "freckles-adapter-nsbl[ansible]",
            "freckles-cli",
            # "freckles-manager",
            "tempting",
            "ting",
            "frkl-pkg",
        ],
    },
}

FRECKLES_PROFILE_METADATA_PY3 = {
    "exec": False,
    "pip_extra_url": "https://pkgs.frkl.io/frkl/dev",
    "pip_pre_release": True,
    "prefix_command": None,
    "template_init_function": None,
    "no_exec": False,
    "default_profile": {
        "profile_name": "freckles",
        "profile_env_name": "freckles",
        "conda_python_version": "3.6",
        "virtualenv_python_version": "3",
        "executables_to_link": [
            "frecklecute",
            # "freckelize",
            "freckles",
            # "freckles-manager",
            # "templig",
        ],
        "conda_dependencies": ["git", "curl", "wget", "pip"],
        "extra_executables": [
            "ansible",
            "ansible-playbook",
            "ansible-galaxy",
            "git",
            "curl",
            "wget",
        ],
        "debian_dependencies": [
            "curl",
            "wget",
            # "build-essential",
            "git",
            "python3-dev",
            # "python3-pip",
            "virtualenv",
            # "virtualenv",
            "libssl-dev",
            "libffi-dev",
            "rsync",
            "sshpass",
        ],
        "rpm_dependencies": [
            "wget",
            "curl",
            "git",
            # "python-pip",
            "python-virtualenv",
            "openssl-devel",
            "gcc",
            "libffi-devel",
            "python3-devel",
            "rsync",
            "sshpass",
        ],
        "pip_dependencies": [
            "frutils",
            "frkl",
            "freckles",
            "freckles-cli",
            "freckles-adapter-nsbl[ansible]",
            "frkl-pkg",
            "tempting",
            "ting",
        ],
    },
}

TEMPLATE_STRING = """
# =================================================================
# Inserted template string

DEFAULT_PROFILE="{{ metadata['default_profile']['profile_name'] }}"
# conda
DEFAULT_PROFILE_CONDA_PYTHON_VERSION="{{ metadata['default_profile']['conda_python_version'] }}"
DEFAULT_PROFILE_VIRTUALENV_PYTHON_VERSION="{{ metadata['default_profile']['virtualenv_python_version'] }}"
DEFAULT_PROFILE_CONDA_DEPENDENCIES="{{ metadata['default_profile']['conda_dependencies'] | join(' ') }}"
DEFAULT_PROFILE_EXECUTABLES_TO_LINK="{{ metadata['default_profile']['executables_to_link'] | join(' ') }}"
DEFAULT_PROFILE_EXTRA_EXECUTABLES="{{ metadata['default_profile']['extra_executables'] | join(' ') }}"
# deb
DEFAULT_PROFILE_DEB_DEPENDENCIES="{{ metadata['default_profile']['debian_dependencies'] | join(' ') }}"
# rpm
DEFAULT_PROFILE_RPM_DEPENDENCIES="{{ metadata['default_profile']['rpm_dependencies'] | join(' ') }}"
# pip requirements
DEFAULT_PROFILE_PIP_DEPENDENCIES="{{ metadata['default_profile']['pip_dependencies'] | join(' ') }}"
DEFAULT_PROFILE_ENV_NAME="{{ metadata['default_profile']['profile_name'] }}"
{% if metadata.get('pip_pre_release', False) %}

export PIP_PRE_RELEASE=true
{% endif %}
{% if metadata.get('pip_extra_url', False) %}

export PIP_EXTRA_INDEX_URL="{{ metadata['pip_extra_url'] }}"
{% endif %}{% if metadata.get('template_init_function', False) %}

{{ metadata['template_init_function'] }}
{% endif %}{% if metadata.get('prefix_command', False) %}

{{ metadata['prefix_command'] }}
{% endif %}{% if metadata.get('no_exec', False) == True %}

NO_EXEC=true{% endif %}

# End inserted template string
# =================================================================
"""


def generate_template_string(metadata=None):

    if metadata:
        if not isinstance(metadata, (dict, OrderedDict, CommentedMap)):
            click.echo("Invalid metadata: {}".format(metadata))
            sys.exit(1)

        metadata = dict_merge(FRECKLES_PROFILE_METADATA_PY3, metadata, copy_dct=True)
    else:
        metadata = FRECKLES_PROFILE_METADATA_PY3

    t = Template(TEMPLATE_STRING)
    rendered = t.render(metadata=metadata)

    return rendered


def render_inaugurate_script(additions):

    this_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(this_dir, "external", "scripts", "inaugurate")
    loader = FileSystemLoader(template_path)

    env = Environment(loader=loader, **JINJA_DELIMITER_PROFILES["shell"])
    template = env.get_template("inaugurate")

    rendered = template.render(TEMPLATE_MARKER=additions)

    return rendered


def generate_inaugurate_script(additional_metadata=None):
    """Generate a customized 'inaugurate' script.
    """

    if additional_metadata is None:
        additional_metadata = [{}]
    if isinstance(additional_metadata, Mapping):
        additional_metadata = [additional_metadata]

    merged_md = {}
    for md in additional_metadata:
        dict_merge(merged_md, md, copy_dct=False)

    rendered = generate_template_string(metadata=merged_md)

    script = render_inaugurate_script(rendered)

    return script
