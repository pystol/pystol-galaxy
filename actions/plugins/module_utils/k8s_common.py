import os
from kubernetes import config


def load_kubernetes_config():
    """
    Load the initial config details.
    We load the config depending where we execute the code from
    """
    try:
        if 'KUBERNETES_PORT' in os.environ:
            # We set up the client from within a k8s pod
            config.load_incluster_config()
        elif 'KUBECONFIG' in os.environ:
            config.load_kube_config(os.getenv('KUBECONFIG'))
        else:
            config.load_kube_config()
    except Exception as e:
        message = ("---\n"
                   "The Python Kubernetes client could not be configured "
                   "at this time.\n"
                   "You need a working Kubernetes deployment to make "
                   "Pystol work.\n"
                   "Check the following:\n"
                   "Use the env var KUBECONFIG with the path to your K8s "
                   "config file like:\n"
                   "    export KUBECONFIG=~/.kube/config\n"
                   "Or run Pystol from within the cluster to make use of "
                   "load_incluster_config.\n"
                   "Error: ")
        print(message)
        raise e
