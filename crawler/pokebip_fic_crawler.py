#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import re
import sys
import uuid
import shlex
import shutil
import zipfile
import subprocess
import urllib.request as request

# Merci tonton wiki
CHAPTER_TEMPLATE = """
<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>%(booktitle)s</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
	<link href="../OEBPS/css/stylesheet.css" rel="stylesheet" type="text/css"/>
</head>
<body>
	<h1>%(title)s</h1>
	<div>%(content)s</div>
</body>
</html>
"""

OPF_TEMPLATE = """
<?xml version="1.0"?>
<package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="%(uuid)s">
	<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
		<dc:title>%(booktitle)s</dc:title>
		<dc:language>fr</dc:language>
		<dc:creator opf:file-as="%(author)s" opf:role="aut">%(author)s</dc:creator>
		<dc:identifier id="uuid_id" opf:scheme="uuid">urn:uuid:%(uuid)s</dc:identifier>
	</metadata>
	<manifest>
		%(manifest)s
	</manifest>
	<spine toc="ncx">
		%(spine)s
	</spine>
	<guide>
		<reference href="chapter1.xhtml" title="Couverture" type="cover"/>
	</guide>
</package>
"""

OPF_MANIFEST_ITEM_TEMPLATE = '<item id="%(id)s" href="%(href)s" media-type="%(type)s" />\n'
OPF_SPINE_ITEM_TEMPLATE = '<itemref idref="%(id)s" />\n'

NCX_TEMPLATE = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx version="2005-1" xml:lang="en" xmlns="http://www.daisy.org/z3986/2005/ncx/">
	<head>
		<meta name="dtb:uid" content="%(uuid)s"/>
	    <meta name="dtb:depth" content="1"/>
	    <meta name="dtb:totalPageCount" content="0"/>
		<meta name="dtb:maxPageNumber" content="0"/>
	</head>
	<docTitle>
		<text>%(booktitle)s</text>
	</docTitle>
	<docAuthor>
		<text>%(author)s</text>
	</docAuthor>
	<navMap>
		%(map)s
	</navMap>
</ncx>
"""

NCX_NAVMAP_ITEM_TEMPLATE = """
<navPoint class="chapter" id="%(id)s" playOrder="%(order)d">
	<navLabel><text>%(title)s</text></navLabel>
	<content src="%(href)s" />
