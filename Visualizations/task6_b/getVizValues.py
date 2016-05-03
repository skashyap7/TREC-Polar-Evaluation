import json

with open('final_parser_list.json','r') as fin:
	data=json.loads(fin.read())

parser_list=["x"]
m_dict={}

for entry in data:
	parser_list.append(entry)

for parser in data:
	for item in data[parser].keys():
		if item not in m_dict:
			m_dict[item]=[]
		for v in parser_list:
			if v == parser:
				m_dict[item].append(data[parser][item]["avg"])
			else:
				m_dict[item].append(0)

with open('viz_parser_list_text.txt','w') as fout:
	fout.write(str(parser_list))
	fout.write(',')
	fout.write(str(m_dict))