from __future__ import division
import urllib, json,re,os
import itertools
from collections import defaultdict
import sys, traceback

#read 10000 rows at a time
start=0
rows=10000
parser_dict={}
count_dict=defaultdict(int)
type_dict={}
count=0

def get_solr_response():
	global start
	for i in range(0,30):
		try:
			url="http://localhost:8983/solr/language/select?q=*%3A*&fl=text-count,size,Content-Type,X-Parsed-By&wt=json&indent=true&start="+str(start)+"&rows="+str(rows)
			response = urllib.urlopen(url);
			data = json.loads(response.read())
			calculate_stats(data)		
			#set start and rows - pagination
			start+=rows+1
		except Exception, e:
			traceback.print_exc()
			print "Solr: Failed at " + str(start) + " %s" % e
			with open("parse_list.json","w") as outFile:
				json.dump(parser_dict,outFile,indent=4, sort_keys=True)
			outFile.close()

#read response from solr
def calculate_stats(data):
	global count
	for entry in data["response"]["docs"]:
		try:
			val ='/'.join(str(x).replace('org.apache.tika.parser.','') for x in entry["X-Parsed-By"])
			#parse above response
			content_type='***'.join(str(x) for x in entry["Content-Type"])
			if val not in parser_dict:
				parser_dict[val]={}
			if content_type not in parser_dict[val]:
				parser_dict[val][content_type]={}
				parser_dict[val][content_type]["avg"]=0
				parser_dict[val][content_type]["size"]=0
				parser_dict[val][content_type]["text-count"]=0
			parser_dict[val][content_type]["size"]+=entry["size"]
			parser_dict[val][content_type]["text-count"]+=entry["text-count"]
			count+=1
		except KeyError:
			pass
	print "Processed "+str(count)

get_solr_response()
print "Writing to json output file..."

print "Calculating avg of text-count and size"
for val in parser_dict:
	for mime in parser_dict[val]:
		sum_size=parser_dict[val][mime]["size"]
		sum_text=parser_dict[val][mime]["text-count"]
		avg=(sum_text/sum_size)
		parser_dict[val][mime]["avg"]=avg
		parser_dict[val][mime].pop("size", None)
		parser_dict[val][mime].pop("text-count", None)


with open("final_parser_list.json","w") as outFile:
	json.dump(parser_dict,outFile,indent=4, sort_keys=True)
outFile.close()
