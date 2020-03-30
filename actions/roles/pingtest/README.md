# KillPods role

Run with:

There are no required params.

The source is optional, it depends on
the collection location.

If source is used, then we will invoque
the action from that repository.

```
pystol run --namespace pystol \
           --collection actions \
           --role pingtest \
           --source https://github.com/pystol/pystol-galaxy
```

Or locally with, copying the `ansible -m ...` command from the
container execution info,
the containers running the actions are named as
**pystol-action-pystol-actions-actionname-d34de-2345r**.
Open the container details and execute the
arguments.

## Local testing of the pingtest

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

# Go to the playbook folder
cd ~/pystol-galaxy/actions/roles/killpods/tasks/
# Execute the playbook
ansible -m include_role \
-a 'name=pystol.actions.pingtest' \
localhost -vv
```

This way, you should be able to test locally
all the actions without the need of deploying them
in the Kubernetes cluster.

