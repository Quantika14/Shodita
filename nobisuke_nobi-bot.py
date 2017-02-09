#!/usr/bin/python  
''' 
Copyright (C) 2017  QuantiKa14 Servicios Integrales S.L
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
#AUTHOR: Fare9                             ##
#TWITTER: @erockandblues                   ##
#BLOG: estacion-informatica.com            ##
#EMAIL: farenain9@gmail.com                ##
#############################################
#***********BOT PRINCIPAL******************##
#BOT NAME: Nobisuke Nobi                   ##
#BOT ENCARGADO DE BUSCAR SERVICIOS WEB     ##
#Y SACAR UN SCREENSHOT                     ##
#############################################

import sys
import os
import threading
import urllib2
import time

#librerias selenium
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#para coger rangos de ips
from netaddr import IPNetwork,IPAddress


from pymongo import MongoClient

subnet = '' 
timeout = 0.5

dic = os.getcwd() + os.sep + "dic/targets.txt"

def tryConnection(IP):
    '''
        Metodo para hacer conexiones con urllib2, 
        miraremos si la IP recibe un response al conectarse, sea cual sea 
    '''
    try:
        if "http" not in str(IP):
            aux = "http://"+str(IP)
        response = urllib2.urlopen(aux,timeout=timeout)
        if (len(response.read()) != 0) and (response.getcode() != 403) and (response.getcode() != 500) and (response.getcode() != 404):
            return True
        else:
            return False
    except Exception as e:
        #print '[-] ERROR TRYING CONNECT: (%s) %s'%(str(IP),e)
        return False

def screenShot(ImageFolder,IP):
    ''' 
        Metodo para hacer el screenshot con selenium haciendo la conexion
        a la web en caso sea posible esa conexion.
    '''
    

    print '[INFO] Trying to connect to:',str(IP)
    IP = str(IP)
    if 'http' not in IP:
        aux = 'http://'+IP 
    #ahora conectar y screenshot
    try:
        if not ImageFolder.endswith('/'):
            nombreScreenShot = ImageFolder+'/'+IP+'.png'
        else:
            nombreScreenShot = ImageFolder+IP+'.png'
        client = MongoClient()
        db = client.test
        db.Nobisuke.insert({"IP":str(IP),"Picture":str(nombreScreenShot),"bot":"Nobisuke Nobi"})
        driver = webdriver.Firefox()
        driver.get(aux)
        driver.save_screenshot(nombreScreenShot)
        driver.quit()
    except Exception as e:
        print '[-] ERROR TRYING SCREENSHOT: (%s) %s'%(IP,e)


def main():
    global timeout
    global subnet
    global check

    folder = os.getcwd() + os.sep + "Images"

    # Para ver si existe el directorio y si no lo creo
    if not os.path.exists(folder):
        print "[INFO] Creating folder for images..."
        os.makedirs(folder)

    if not os.path.exists(dic):
        print "[ERROR] Dictionary with targets doesn't exist"
        sys.exit(-1)

    line = ''

    # abrimos el archivo
    table_dict = open(dic,"r")
    while True:
        line = table_dict.readline()

        if not line:
            break
        subnet = str(line)

        print "[INFO] Scanning subnet: "+subnet
        subnetTotal = float(len(IPNetwork(subnet)))
        i = 0.0
        for ip in IPNetwork(subnet):

            i += 1.0
            porcentaje = int((i / subnetTotal)*100.0)
            sys.stdout.write("="*porcentaje + "> "+str(porcentaje)+"% "+str(ip)+"\r")
            sys.stdout.flush()
            if tryConnection(ip):
                t = threading.Thread(target=screenShot,args=(folder,ip))
                t.start()
                #si hemos podido conectar demos tiempo para que se monte el navegador
                time.sleep(5)

if __name__ == '__main__':
    main()



