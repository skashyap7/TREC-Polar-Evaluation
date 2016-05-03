import urllib, json,re,os
import itertools
from collections import defaultdict

#read 10000 rows at a time
start=0
rows=10000
min_dict={}
max_dict={}
count_dict=defaultdict(int)
type_dict={}
count=0

def get_solr_response():
	global start
	for i in range(0,5):
		try:
			url = "http://localhost:8983/solr/measure/select?q=*%3A*&fl=measurements&wt=json&indent=true&start="+str(start)+"&rows="+str(rows)+"&fq=measurements:[%27%27%20TO%20*]"
			response = urllib.urlopen(url);
			data = json.loads(response.read())
			calculate_stats(data)		
			#set start and rows - pagination
			start+=rows+1
		except Exception, e:
			print "Solr: Failed at " + str(start) + " %s" % e
			with open("min_measurement_list.json","w") as outFile:
				json.dump(min_dict,outFile,indent=4, sort_keys=True)
			outFile.close()
			with open("max_measurement_list.json","w") as outFile:
				json.dump(max_dict,outFile,indent=4, sort_keys=True)
			outFile.close()

def update_min_max(unit,value):
	unit=unit.lower()
	if (unit in min_dict and min_dict[unit]>value) or unit not in min_dict:
		min_dict[unit]=value
	if (unit in max_dict and max_dict[unit]<value) or unit not in max_dict:
		max_dict[unit]=value
	count_dict[unit]+=1

#read response from solr
def calculate_stats(data):
	global count
	for entry in data["response"]["docs"]:
		try:
			val=entry["measurements"]
			#parse above response and calculate the min,max and range
			if len(val)==4 and val[0][0]!='[':
				m=re.search(r"([-+]?\d+[\.]?\d*)",val[0])
				if m:
					update_min_max(val[3].strip(),float(m.groups()[0]))
			else:
				for v in val:
					if v.startswith('['):
						item=v.split(",")
						p=re.search(r"([-+]?\d+[\.]?\d*)",item[0])
						if p:
							update_min_max(item[3].replace(']','').strip(),float(p.groups()[0]))	
			count+=1
		except Exception, e:
			print "Failing for entry %s" % e
	print "Processed "+str(count)

get_solr_response()
print "Calculating min,max and range by type of measurement"
for key,value in min_dict.items():
	inner_dict={}
	max_value=max_dict[key]
	inner_dict["min"]=value
	inner_dict["max"]=max_value
	inner_dict["range"]=max_value-value
	inner_dict["count"]=count_dict[key]
	type_dict[key]=inner_dict

with open("final_measurement_list.json","w") as outFile:
	json.dump(type_dict,outFile,indent=4, sort_keys=True)
outFile.close()
