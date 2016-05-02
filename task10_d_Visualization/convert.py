#!/usr/bin/python2
import json

with open('final_measurement_task_d.json','r') as fp:
	data=json.load(fp)


final_list=[]
for mime, mime_val in data.items():

	mime_obj = {}
	mime_obj["name"] = mime 
	mime_obj["children"] = []

	for measurement, measurement_val in mime_val.items():
		
		measurement_obj = {}
		measurement_obj["name"] = measurement
		measurement_obj["children"] = []

		for key, val in measurement_val.items():

			attr = {}
			attr["name"] = key + " : " + str(val)

			measurement_obj["children"].append(attr)
		
		mime_obj["children"].append(measurement_obj)

	final_list.append(mime_obj)

with open('converted.json','w') as fout:
	json.dump(final_list,fout,indent=4)
