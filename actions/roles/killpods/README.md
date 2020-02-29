# KillPods role

Run with:


```
pystol run --namespace pystol \
           --collection actions \
           --role killpods
```
 OR

```
ansible -m include_role -a 'name=killpods' -e 'ansible_python_interpreter=/usr/bin/python3' localhost -vvvv
```
