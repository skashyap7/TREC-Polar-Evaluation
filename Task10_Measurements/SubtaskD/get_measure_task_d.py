import urllib, json,re,os
import itertools
from collections import defaultdict

#read 10000 rows at a time
start=0
rows=10000

mime_dict={} # a 3 level dict { mime => { unit => {min:x, max:y, count:z} }

count=0

def get_solr_response():
	global start
	for i in range(0,5):
		try:
			url = "http://localhost:8983/solr/measure/select?q=*%3A*&fl=content-type,measurements&wt=json&indent=true&start="+str(start)+"&rows="+str(rows)+"&fq=measurements:[%27%27%20TO%20*]"
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

def update_min_max(mime,unit,value):
	unit=unit.lower()

	unit_dict={}
	if(mime not in mime_dict):
		mime_dict[mime]=unit_dict
	else:
		unit_dict=mime_dict[mime]

	unitval_dict={}
	if(unit not in unit_dict):
		unit_dict[unit]=unitval_dict
		unitval_dict["min"]=value
		unitval_dict["max"]=value
		unitval_dict["count"]=1
	else:
		unitval_dict=unit_dict[unit]
		if(unitval_dict["min"]>value):
			unitval_dict[""]=value
		if(unitval_dict["max"]<value):
			unitval_dict["max"]=value
		unitval_dict["count"]+=1

#read response from solr
def calculate_stats(data):
	global count
	for entry in data["response"]["docs"]:
		try:
			mime=entry["content-type"].lower() # update this
			val=entry["measurements"]
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
	print "Processed "+str(count)

get_solr_response()
print "Calculating range by type of measurement by mime type"
for mime,unit_dict in mime_dict.items():
	for unit,unitval_dict in unit_dict.items():
		unitval_dict["range"]=unitval_dict["max"]-unitval_dict["min"]


with open("final_measurement_task_d.json","w") as outFile:
	json.dump(mime_dict,outFile,indent=4, sort_keys=True)
outFile.close()
