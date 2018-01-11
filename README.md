## Ansible dynamic inventory for MySQL with Python Script - ansible-dynamic-inventory-mysql
Ansible dynamic inventory for MySQL with Python Script. Here I have created test dynamic inventory script with python to get data from MySQL and Ansible will use it as an inventory source as long as it returns a JSON structure with the --list option.

## Usage
Simply call the script like the following

```yml
ansible-playbook -i dynamic_inventory.py example_playbook.yml
# or
ansible -i dynamic_inventory.py group_name -m ping
```
## Author Informations

This python script was created by [Avinash Pawar](http://devopstechie.com).
