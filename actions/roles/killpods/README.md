# KillPods role

Run with:


```
pystol run --namespace pystol \
           --collection actions \
           --role killpods \
           --extra-vars '{"pystol_killpods_namespace":"default","pystol_killpods_distribution":"poisson","pystol_killpods_amount":"10"}'

```

Or locally with:

```
ansible -m include_role \
    -a 'name=pystol.actions.killpods' \
    -e '{"pystol_killpods_namespace": "default", \
         "pystol_killpods_distribution": "poisson", \
         "pystol_killpods_amount": "1", \
         "ansible_python_interpreter": "/usr/bin/python3", \
         "pystol_action_id": "pystol-action-pystol-actions-killpods-tlxtb"}' \
    localhost -vv
```
