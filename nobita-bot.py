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
import GeoIP
import netaddr
from pymongo import MongoClient

# Configuracion
# portList = [21,22,23,25,53,63,80,90,110,143,161,443,500,513,520,559,3306,3389,5000,5050, 5060, 8069,8080, 9443,27017, 28017] 
portList = [80, 443]
totalPuertos = len(portList)
ip_root = ""
timeout = 3


def insert_mongodb(IP, Country, City, regionName, ISP, Port, Banner, Latitud, Longitud, date_Insert, date_Update):
    try:
        client = MongoClient()
        db = client.test
        cursor = db.Shodita.insert({"ip":IP, "country": Country, "city": City, "region_name": regionName, "isp": ISP, "port": Port, "banner": Banner, "latitud": Latitud, "longitud": Longitud, "date_insert": date_Insert, "date_Update": date_Update, "bot":"Nobita"})
        print "[INFO] INSERT IN DB"
    except:
        print "[WARNING]ERROR INSERT MONGODB"


def geoIp(IP):
    # return urllib.urlopen("http://ip-api.com/json/" + str(IP))
    gi = GeoIP.open("/usr/share/GeoIP/GeoIPCity.dat", GeoIP.GEOIP_STANDARD)
    gir = gi.record_by_addr(IP)
    print gir
    return gir


'''Grab Banner'''
def banner_grabbing_web(ip_address,port):  
    global portList
    try:  
        s=socket.socket()  
        s.settimeout(timeout)
        s.connect((ip_address,port))
        s.send("GET HTTP/1.1 \r\n")
        banner = s.recv(2048)  
        print "[+]" + ip_address + ' : ' + str(port) + ' -BANNER- ' + banner + time.strftime("%H:%M:%S") + ' '
        return banner
    except:  
        return "none"


def banner_grabbing(ip_address,port):  
    global portList
    try:  
        s=socket.socket()  
        s.settimeout(5.0)
        s.connect((ip_address,port))  
        banner = s.recv(2048)  
        pct = str(porcentaje(portList.index(port)))
        print "[+]" + ip_address + ' : ' + str(port) + ' -BANNER- ' + banner \
                + time.strftime("%H:%M:%S") + ' ' + pct + '%'
        return banner
    except: 
        return "none"


def porcentaje(portID):
    global portList, totalPuertos
    total = (portID + 1) * 100
    total = total / totalPuertos
    return total
    

def is_valid_cidr(s):
    try:
        net = netaddr.IPNetwork(s)
        return True
    except:
        return False
        

def main():  
    global portList, totalPuertos, ip_address
    f = open("dic/targets.txt", "r")
    targets = f.readlines()

    for target in targets:
        target = target.strip()
        if not target or target.startswith("#"):
            continue
        if is_valid_cidr(target):
            for ip_address in netaddr.IPNetwork(target):
                ip_address = str(ip_address)
                print "----------------------------------------"
                print "[INFO] Connecting to: " + str(ip_address)
                for port in portList:
                    pct = str(porcentaje(portList.index(port)))
                    print "|----[!] " + str(ip_address) + " -> " + str(port) + " " + pct + "%"
                    # Obtenemos el mensaje del servidor en el puerto 
                    if port == 80 or port == 8080 or 27017 or 28017:
                        Banner = banner_grabbing_web(ip_address, port)
                    else:
                        Banner = banner_grabbing(ip_address,port)
                    if Banner == "none":
                        pass
                    else:
                        # Variables obtenidas de la geoIp
                        data_geoIP = geoIp(ip_address)
                        if data_geoIP:
                            Country = data_geoIP["country_name"]
                            City = data_geoIP["city"]
                            regionName = data_geoIP["region_name"]
                            # ISP = data_geoIP["isp"]
                            Latitud = data_geoIP["latitude"]
                            Longitud = data_geoIP["longitude"]
                            ISP = "null"
                        else:
                            ip_address = Country = City = regionName = ISP = Latitud = Longitud = "null"
                        date_Insert = time.strftime("%H:%M:%S")
                        date_Update = "none"
                        insert_mongodb(ip_address, Country, City, regionName, ISP, port, Banner, Latitud, Longitud, date_Insert, date_Update)

        else:
            print "[ERROR] Invalid target: " + target


if __name__ == '__main__':  
    main() 

