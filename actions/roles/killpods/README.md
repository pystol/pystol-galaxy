# KillPods role

Run with:

This action needs 3 required parameters.

* pystol_killpods_namespace: The namespace for killig the pods
* pystol_killpods_distribution: The probabilistic distribution to create the histogram
* pystol_killpods_amount: The total amount of pods to kill

## Execute the Pystol action in the cluster using the operator


```
pystol run --namespace pystol \
           --collection actions \
           --role killpods \
           --extra-vars '{"pystol_killpods_namespace":"default","pystol_killpods_distribution":"poisson","pystol_killpods_amount":3}'

```

Or locally with, copying the `ansible -m ...` command from the
container execution info,
the containers running the actions are named as
**pystol-action-pystol-actions-actionname-d34de-2345r**.
Open the container details and execute the
arguments.

The actions execution should look like:

```
echo '---' > req.yml; \
echo 'collections:' >> req.yml; \
echo '- name: pystol.actions' >> req.yml;\
echo '  source: https://galaxy.ansible.com' >> req.yml; \
ansible-galaxy collection install --force -r req.yml; \
ansible -m include_role -a 'name=pystol.actions.killpods' -e '{'pystol_killpods_namespace': 'default', 'pystol_killpods_distribution': 'poisson', 'pystol_killpods_amount': '1', 'ansible_python_interpreter': '/usr/bin/python3', 'pystol_action_id': 'pystol-action-pystol-actions-killpods-nthkp'}' localhost -vv; exit 0
```

## Local testing of the KillPods action/role

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
ansible-playbook debug_role.yml \
        -e '{'pystol_killpods_namespace': 'default',
             'pystol_killpods_distribution': 'poisson',
             'pystol_killpods_amount': '1',
             'ansible_python_interpreter': '/usr/bin/python3'}' \
        -vvvvv
```

This way, you should be able to test locally
all the actions without the need of deploying them
in the Kubernetes cluster.
