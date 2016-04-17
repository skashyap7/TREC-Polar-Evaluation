#!/usr/bin/python3
import os
from os import path
import json
import tika
from tika import parser
from tika import language
from langdetect import detect_langs
import pprint
root = "D:\\seperated_data"

'''
# Already done with
listing = ["application_atom+xml",
"application_dif+xml",
"application_dita+xml; format=concept",
"application_epub+zip",
"application_fits",
"application_google-earth",
"application_gzip",
"application_java-vm",
"application_msword",
"application_octet-stream",
"application_xml",
"application_postscript",
"application_rdf+xml",
"application_rss+xml",
"application_rtf",
"application_vnd.ms-excel.sheet.4",
"application_vnd.ms-htmlhelp",
"application_vnd.rn-realmedia",
"application_x-matroska",
"application_x-msdownload",
"application_x-msdownload; format=pe",
"application_x-msdownload; format=pe32",
"application_x-msmetafile",
"application_xslt+xml",
"application_x-bibtex-text-file"
"application_x-hdf",
"application_x-java-jnilib",
"application_x-lha",
"application_x-rar-compressed",
"application_x-rpm",
"application_x-sh",
"application_vnd.google-earth.kml+xml",
"application_x-7z",
"application_x-7z-compressed",
"application_x-bittorrent",
"application_x-bzip2",
"application_x-compress",
"application_x-debian-package",
"application_x-elc"
"application_x-shockwave-flash",
"application_x-sqlite3",
"application_x-stuffit",
"application_x-tar",
"application_x-tex",
"application_x-tika-ooxml",
"application_x-xz",
"application_zip",
"application_zlib",
"application_x-font-ttf",
"application_x-grib",
"application_x-gtar"
"application_x-executable"
'''

application_list =[
"application_pdf"
]


run_listing = [
"application_xhtml+xml"
]

# Done with
listing = [
"audio_basic",
"audio_mp4",
"audio_mpeg",
"audio_x-aiff",
"audio_x-flac",
"audio_x-mpegurl",
"audio_x-ms-wma",
"audio_x-wav"
]

# Done with
#"image_jpeg"

image_huge_listing = [
	"image_gif",
	"image_jpeg",
]

#done with
image_listing =[
	"image_png",
	"image_svg+xml",
	"image_tiff",
	"image_vnd.adobe.photoshop",
	"image_vnd.dwg",
	"image_vnd.microsoft.icon",
	"image_x-bpg",
	"image_x-ms-bmp",
	"image_x-xcf"
]


#done with
text_listing = [
"text_plain",
"text_html",
"message_rfc822",
"message_x-emlx",
"text_troff",
]

# Done with
light_text_listing = [
"text_x-csrc",
"text_x-diff",
"text_x-jsp",
"text_x-matlab",
"text_x-perl",
"text_x-php",
"text_x-python",
"text_x-vcard"]

#Done with
video_listing = [
"video_mp4",
"video_mpeg",
"video_quicktime",
"video_x-flv",
"video_x-m4v",
"video_x-ms-asf",
"video_x-ms-wmv",
"video_x-msvideo"
]


# Get languages for each file 
for item in run_listing:
	mime_json = {}
	#item = "text_x-perl"
	rootDir = root+"\\"+item
	pp = pprint.PrettyPrinter(indent=4)
	dirName = rootDir.split("\\")[-1]
	mime_json[dirName] = []
	for dirname, subdir , fileList in os.walk(rootDir):
		total_files = len(fileList)
		cnt = 0
		for fname in fileList:
			cnt += 1
			print("Processing file {cnt}/{t} in {dir}".format(cnt=cnt,t= total_files,dir=item))
			fpath = os.path.join(rootDir,fname)
			print("Detecting Languages in {f}".format(f=fpath))
			fjson = {}
			# Read every file and detect Language of it
			with open(fpath,"r") as fhandle:
				try:
					parsed = parser.from_file(fpath)
					#print(parsed)
					try:
						f_text = parsed["content"]
						#print(f_text)
						if f_text != None:
							#print("Found the Text to be None and hence Skipping !")
							fjson["text-count"] = len(f_text)
							#fhandle.close()
							#continue
						f_metadata = parsed["metadata"]
						#print(f_metadata)
						fjson["metadata"] = json.dumps(f_metadata)
						if isinstance(f_metadata,dict):
							fjson["metadata_length"] = len(f_metadata.keys())
							#print("Metadata Fields are: "+str(len(f_metadata.keys())))
						try:
							fjson["languages"] = {}
							languages = detect_langs(f_text)
							for l in languages:
								(lang,probability) = str(l).split(":")
								fjson["languages"][lang] = probability
						except:
							print("\n Language Detection module exncountered error")	
						#print(" Languages Detected {l}".format(l=languages))
						#pp.pprint(fjson["languages"])
					except (KeyError,ValueError):
						print("Tika could not get content for {f}".format(f=fpath))
						fjson["languages"] = " "
					fhandle.close()
					fjson["id"] = fname
					fjson["size"] = os.path.getsize(fpath)
					#print("Size of file : "+str(fjson["size"]))
				except ValueError:
					print("Tika could not get content for {f}".format(f=fpath))
				try:
					fjson["tika_language"] = language.from_file(fpath)
					#print(" Languages Detected by Tika {l}".format(l=fjson["tika_language"]))
				except UnicodeDecodeError:
					fjson["tika_language"] = " "
					print("Tika encountered problem reading the text for identifying Languages! Skipping")
				mime_json[dirName].append(fjson)

	filename = "lang_jsons//"+dirName+"_lang.json"
	with open(filename,"w") as ohandle:
		json.dump(mime_json,ohandle)
		ohandle.close()