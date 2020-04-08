#!/bin/bash

# Then execute
rm -rf actions/releases
mkdir -p actions/releases
cd actions
# Build and install the collection
ansible-galaxy collection build -v --force --output-path releases/
ansible-galaxy collection install --force releases/pystol-actions-`cat galaxy.yml | shyaml get-value version`.tar.gz
cd ~/.ansible/collections/ansible_collections/pystol/actions
ansible-test sanity --skip-test import
