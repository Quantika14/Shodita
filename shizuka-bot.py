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
#BOT NAME: SHIZUKA                         ##
#BOT ENCARGADO DE OBTENER LOS DOMINIOS     ## 
#ASOCIADOS A UNA MISMA IP CON ROBTEX       ##
#############################################

import urllib, urllib2, re, time
from pymongo import MongoClient
from bs4 import BeautifulSoup

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


TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

def insert_mongodb(ip, dominio):
	global client, db
	try:
		date_Insert = time.strftime("%H:%M:%S")
		date_Update = ""
		cursor = db.Shodita.insert({"ip":ip, "dominio":dominio, "date_insert": date_Insert, "date_Update": date_Update, "bot": "Shizuka"})
		print colores.azul + "[INFO] INSERT IN DB " + dominio + colores.normal
	except:
		print colores.alerta + "[WARNING] ERROR INSERT IN MONGODB" + colores.normal


def check_domain_mongodb(ip, dominio):
	global client, db
	if db.Shodita.find({"ip":ip, "dominio": dominio}).count() >= 1:
		return True
	else:
		return False


def get_domain(target):
	url = "https://www.robtex.net/?dns=" + str(target) + "&rev=1"
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser')
	table = soup.findAll("td")
	table = remove_tags(str(table))
	data = table.split(",")
	for d in data:
		if len(d) > 10:
			d = d.replace(" ", "")
			d = d.replace("]","")
			if check_domain_mongodb(target, d):
				print "[INFO]" + str(d) + " in " + str(target) + " already insert ..."
			else:
				insert_mongodb(target, d)
				print colores.verde + "[INFO]" + str(d) + " in " + str(target) + " insert ..." + colores.normal
				
def get_target():
	global client, db
	cursor = db.Shodita.find({"port":80})
	for document in cursor:
		get_domain(document["ip"])

def main():
	get_target()
if __name__ == '__main__':  
	main()
