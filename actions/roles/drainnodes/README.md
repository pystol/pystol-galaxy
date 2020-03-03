# DrainNodes role

Run with:

This action needs 3 required parameters.

* pystol_drainnodes_amount: Number of nodes to be randomly drained
* pystol_drainnodes_names: A list of nodes to be drained

```
pystol run --namespace pystol \
           --collection actions \
           --role drainnodes \
           --extra-vars '{"pystol_drainnodes_amount":1,"pystol_drainnodes_names":["minikube", "node2"]}'

```

**pystol_drainnodes_names has prcedence over pystol_drainnodes_amount**

If pystol_drainnodes_names is defined, then pystol_drainnodes_amount is skipped.
