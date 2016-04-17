#!/usr/bin/python3

import simplejson as json
import argparse
import itertools


domain_json = "domain_json"   # Path to domain_json
ttr_json = "ttr_json"      # Path to all the ttr jsons
lang_json = "lang_json"  # Path to all the jsons that need to add the field


def getFilesinDir(rootDir):
	filelisting = []
	for dirname, subdir , fileList in os.walk(rootDir):
		for fname in fileList:
			filelisting.append(os.path.join(rootDir,fname))
	return filelisting

def addTTRMetadata(filelist1,filelist2):
	# Read both the file in filelist with same mime-name
	# Read the contents of each and file each id field and merge in final
	for item in filelist1:
		elem_list = item.split("_")
		mime-name = elem_list[0] + "_" + elem_list[1]
		print(mime-name)

lang_files = getFilesinDir(lang_json)
ttr_files = getFilesinDir(ttr_json)
addTTRMetadata(lang_files,ttr_files)