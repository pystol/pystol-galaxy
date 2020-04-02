# Log role

Used to foce update a custom resource,
for example in the case of a failure.

```
ansible -m include_role \
        -a 'name=pystol.actions.log' \
        -e '{'pystol_action_id': 'pystol-action-test-34yt9',
             'pystol_log_workflow_state': 'PystolOperatorEnded',
             'pystol_log_action_state': 'PystolActionEndedFail',
             'pystol_log_action_stdout': 'This action did not finish correctly',
             'pystol_log_action_stderr': 'An error ocurred when executing the action, check the names',
             'ansible_python_interpreter': '/usr/bin/python3'}' \
        localhost \
        -vvvvv
```
