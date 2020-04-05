# DrainNodes role

This is a role to execute the action to drain the nodes.

Run with:

This action needs 3 required parameters.

* pystol_drainnodes_amount:
Number of nodes to be randomly drained.
* pystol_drainnodes_nodes:
A list of nodes to be drained.
* pystol_drainnodes_duration:
Duracion in seconds of the action execution.

```
pystol run --namespace pystol \
           --collection actions \
           --role drainnodes \
           --extra-vars '{"pystol_drainnodes_amount":1,"pystol_drainnodes_nodes":["minikube", "node2"],"pystol_drainnodes_duration":60}'

```

**pystol_drainnodes_nodes has precedence over pystol_drainnodes_amount**

If pystol_drainnodes_names is defined, then pystol_drainnodes_amount is skipped.
