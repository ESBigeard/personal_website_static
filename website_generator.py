#!/usr/bin/python
# -*- coding:utf-8 -*-
"""script used to generate dynamic pages for my personal website bigeard-nlp
attention, ne génère pas la page index.html, seulement indexen et indexfr. Il faut dupliquer manuellement indexen"""

import codecs,re,sys

content_files=["index-content.html","publi-content.html","thesis-content.html","more-content.html"]



def load_content_files(fnames):

	out={} #main infos
	menu={} #liste d'url/noms de pages pour le menu

	menu["fr"]=[]
	menu["en"]=[]
	allowed_labels=["url","title_en","title_fr","content_en","content_fr"]
	allowed_labels_string="|".join(allowed_labels)
	for fname in fnames:
		with codecs.open(fname,"r","utf-8") as f:
			page_data={}
			page_data["fr"]={}
			page_data["en"]={}
			url=""
			previous=None
			for l in f:
				l=l.rstrip()
				if l.startswith("#") or (len(l)<1 and previous==None):
					continue
				
				if re.match("("+allowed_labels_string+") ?=",l):
					label,value=re.split("=",l,1)
				else:
					page_data[lgg][previous]+="<br/>"+l
					continue
				if label=="url":
					url=value
				else:
					label,lgg=label[:-3],label[-2:]
					page_data[lgg][label]=value
					previous=label

			out[url]=page_data
			menu["fr"].append([url,page_data["fr"]["title"]])
			menu["en"].append([url,page_data["en"]["title"]])
	return out,menu

def gen_page(language,url,menu,infos):
	html=u"""
	 <!DOCTYPE html>
	<html>
	<head>
	<title>Élise Bigeard</title>
	<meta charset="UTF-8"> 
	<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	<body>

	<div id="top-wrapper">
		<div id="title-wrapper">
		<h1>Élise Bigeard</h2>
		</div>

		<div id="language-switch">"""

	if language=="en":
		html+="""<p>
		<a href=" """+url+"fr.html"+""" "><img src="french.ico" width="20px" alt="switch to french" ></img></a>
		</p>
		<p class="selected">
		<a href=""><img src="english.png" width="20px" alt="switch to english" ></img></a>
		</div>
		</p>"""
	else:
		html+="""
		<p class="selected">
		<a href=""><img src="french.ico" width="20px" alt="switch to french" ></img></a>
		</p><p>
		<a href=" """+url+"en.html"+""" "><img src="english.png" width="20px" alt="switch to english" ></img></a>
		</div>
		</p>"""


	html+="""</div>

	<div id="menu-wrapper">"""

	#build the menu
	html+="<p>"
	menu_items=[]
	for couple in menu[language]:
		if couple[1]==infos[language]["title"]:#current section
			menu_items.append('<a href="'+couple[0]+language+'.html" class="menu_current">'+couple[1]+'</a>')
		else:
			menu_items.append('<a href="'+couple[0]+language+'.html">'+couple[1]+'</a>')
	menu_items=" - ".join(menu_items)
	html+=menu_items
	html+="</p>"

	#html+='<p><a href="indexfr.html">Accueil</a> - <a href="publicationsfr.html">Publications</a></p>'
	#html+='<p><a href="indexen.html">Home</a> - <a href="publicationsen.html">Publications</a></p>'
	
	#/menu
	html+="""</div>

	<div id="main-wrapper">
	<p>"""
	html+=infos[language]["content"]
	html+="""</p>
	<div>



	</body>
	</html>"""

	return html

if __name__=="__main__":
	pages,menu=load_content_files(content_files)
	for url in pages:
		page_content=pages[url]
		for language in ["en","fr"]:
			html=gen_page(language,url,menu,page_content)
			with codecs.open("generated_pages/"+url+language+".html","w","utf-8") as f:
				f.write(html)




