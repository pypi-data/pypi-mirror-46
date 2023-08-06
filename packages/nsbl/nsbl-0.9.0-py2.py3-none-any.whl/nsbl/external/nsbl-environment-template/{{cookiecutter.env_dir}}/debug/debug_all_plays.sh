#!/usr/bin/env bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -e "$HOME/.nix-profile/etc/profile.d/nix.sh" ]; then source "$HOME/.nix-profile/etc/profile.d/nix.sh"; fi

# additional bin paths
{% for path in cookiecutter.extra_paths.split(':') %}
if [ -d "{{ path }}" ]; then
    export PATH="{{ path }}:$PATH"
fi
{% endfor %}

cd {{cookiecutter.playbook_dir}}/../debug

{{cookiecutter.extra_script_commands}}

ANSIBLE_CONFIG=./ansible.cfg ansible-playbook -vvvv {{cookiecutter.ask_sudo}} ../plays/{{cookiecutter.playbook}}
