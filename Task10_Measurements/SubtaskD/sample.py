import urllib, json,re,os
import itertools
from collections import defaultdict
import traceback

#read 10000 rows at a time
min_dict={}
max_dict={}
count_dict=defaultdict(int)
mime_dict={}
final_dict={}
count=0

def get_solr_response():
	try:
		with open("sample.json","r") as out:				
			data = json.loads(out.read())
		calculate_stats(data)		
	except Exception, e:
		print "Solr: Failed at  %s" % e
		with open("min_measurement_list.json","w") as outFile:
			json.dump(min_dict,outFile,indent=4, sort_keys=True)
		outFile.close()
		with open("max_measurement_list.json","w") as outFile:
			json.dump(max_dict,outFile,indent=4, sort_keys=True)
		outFile.close()

def update_min_max(mime,unit,value):
	unit=unit.lower()
	if mime not in mime_dict:
		mime_dict[mime]={}
	else:
		if (unit in min_dict and min_dict[unit]>value) or unit not in min_dict:
			min_dict[unit]=value
			print min_dict[unit]
			mime_dict[mime]=min_dict[unit]
		if (unit in max_dict and max_dict[unit]<value) or unit not in max_dict:
			max_dict[unit]=value
			print min_dict[unit]
			mime_dict[mime]=max_dict[unit]
		count_dict[unit]+=1
		mime_dict[mime]=count_dict[unit]

#read response from solr
def calculate_stats(data):
	global count
	for entry in data["response"]["docs"]:
		try:
			val=entry["measurements"]
			mime=entry["content-type"].split(';')[0].replace('/','_').replace('+','_')
			print mime
			#parse above response and calculate the min,max and range
			if len(val)==4 and val[0][0]!='[':
				m=re.search(r"([-+]?\d+[\.]?\d*)",val[0])
				if m:
					update_min_max(mime,val[3].strip(),float(m.groups()[0]))
			else:
				for v in val:
					if v.startswith('['):
						item=v.split(",")
						p=re.search(r"([-+]?\d+[\.]?\d*)",item[0])
						if p:
							update_min_max(mime,item[3].replace(']','').strip(),float(p.groups()[0]))	
			count+=1
		except Exception, e:
			print "Failing for entry %s" % e 
			traceback.print_exc()
	print "Processed "+str(count)

get_solr_response()
print "Calculating min,max and range by type of measurement"

print mime_dict.items()
for k,v in mime_dict.items():
	type_dict={}
	for key,value in v:
		inner_dict={}
		max_value=v[key]
		inner_dict["min"]=value
		inner_dict["max"]=max_value
		inner_dict["range"]=max_value-value
		inner_dict["count"]=v[key]
		type_dict[key]=inner_dict
	final_dict[k]=type_dict

with open("final_measurement_task_d.json","w") as outFile:
	json.dump(final_dict,outFile,indent=4, sort_keys=True)
outFile.close()
