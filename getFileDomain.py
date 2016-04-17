#!/usr/bin/python3
import os
import json

root = "D:\\trainingdata\\"


listing = ["ae","aero","ag","ai","al","am","aq","ar","at","au","ax","bb","be","bg","biz","br","ca","camp","cat","cc","ch","cl","club","cm","cn","co","com","coop","cr","cu","cx","cz","de","dj","dk","do","ec","edu","ee","eg","enlace","es","et","eu","fi","fj","fm","fr","gd","gl","gov","gr","gs","gy","help","hk","hr","hu","id","ie","il","im","in","info","int","io","ir","is","it","jobs","jp","ke","kr","ky","kz","la","land","li","link","lt","lu","lv","ly","ma","md","me","media","mil","mn","mo","mobi","mp","ms","museum","mx","my","name","ne","net","ng","ninja","nl","no","nr","nu","nz","org","ovh","pe","ph","pk","pl","pr","pro","pt","pw","re","ro","rs","ru","sa","sc","se","sg","sh","si","sk","sm","st","th","tk","tm","to","tr","travel","tt","tv","tw","ua","ug","uk","us","uy","ve","vg","vn","vu","ws","za","zm"]
for item in listing:
	domain_json = {}
	rootDir = root+"\\"+item
	domainName = rootDir.split("\\")[-1]
	domain_json[domainName] = []
	for dirname, subdir , fileList in os.walk(rootDir):
		for fname in fileList:
			domain_json[domainName].append(fname)

	filename = domainName+"_result.json"
	with open(filename,"w") as ohandle:
		json.dump(domain_json,ohandle)
		ohandle.close()