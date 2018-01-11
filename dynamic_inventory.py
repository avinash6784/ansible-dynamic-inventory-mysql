#!/usr/bin/env python

'''
Example custom dynamic inventory script for Ansible, in Python.
'''

import os
import sys
import argparse
import mysql.connector as mariadb
from collections import defaultdict

try:
    import json
except ImportError:
    import simplejson as json

class DynamicInventory(object):

    def __init__(self, args):
        self.inventory = {}
        self.args = args
        self.mariadb_connection = mariadb.connect(user='ansible', password='ansible', database='inventory')
        self.cursor = self.mariadb_connection.cursor(dictionary=True)
	self.os = []
	self.osgroup = []
	self.result = {}
        # Called with `--list`.
        if self.args.list:
            self.inventory = self.dynamic_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print json.dumps(self.inventory);

    # Example inventory for testing.
    def dynamic_inventory(self):
	self.cursor.execute("select h.name as hostname, h.os, g.name as groupname from hosts as h, groups as g where h.group_id = g.id")
        result_set = self.cursor.fetchall()
	
	# Normalize data based on db data.
	result_dict = lambda: defaultdict(result_dict) 
        results_group = result_dict()       
        results_os = result_dict()       
	for row in result_set:
	    results_group[row['groupname']][row['hostname']] = row['hostname']
	    results_os[row['os']][row['hostname']] = row['hostname']
	
	# For groupname wise/all groups
	all_hostlist = []
	for group in results_group:
	    group_hostlist = []	    
	    for host in results_group[group]:
		group_hostlist.append(host)
		all_hostlist.append(host)
	        self.result.update({group : group_hostlist})
        
	self.result.update({'all' : list(set(all_hostlist))})

	# For OS groups
	for os in results_os:
	    os_hostlist = []
            for host in results_os[os]:
		os_hostlist.append(host)
	        self.result.update({os : os_hostlist})

	return self.result
	
	
    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    def __del__(self):
	self.cursor.close()
	self.mariadb_connection.close()

# Main function
def main():
        # Read command line args
	parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        args = parser.parse_args()
	# Get the inventory.
	DynamicInventory(args)


if __name__ == '__main__':
	main()
