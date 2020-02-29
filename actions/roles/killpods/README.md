# KillPods role

Run with:


```
pystol run --namespace pystol \
           --collection actions \
           --role killpods \
           --extra-vars '{"pystol_killpods_namespace":"default","pystol_killpods_distribution":"poisson","pystol_killpods_amount":"10"}'

```
 OR

```
ansible -m include_role -a 'name=killpods' -e 'ansible_python_interpreter=/usr/bin/python3' localhost -vvvv
```
