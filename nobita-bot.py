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

import socket, urllib, sys, os, time, json, ssl
import GeoIP
import netaddr
from pymongo import MongoClient
from urlparse import urlparse

# Configuracion
#portList = [21,22,23,25,53,63,80,90,110,143,161,443,500,513,520,559,3306,3389,5000,5050, 5060, 8069,8080, 9443,27017, 28017]
portList = [80, 443, 8080, 27017]
totalPuertos = len(portList)
ip_root = ""
timeout = 3
_lastlocation = ''


def insert_mongodb(IP, Country, City, regionName, ISP, Port, Banner, Latitud, Longitud, date_Insert, date_Update):
    try:
        client = MongoClient()
        db = client.test
        cursor = db.Shodita.insert({"ip":IP, "country": Country, "city": City, "region_name": regionName, "isp": ISP, "port": Port, "banner": Banner, "latitud": Latitud, "longitud": Longitud, "date_insert": date_Insert, "date_Update": date_Update, "bot":"Nobita"})
        print "[INFO] INSERT IN DB"
    except:
        print "[WARNING]ERROR INSERT MONGODB"

def geoIp(IP):

    #return urllib.urlopen("http://ip-api.com/json/" + str(IP))
    gi = GeoIP.open("/usr/share/GeoIP/GeoIPCity.dat", GeoIP.GEOIP_STANDARD)
    gir = gi.record_by_addr(IP)
    print gir
    return gir

'''Grab Banner'''
def banner_grabbing_web(ip_address, port, path='/'):
    global _lastlocation

    try:
        banner = str()
        location = None

        if port in [80, 8080, 28017]:
            s = socket.socket()
            s.settimeout(timeout)
        elif port == 443:
            socketssl = socket.socket()
            socketssl.settimeout(timeout)
            s = ssl.wrap_socket(socketssl)
        s.connect((ip_address, port))
        s.send("GET "+path+" HTTP/1.1\r\nHost: "+ip_address+"\r\n\r\n")

        message = s.recv(2048)

        for bannerline in message.split('\r\n'):
            if len(bannerline) != 0:
                banner += bannerline+'\n'
                if 'location' in bannerline.lower():
                    location = bannerline.lower()
            else:
                break

        if location:
            _getlocation = location[location.index(':')+1:].strip()
            _newurl = urlparse(_getlocation)
            _lenurlbase = len(_newurl.scheme + '://' + _newurl.netloc)
            _newpath = _getlocation[_lenurlbase:]

            if _lastlocation != _newpath:
                print 1
                _lastlocation = _newpath
                banner = banner_grabbing_web(_newurl.netloc, port, _newpath)
        return banner

    except:
        return "none"

def banner_grabbing_mongo(ip_address, port):

    try:
        mongo = MongoClient(ip_address, port)
        infoserver = mongo.server_info()
        databasesname = mongo.database_names()
        serverstatus = ''
        listdatabases = ''
        banner = "none"
        for namedb in databasesname:

            try:
                if serverstatus != mongo[namedb].command('serverStatus'):
                    serverstatus = mongo[namedb].command('serverStatus')
            except:
                pass
            try:
                listdatabases = mongo[namedb].command({'listDatabases': 1})
            except Exception as error:
                if 'listDatabases may only be run against the admin database.' in error:
                    databasesname.append('admin')

        if len(infoserver) != 0 or len(serverstatus) != 0 or len(listdatabases) != 0:
            banner = str(infoserver)+'\n'+str(serverstatus)+'\n'+str(listdatabases)

        return banner
    except:
        return "none"

def banner_grabbing(ip_address, port):
    global portList
    try:
        s=socket.socket()
        s.settimeout(5.0)
        s.connect((ip_address, port))
        banner = s.recv(4096)
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
                    global _lastlocation
                    _lastlocation = ''
                    pct = str(porcentaje(portList.index(port)))
                    print "|----[!] " + str(ip_address) + " -> " + str(port) + " " + pct + "%"
                    # Obtenemos el mensaje del servidor en el puerto
                    webport = [80, 8080, 443, 28017]
                    if port in webport:
                        Banner = banner_grabbing_web(ip_address, port)
                    elif port == 27017:
                        Banner = banner_grabbing_mongo(ip_address, port)
                    else:
                        Banner = banner_grabbing(ip_address, port)

                    if Banner == "none":
                        pass
                    else:
                        print "[+]" + ip_address + ' : ' + str(port) + ' -BANNER- \n' + Banner + time.strftime("%H:%M:%S") + ' '
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
                            Country = City = regionName = ISP = Latitud = Longitud = "null"
                        date_Insert = time.strftime("%H:%M:%S")
                        date_Update = "none"
                        insert_mongodb(ip_address, Country, City, regionName, ISP, port, Banner, Latitud, Longitud, date_Insert, date_Update)
                break
            else:
                print "[ERROR] Invalid target: " + target

if __name__ == '__main__':
    main()

