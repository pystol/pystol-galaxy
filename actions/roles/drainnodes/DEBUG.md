## Local testing of the DrainNodes action/role

If you don't require to execute the action from the
cluster operator, for example for developing purposes,
you can follow the next steps.

Open a session in a terminal and execute:

```
journalctl -f
```

This will print the system's logs including the debug information from the
action.

In another session execute:

```
# Go to the home folder
cd
# Clone pystol-galaxy
git clone https://github.com/pystol/pystol-galaxy.git

# Do any change you need in the repository.

# Then execute
cd ~/pystol-galaxy/actions/
mkdir -p releases
# Build and install the collection
ansible-galaxy collection build -v --force --output-path releases/
cd releases
LATEST=$(ls pystol-actions*.tar.gz | grep -v latest | sort -V | tail -n1)
ln -sf $LATEST pystol-actions-latest.tar.gz
ansible-galaxy collection install --force pystol-actions-latest.tar.gz

# Go to the home folder
cd ~/pystol-galaxy/actions/

# Execute the playbook
ansible -m include_role \
        -a 'name=pystol.actions.drainnodes' \
        -e '{'pystol_drainnodes_amount': 1,
             'pystol_drainnodes_nodes': ["node_1","node_2"],
             'pystol_drainnodes_duration': 60,
             'ansible_python_interpreter': '/usr/bin/python3'}' \
        localhost \
        -vvvvv
```

This way, you should be able to test locally
all the actions without the need of deploying them
in the Kubernetes cluster.
