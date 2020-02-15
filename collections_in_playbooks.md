```
- name: Run a module from inside a collection
  hosts: localhost
  tasks:
    - name: Gather some real Facts.
      pystol.actions.real_facts:
        name: John Snow
      register: testout
    - debug:
        msg: "{{ testout }}"
```
```
- name: Run a module from inside a collection using the collections keyword
  hosts: localhost
  collections:
    - pystol.actions
  tasks:
    - name: Gather some real Facts.
      real_facts:
        name: Jane Doe
      register: testout
    - debug:
        msg: "{{ testout }}"
```
```
- name: Run a role from inside of a collection
  hosts: localhost
  roles:
    - "pystol.actions.pingtest"
```
