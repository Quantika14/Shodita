# ¿Qué es Shodita?
Un conjunto de bots creados en Python que recogen los datos de los banner grabbing de miles de IPs v4. Analiza la información y la muestra. Además incluye bots de ataques de fuerza bruta, aun falta por implementar sistema de lanzadera de exploits.

# ¿Qué necesitas?
 - Python 2.7
 - MongoDB >= 2.6.10

# Bot Nobita-bot.py
- Encargado de enviar peticiones y almacenar los banner grabbing de los diferentes puertos del target.
- Dependencias -> socket, urllib, sys, os, time, json, GeoIP, pymongo
- Autor: @JorgeWebsec

# Bot Shizuka-bot.py
- Encarga de obtener los dominios asociacidos a la misma IP que tenga el puerto 80 abierto.
- Dependencias -> urllib, urllib2, re, time, pymongo, bs4
- Autor: @JorgeWebsec

# Bot Suneo-bot.py
- Encargado de clasificar los diferentes dominios webs por WordPress, Joomla y Drupal.
- Dependencias -> re, time, urllib2, httplib, pymongo, MongoClient, bs4, urllib2, Request
- Autor: @JorgeWebsec

# Bot Suneo-whois-libreborme.py
- Encargado de obtener la información del titular de un dominio y cruzar los datos con LibreBorme.
- Dependencias -> re, time, urllib2, httplib, whois, json, pymongo, bs4
- Autor: @JorgeWebsec

# Bot Gigante-ssh-bot.py
- Encargado de realizar comprobaciones de fuerza bruta en servicios SSH y FTP.
- Dependencias -> paramiko, time, sys, os, socket, pymongo, MongoClient
- Autor: @JorgeWebsec

# Bot nobisuke_nobi-bot.py
- Encargado de buscar servicios web en rangos IP y realizar un screenshot.
- Dependencias -> Firefox, pymongo, MongoClient, sys, os, threading, urllib2, time, selenium, netaddr
- Autor: @Erockandblues

# Contacto
- Twitter: @jorgewebsec
- Email: jorge@quantika14.com
