#!/usr/bin/python
# -*- coding: utf-8 -*-

#Ce programme permet de vérifier le systeme d'exploitation, de comparer l'espace disque disponible avec l'espace disque nécessaire renseigné, d'effectuer une copie de fichier et d'installer un paquet sous debian"

#l'argument 1 pour sys.argv, renseigné au moment du lancement du script, défini le paquet à installer"

import time, paramiko, os, sys , socket,re, logging
from datetime import datetime
from donnees import *



ips = client                                                      #import des ip
WARNING_DISK = 1                                                  #Espace en GO minimum avant WARNING sur l'espace disque restant

#POSTE_DISTANT
login = POSTE_DISTANT ['logins']                                  #Login admin des postes distant
dire = POSTE_DISTANT ['dir']                                      #Chemin du programme à désinstaller
mdp = POSTE_DISTANT ['mdp']                                       #mdp admin des postes distant
port = POSTE_DISTANT ['port_client']                              #port d'entre des postes distant

#commande à effectuer, placée en argument 1 lors du lancement du programme
command = sys.argv[1]

#SRV_LOCAL 
dir_source = SRV_LOCAL['dir_source']                               #Emplacement de la source à installer
dir_log =  SRV_LOCAL['dir_log']                                    #Emplacement des log
doc_source = SRV_LOCAL['doc_source']                               #Fichier ou prog à copier

#Réinitialisation des fichiers de log

os.system("echo ' ' > "+dir_log+"/Script_log.log")                 #Fichier de log du script en cours
os.system("echo ' ' > "+dir_log+"/disk_space.txt")                 #Fichier info espace disque du serveur distant

#Création du format d'entree du fichier de log

logging.basicConfig(filename=dir_log+'/Script_log.log',level=logging.INFO,\
	format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')

# pour chaque addresse du tableau
for ip in ips :
	d = datetime.now()                                          #Date à l'instant T
	date = d.strftime("%d/%m-%H:%M:%S")                         #Format de la date

	print ('\x1b[5;32;47m' + date +"                         connexion sur le poste : " + ip +"                        " + '\x1b[0m' )
	logging.info ('connexion au poste : '+ip)

#Etablissement de la connexion
	try:
		ssh_client = paramiko.SSHClient ()
		ssh_client.set_missing_host_key_policy (paramiko.AutoAddPolicy ()) 
		ssh_client.connect (hostname = ip, port = port, username = login, password = mdp)
		
	except paramiko.AuthenticationException:
		logging.error ( "Authentication échouée, merci de vérifier les identifiants")
		result_flag = False
	except paramiko.SSHException as sshException:
		logging.error ( "Connexion non établie: %s" % sshException)
		result_flag = False
	except socket.timeout as e:
		logging.error ( "Connexion temps dépassé")
		result_flag = False
	except Exception as e:
		logging.error ( "Erreur de connexion au serveur")
		result_flag = False

	else:
		result_flag = True

	if result_flag == True:
		logging.info('Connexion SSH ok')
		print ('connexion ssh ok')

# verification du systeme d'exploitation
	try :			
		stdin, stdout, stderr = ssh_client.exec_command("uname", timeout=10)
		exploit = stdout.readlines()
		exploit = "".join(exploit[0])
		exploit_linux = exploit[0:5]
		print (ip +" : "+ exploit_linux)
		
	except Exception as e:
		logging.error ("system different de linux ou poste injoignagle")
		print (ip + " : system different de linux ou poste injoignable")
		print ('\x1b[5;31;47m' + " fin " + '\x1b[0m')
		exploit_linux = []

	if exploit_linux == 'Linux' :		

#Récupération de l'espace libre sur poste distant 		
		stdin, stdout, stderr = ssh_client.exec_command("df -h",timeout=10)			
		output = stdout.readlines()
		output = output[3]		
		output = output.split()
		output = output[3]

# mise en forme des données disque et comparaison	
		if 'G' or 'T' in output :
			if 'T' in output :
				fact = 1000
			else : 
				fact = 1

			output = re.findall('\d+', output)			
			output = str(".".join(output))					
			
			int_disk =float(output)*fact		

# verification espace disque suffisant
			if (int(int_disk) < WARNING_DISK):
				logging.warning('Espace disque insuffisant')
				print ('espace disque insuffisant')
					
			else:
				logging.info('Espace disque pour le transfert %sG: ok' % int_disk)
				print ('espace_disque necessaire : ' + str(WARNING_DISK)+' G')			
				print ('Espace disque disponible : ' + str(int_disk) + ' G')

		
#Vérification des chemins 
				try:

					if not os.path.exists(SRV_LOCAL['dir_source']):
						print("\nERREUR: Le répértoire cible \n>> "+SRV_LOCAL[production]['dir_source']+" << \nn'est pas valide!!\n\n")

				except BaseException as e:
					logging.error(str(e))
					logging.error('Problème au niveau des répertoires cibles!!')
			

				print ("emplacement dossiers ok")

#transfert de fichier
				if dir_source != "":
					print ("fichier à transférer :" + doc_source)
					try: 
						ftp_client = ssh_client.open_sftp() 
						ftp_client.put (dir_source + doc_source, dire + doc_source) 
						logging.info (stdout.readlines ())
						logging.info ("transfert de fichier " + doc_source + " ok")
						ftp_client.close ()
						print ("transfert ok")
					except BaseException as e:
						logging.error(str(e))
						logging.error('le transfert à échoué')
		
				else :
					print (" rien a transferer")

# envoye de commande pour installer un paquet
				if command != "" :
					print ('paquet à installer : ', command)
					logging.info('paquet à installer : '+ command)
					try: 					
						stdin, stdout, stderr = ssh_client.exec_command ("sudo -S apt-get install " + command, get_pty= True, timeout=10)
						stdin.write (mdp +'\n') 
						exploit = stdout.read()
						time.sleep(2)
						logging.info (stdout.readlines())
						test = len (exploit)
						reponse = str(exploit[test-50:test])
						
						Impossible = 'Impossible'
						if Impossible in reponse :
							print ('impossible de trouver ' + command)
							logging.info ('paquet introuvable')
						else :
							print ('installation terminée')
							logging.info('installation terminée')
					
					except BaseException as e:
						logging.error(str(e))
						logging.error('la commande a échouée')
						print ('la commande a échouée')
				else :
					print ("rien a installer")

		else :
			print ("espace disque trop faible")

#fermeture de la liaison
		ssh_client.close()
		print ('\x1b[5;31;47m' + " fin " + '\x1b[0m')

	