</navPoint>
"""

TOC_REGEX = re.compile('<a href="(.*?)">')
IMG_REGEX = re.compile('<img src="(.*?)"')

IMAGE_MIME_TYPES = {"png": "image/png", "gif": "image/gif", "jpeg": "image/jpeg", "jpg": "image/jpeg"}

def mkdir(path):
	try:
		os.mkdir(path)
	except:
		pass

if __name__ == "__main__":
	if len(sys.argv) < 5:
		print("Usage: pokebip_fic_crawler.py <table_of_contents_url> <book_name> <author> <outname>")
		exit()
	if len(sys.argv) >= 6:
		opts = sys.argv[5:]
	else:
		opts = []
	startchapter = endchapter = None
	started = True
	for opt in opts:
		if "--from=" in opt:
			startchapter = opt.partition("=")[-1].strip('"')
			started = False
		if "--to" in opt:
			endchapter = opt.partition("=")[-1].strip('"')
	if startchapter is not None:
		print("Début à '%s'" % startchapter)
	if endchapter is not None:
		print("Jusqu'à '%s'" % endchapter)
	tocurl = sys.argv[1]
	bookname = sys.argv[2]
	author = sys.argv[3]
	outname = sys.argv[4]
	# Création des dossiers
	mkdir(outname)
	mkdir(os.path.join(outname, "text"))
	mkdir(os.path.join(outname, "fonts"))
	mkdir(os.path.join(outname, "images"))
	mkdir(os.path.join(outname, "META-INF"))
	mkdir(os.path.join(outname, "OEBPS"))
	mkdir(os.path.join(outname, "OEBPS", "css"))
	# Transfert de quelques fichiers communs
	shutil.copy(os.path.join("res", "container.xml"), os.path.join(outname, "META-INF", "container.xml"))
	shutil.copy(os.path.join("res", "mimetype"), os.path.join(outname, "mimetype"))
	shutil.copy(os.path.join("res", "stylesheet.css"), os.path.join(outname, "OEBPS", "css", "stylesheet.css"))
	shutil.copy(os.path.join("res", "DejaVuSans.ttf"), os.path.join(outname, "fonts", "DejaVuSans.ttf"))
	shutil.copy(os.path.join("res", "DejaVuSans-Italic.ttf"), os.path.join(outname, "fonts", "DejaVuSans-Italic.ttf"))
	shutil.copy(os.path.join("res", "DejaVuSans-Bold.ttf"), os.path.join(outname, "fonts", "DejaVuSans-Bold.ttf"))
	# Initialisation des métadonnées
	opfmanifest = ""
	opfspine = ""
	ncxmap = ""
	data = {"id": "font", "href": "../fonts/DejaVuSans.ttf", "type": "application/x-font-truetype"}
	opfmanifest += OPF_MANIFEST_ITEM_TEMPLATE % data
	data = {"id": "fontitalic", "href": "../fonts/DejaVuSans-Italic.ttf", "type": "application/x-font-truetype"}
	opfmanifest += OPF_MANIFEST_ITEM_TEMPLATE % data
	data = {"id": "fontbold", "href": "../fonts/DejaVuSans-Bold.ttf", "type": "application/x-font-truetype"}
	opfmanifest += OPF_MANIFEST_ITEM_TEMPLATE % data
	data = {"id": "css", "href": "css/stylesheet.css", "type": "text/css"}
	opfmanifest += OPF_MANIFEST_ITEM_TEMPLATE % data
	data = {"id": "ncx", "href": "toc.ncx", "type": "application/x-dtbncx+xml"}
	opfmanifest += OPF_MANIFEST_ITEM_TEMPLATE % data
	# Couverture, pas trop complexe
	data = {"booktitle": bookname, "title": bookname, "content": "<p><i>%s</i></p>" % author}
	html = CHAPTER_TEMPLATE % data
	with open(os.path.join(outname, "OEBPS", "chapter1.xhtml"), "w", encoding="utf-8") as f:
		f.write(html)
	data = {"id": "cover", "href": "chapter1.xhtml", "type": "application/xhtml+xml"}
	opfmanifest += OPF_MANIFEST_ITEM_TEMPLATE % data
	if "--repack" not in opts:
		# Récupération des URL des pages
		f = request.urlopen(tocurl)
		html = f.read().decode("utf-8")
		f.close()
		# Séparation de la table des matières
		start = html.index('<div class="fanfics-liste-chapitres">')
		end = html[start:].index('</div>')
		toc = html[start:start + end]
		# Et extraction
		chapter = 0
		while '<a href' in toc:
			# Récupération du texte
			start = toc.index('<a href')
			end = toc.index('</a>')
			line = toc[start:end]
			toc = toc[end + 4:]
			match = TOC_REGEX.match(line)
			if match is None:
				print("Erreur pour la récupération de l'URL du chapitre %d" % chapter)
				chapter += 1
				continue
			url = "https://www.pokebip.com/" + match.groups()[0]
			title = line[match.end():].strip()
			if startchapter is not None:
				if not started and startchapter.lower() in title.lower():
					started = True
			if endchapter is not None:
				if started and endchapter.lower() in title.lower():
					started = None
			# Récupération du chapitre
			if started == True or started is None:
				print("\nRécupération du chapitre %d" % chapter)
				print("URL du chapitre : %s" % url)
				print("Titre du chapitre : %s" % title)
				f = request.urlopen(url)
				html = f.read().decode("utf-8")
				f.close()
				starttxt = html.index('<div class="fanfics-affichage-chapitre-corps">')
				usingtxt = html[starttxt:].replace('<div class="fanfics-affichage-chapitre-corps">', '<div class="text">')
				endtxt = usingtxt.index('</div>')
				content = usingtxt[:endtxt] + "</div>"
				# Insertion des images
				sub = content
				while "<img" in sub:
					start = sub.index("<img")
					end = sub[start:].index(">")
					line = sub[start: start + end]
					sub = sub[start + end + 1:]
					match = IMG_REGEX.match(line)
					if match is None:
						print("Erreur pour la récupération d'une image dans le chapitre %d" % chapter)
						continue
					imgurl = match.groups()[0].strip()
					f = request.urlopen(imgurl)
					data = f.read()
					f.close()
					imgname = imgurl.split("/")[-1]
					imgid = imgname.replace(".", "_")
					with open(os.path.join(outname, "images", imgname), "wb") as f:
						f.write(data)
					data = {"id": imgid, "href": "../images/%s" % imgname, "type": IMAGE_MIME_TYPES[imgname.split(".")[-1].lower()]}
					opfmanifest += OPF_MANIFEST_ITEM_TEMPLATE % data
					content = content.replace(imgurl, "../images/%s" % imgname)

				# Génération du HTML de sortie
				data = {"booktitle": bookname, "title": title, "content": content}
				final = CHAPTER_TEMPLATE % data
				refid = "part%05d" % chapter
				with open(os.path.join(outname, "text", "%s.html" % refid), "w", encoding="utf-8") as h:
					h.write(final)
				# Ajout dans les métadonnées
				data = {"id": refid, "href": "../text/%s.html" % refid, "type": "application/xhtml+xml"}
				opfmanifest += OPF_MANIFEST_ITEM_TEMPLATE % data
				data = {"id": refid}
				opfspineitem = OPF_SPINE_ITEM_TEMPLATE % data
				opfspine += opfspineitem
				data = {"id": refid, "href": "../text/%s.html" % refid, "title": title, "order": chapter + 1}
				ncxmapitem = NCX_NAVMAP_ITEM_TEMPLATE % data
				ncxmap += ncxmapitem
				chapter += 1
			if started is None:
				started = False

		# Finalisation des métadonnées, commence par OPF
		uniqueid = uuid.uuid5(uuid.NAMESPACE_URL, tocurl)
		data = {"booktitle": bookname, "author": author, "uuid": uniqueid, "manifest": opfmanifest, "spine": opfspine}
		opf = OPF_TEMPLATE % data
		with open(os.path.join(outname, "OEBPS", "content.opf"), "w", encoding="utf-8") as f:
			f.write(opf)
		data = {"booktitle": bookname, "author": author, "uuid": uniqueid, "map": ncxmap}
		ncx = NCX_TEMPLATE % data
		with open(os.path.join(outname, "OEBPS", "toc.ncx"), "w", encoding="utf-8") as f:
			f.write(ncx)

	outpath = os.path.join("..", "ebooks", outname + ".epub")
	out = zipfile.ZipFile(outpath, "w", compression=zipfile.ZIP_DEFLATED)
	for path, dirs, files in os.walk(outname):
		for filename in files:
			filepath = os.path.join(path, filename)
			arcpath = os.path.join(path.partition(os.path.sep)[-1], filename)
			out.write(filepath, arcpath)
	out.close()
	if "--clean" in opts:
		shutil.rmtree(outname)

	# Conversion
	subprocess.run(("ebook-convert", outpath, outpath.replace(".epub", ".pdf")))
	subprocess.run(("ebook-convert", outpath, outpath.replace(".epub", ".azw3")))
