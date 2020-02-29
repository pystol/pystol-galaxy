# KillPods role

Run with:

This action needs 3 required parameters.

* pystol_killpods_namespace: The namespace for killig the pods
* pystol_killpods_distribution: The probabilistic distribution to create the histogram
* pystol_killpods_amount: The total amount of pods to kill

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

Thy should looks like:

```
echo '---' > req.yml; \
echo 'collections:' >> req.yml; \
echo '- name: pystol.actions' >> req.yml;\
echo '  source: https://galaxy.ansible.com' >> req.yml; \
ansible-galaxy collection install --force -r req.yml; \
ansible -m include_role -a 'name=pystol.actions.killpods' -e '{'pystol_killpods_namespace': 'default', 'pystol_killpods_distribution': 'poisson', 'pystol_killpods_amount': '1', 'ansible_python_interpreter': '/usr/bin/python3', 'pystol_action_id': 'pystol-action-pystol-actions-killpods-nthkp'}' localhost -vv; exit 0
```
