Wrapper for Ansible cli.
========================

Usage
=====

*  `pm-execute [ansible command name] [args]` - calls any ansible cli tool.
*  `pm-cli-reference [ansible command name,...] [--exclude key]` -
    output cli keys for command. Default - all. Exclude keys by names (support many).
    Now support output only 'ansible', 'ansible-playbook' and
    'ansible-galaxy'.
*  `pm-ansible [reference/ansible_command]` - run as module.
   For output reference use 'reference', or full ansible command.
*  `pm-ansible [--detail] [--get]` -
    Output modules reference. 

Contribution
============

We use `tox` for tests and deploy. Just run `tox -e py27-coverage,py36-coverage,flake`
for full tests with coverage output. It's small project and 
we strictly adhere to the full (__100%__) code coverage.
