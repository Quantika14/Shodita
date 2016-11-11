#!/usr/bin/python  
''' 
Copyright (C) 2016  QuantiKa14 Servicios Integrales S.L
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
#############################################
#AUTHOR: JORGE WEBSEC                      ##
#TWITTER: @JORGEWEBSEC                     ##
#BLOG: BOTENTRIANA.WORDPRESS.COM           ##
#EMAIL: JORGE@QUANTIKA14.COM               ##
#############################################
#***********BOT PRINCIPAL******************##
#BOT NAME: SUNEO                           ##
#BOT ENCARGADO DE DETECTAR CMS EN LOS      ## 
#DOMINIOS OBTENIDOS POR SHIZUKA-BOT.PY     ##
#############################################
import re, time, urllib2, httplib
from pymongo import MongoClient
from bs4 import BeautifulSoup
from urllib2 import Request, urlopen, URLError

#Colores
class colores:
    HEADER = '\033[95m'
    azul = '\033[94m'
    verde = '\033[92m'
    alerta = '\033[93m'
    FAIL = '\033[91m'
    normal = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
client = MongoClient()
db = client.test

client = MongoClient()
db = client.test

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

def check_domain_mongodb(ip, dominio):
	global client, db
	if db.Shodita.find({"ip":ip, "dominio": dominio, "bot": "Suneo"}).count() >= 1:
		return True
	else:
		return False

def get_html_without_subdomain(target):
	try:
		target = target.split(".")
		url = "http://" + target[1] + "." + target[2]
		html = urllib2.urlopen(url).read()
		return html
	except urllib2.URLError, e:
		return "False"

def get_html(target):
	url = "http://" + str(target)
	print colores.verde + "[INFO] Generate URL: " + colores.normal + str(url)
	opener = urllib2.build_opener()
	opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
	html = opener.open('http://www.stackoverflow.com').read()
	return html

def detect_wp(html, dominio):
	soup = BeautifulSoup(html, "html.parser")
	try:	
		#Buscamos generator
		gen = soup.findAll(attrs={"name":"generator"})
		if "Wordpress" in str(gen):
			return True
		else: #Buscamos wp-content en el html
			if html.find("wp-content")>0:
				return True
			else:#Buscamos links con xmlrpc.php
				links = soup.findAll("link")
				for l in links:
					if "xmlrpc.php" in str(l):
						return True
					else:#Buscamos el readme.html
						try:
							url = "http://" + dominio + "/readme.html"
							html = urllib.urlopen(url).read()
							soup = BeautifulSoup(html)
							for h1 in soup.find_all('h1', {'id':"logo"}):
								h1 = remove_tags(str(h1)) #PARSER
								if h1:
									return True
						except urllib2.HTTPError, e:
							continue 
						except urllib2.URLError, e:
							continue
						except httplib.HTTPException, e:
							continue
	except:
		return False

def detect_joomla(html):
	soup = BeautifulSoup(html, "html.parser")
	#Buscamos el generator
	try:
		gen = soup.findAll(attrs={"name":"generator"})
		if "Joomla!" in str(gen):
			return True
	except:
		return False

def detect_drupal(html):
	soup = BeautifulSoup(html, "html.parser")
	#Buscamos el generator
	try:
		gen = soup.findAll(attrs={"name":"generator"})
		if "Drupal" in str(gen):
			return True
	except:
		return False

def insert_mongodb(cms, dominio, IP):
	try:
		client = MongoClient()
		db = client.test
		date_Insert = time.strftime("%H:%M:%S")
		date_Update = ""
		cursor = db.Shodita.insert({"ip":IP, "dominio":dominio, "cms":cms, "bot":"Suneo", "date_insert": date_Insert, "date_Update": date_Update})
		print colores.azul + "[INFO] INSERT IN DB" + colores.normal
	except:
		print "[WARNING]ERROR INSERT MONGODB"

def get_target():
	global client, db
	cursor = db.Shodita.find({"bot":"Shizuka"})
	for document in cursor:
		if check_domain_mongodb(document["ip"], document["dominio"]):
			print colores.verde + "[INFO] Domain: " + document["dominio"] + " already scanned" + colores.normal
			pass
		else:
			url = "http://" + document["dominio"]
			headers = {'User-Agent' : 'Mozilla 5.10'}
			request = Request(url, None, headers)
			try:
				response = urlopen(request, timeout=10)
				if response.code == 200 or response.code == "OK":
					html = response.read()
					if detect_wp(html, document["dominio"]) == True:
						insert_mongodb("WordPress", document["dominio"], document["ip"])
						print colores.verde + "[+][INFO] " + document["dominio"] + " is WordPress" + colores.normal
					if detect_joomla(html):
						insert_mongodb("Joomla", document["dominio"], document["ip"])
						print colores.verde + "[+][INFO] " + document["dominio"] + " is Joomla" + colores.normal
					if detect_drupal(html):
						insert_mongodb("Drupal", document["dominio"], document["ip"])
						print colores.verde + "[+][INFO] " + document["dominio"] + " is Drupal" + colores.normal
			except URLError, e:
				continue
			except httplib.BadStatusLine:
				continue
			except:
				continue

def main():
	get_target()

if __name__ == '__main__':  
	main()
