import urllib, json
url = "http://localhost:8983/solr/language/select?q=*%3A*&indent=true&wt=json&facet=on&facet.field=langs&rows=0"
response = urllib.urlopen(url);
data = json.loads(response.read())
classified_data={}
keys=[]
values=[]
for count,val in enumerate(data["facet_counts"]["facet_fields"]["langs"]):
	if count % 2 == 0:
		keys.append(val)
	else:
		values.append(val)
classified_data=dict(zip(keys,values))
with open('solr_response_lang.json','w') as fp:
		json.dump(classified_data,fp,indent=4, sort_keys=True)