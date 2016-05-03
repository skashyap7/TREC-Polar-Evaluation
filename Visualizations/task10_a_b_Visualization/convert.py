#!/usr/bin/python2
import json

with open('final_measurement_list.json','r') as fp:
	data=json.load(fp)


final_list=[]
for k in data.keys():
	# For each unit create a new json
	temp_obj = {}
	temp_obj["name"] = k
	children = []
	for elem in data[k].keys():
		child_obj = {}
		child_obj["name"] = elem
		child_obj["children"] = []
		value = {}
		value["name"] = str(data[k][elem])
		child_obj["children"].append(value)
		children.append(child_obj)
	temp_obj["children"] = children
	final_list.append(temp_obj)


'''	
for key,value in data.items():
	par_child_dict={}
	par_child_dict["name"]=key
	child_dict={}
	values_list=[]
	for k,v in value.items():
		child_dict["name"]=k
		value_list=[]
		child_value_dict={}
		child_value_dict["name"]=str(v)
		value_list.append(child_value_dict)
		child_dict["children"]=value_list
		values_list.append(child_dict)
	par_child_dict["children"]=values_list
	final_list.append(par_child_dict)
'''
with open('converted.json','w') as fout:
	json.dump(final_list,fout,indent=4)