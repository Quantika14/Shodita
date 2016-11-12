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
#BOT NAME: NOBITA                          ##
#BOT ENCARGADO DE OBTENER EL WHOIS DE      ##
#Y CRUZAR LOS DATOS CON LIBREBORME         ##
#############################################

import re, time, urllib2, httplib, whois, json
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

def check_domain_mongodb(dominio):
	global client, db
	if db.Shodita.find({"dominio": dominio, "bot": "Suneo-whois-libreborme"}).count() >= 1:
		return True
	else:
		return False

def insert_mongodb(w, lb, dominio):
	try:
		client = MongoClient()
		db = client.test
		date_Insert = time.strftime("%H:%M:%S")
		date_Update = ""
		cursor = db.Shodita.insert({"dominio":dominio, "bot":"Suneo-whois-libreborme", "whois":w,"libreborme":lb,"date_insert": date_Insert, "date_Update": date_Update})
		print colores.azul + "[INFO] INSERT IN DB" + colores.normal
	except:
		print "[WARNING]ERROR INSERT MONGODB"

def invest_name(text):
	name = text.split(" ")
	new_name = ""
	lon = len(name)
	for x in range(lon,0):
		print x
		print name[x]
		new_name = name[x] + x
	return new_name

def get_target():
	global client, db
	cursor = db.Shodita.find({"bot":"Suneo"})
	for document in cursor:
		if check_domain_mongodb(document["dominio"]):
			print colores.verde + "[INFO] Domain: " + document["dominio"] + " already scanned" + colores.normal
		else:
			print "|"
			print colores.HEADER + "[NEW TARGET][INFO] Domain: " + colores.normal +  document["dominio"] 
			w = whois.whois(document['dominio'])
			name = w.name
			print colores.verde + "|----[INFO] OWNER: " + colores.normal + name
			try:
				url = "https://libreborme.net/borme/api/v1/persona/search/?q=" + str(name.replace(" ", "%20"))
				html = urllib2.urlopen(url).read()
				data = json.loads(html)
				if data["objects"][0]["resource_uri"]:
					url = "https://libreborme.net" + data["objects"][0]["resource_uri"]
					html = urllib2.urlopen(url).read()
					data = json.loads(html)
					lon_data = len(data["cargos_actuales"])
					for x in range(0, lon_data):
						print colores.HEADER + "[URL TARGET] " + colores.normal + url
						print colores.verde + "[INFO] Target Name: " + colores.normal + data["name"]
						print colores.verde + "|----[INFO] Business: " + colores.normal + data["cargos_actuales"][x]["name"]
						print colores.verde + "|----[INFO] Date From: " + colores.normal + data["cargos_actuales"][x]["date_from"]
						print colores.verde + "|----[INFO] Title: " + colores.normal + data["cargos_actuales"][x]["title"]
			except:
				pass
def main():
	get_target()

if __name__ == '__main__':  
	main()
