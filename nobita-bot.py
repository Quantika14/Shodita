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
#BOT ENCARGADO DE OBTENER EL               ## 
#BANNER_GRABBING DE LAS IPS GENERADAS      ##
#POR EL BOT                                ##
#############################################

import socket, urllib, sys, os, time, json
from pymongo import MongoClient
portList = [21,22,23,25,53,63,80,90,110,143,161,443,500,513,520,559,3306,3389,5000,5050, 5060, 8069,8080, 9443,27017, 28017] 
totalPuertos =  len(portList)
ip_root = ""

def insert_mongodb(IP, Country, City, regionName, ISP, Port, Banner, Latitud, Longitud, date_Insert, date_Update):
	try:
		client = MongoClient()
		db = client.test
		cursor = db.Shodita.insert({"ip":IP, "country": Country, "city": City, "region_name": regionName, "isp": ISP, "port": Port, "banner": Banner, "latitud": Latitud, "longitud": Longitud, "date_insert": date_Insert, "date_Update": date_Update, "bot":"Nobita"})
		print "[INFO] INSERT IN DB"
	except:
		print "[WARNING]ERROR INSERT MONGODB"

def geoIp(IP):
	return urllib.urlopen("http://ip-api.com/json/" + str(IP))

'''Grab Banner'''
def banner_grabbing_web(ip_address,port):  
	global portList
	try:  
		s=socket.socket()  
		s.settimeout(5.0)
		s.connect((ip_address,port))
		s.send("GET HTTP/1.1 \r\n")
		banner = s.recv(2048)  
		print "[+]" + ip_address + ' : ' + str(port) + ' -BANNER- ' + banner + time.strftime("%H:%M:%S") + ' '
		return banner
	except:  
		#print "[-]" + ip_address + ' : ' + str(port) + ' -BANNER- CLOSE ' + time.strftime("%H:%M:%S") + ' ' + porc + '%'
		return "none"
		
def banner_grabbing(ip_address,port):  
	global portList
	try:  
		s=socket.socket()  
		s.settimeout(5.0)
		s.connect((ip_address,port))  
		banner = s.recv(2048)  
		porc = str(porcentaje(portList.index(port)))
		print "[+]" + ip_address + ' : ' + str(port) + ' -BANNER- ' + banner + time.strftime("%H:%M:%S") + ' ' + porc + '%'
		return banner
	except:  
		#porc = str(porcentaje(portList.index(port)))
		#print "[-]" + ip_address + ' : ' + str(port) + ' -BANNER- CLOSE ' + time.strftime("%H:%M:%S") + ' ' + porc + '%'
		return "none"

def porcentaje(portID):
	global portList, totalPuertos
	total = portID * 100
	total = total / totalPuertos
	return total
	
def main():  
	global portList, totalPuertos, ip_address
	#***CAMBIAR SEGÚN EL TOTAL DE IPS A ESCANEAR***

	#for x1 in range(1,256):
	#	for x2 in range(0,256):
	#		for x3 in range(0,256):
	#**********************************************
	for x4 in range(0,256):
		for port in portList:  
			#ip_address = str(x1) + "." + str(x2) + "." + str(x3) + "." + str(x4)
			ip_address = ip_root + str(x4)
			porc = str(porcentaje(portList.index(port)))
			print "[INFO] " + str(ip_address) + " " + port + " " + porc + "%"
			#Obtenemos el mensaje del servidor en el puerto 
			if port == 80 or port == 8080 or 27017 or 28017:
				Banner = banner_grabbing_web(ip_address, port)
			else:
				Banner = banner_grabbing(ip_address,port)

			if Banner == "none":
				pass
			else:
				#Variables obtenidas de la geoIp
				data_geoIP = geoIp(ip_address)
				data_geoIP = json.load(data_geoIP)
				Country = data_geoIP["country"]
				City = data_geoIP["city"]
				regionName = data_geoIP["regionName"]
				ISP = data_geoIP["isp"]
				Latitud = data_geoIP["lat"]
				Longitud = data_geoIP["lon"]
				date_Insert = time.strftime("%H:%M:%S")
				date_Update = "none"
				#Mandamos los datos a la función encargada de insertarlos en mongoDB
				insert_mongodb(ip_address, Country, City, regionName, ISP, port, Banner, Latitud, Longitud, date_Insert, date_Update)
						
if __name__ == '__main__':  
	main()  
