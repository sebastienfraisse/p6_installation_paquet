# p6_installation_paquet
Ce script permet, sur une serie de postes distant sous debian:
  *D'établir une connexion ssh avec mot de passe.
  *De vérifier le système d'exploitation.
  *De vérifier l'espace disque disponible.
  *De vérifier l'emplacement de sauvegarde.
  *De copier un fichier (option).
  *D'installer un paquet.

# Prérequis
Pour utiliser ce script, il faut tout d'abord installer python3-paramiko, de plus, il faut que la session administrateur sur les postes distant soit identique sur tous les postes.
 
# CONFIGURATION
Plusieurs données sont à modifier 
 ## Dans le fichier donnees.py
  * les différents emplacement et le nom du document à transférer
  * les identifiants de session
  * le port ouvert pour ssh (par defaut le 22)
  * les ip des postes à modifier
 
 ## Dans p6_installation_paquet
  * Warning disk, qui correspond, en G, à l'espace disque nécessaire pour effectuer les installations
 
 
 ## Au lancement du sript
  * Il faut renseigner en argument le paquet à installer (expl : python3 p6_modif_prog nano)

# UTILISATION
Lors du lancement, une serie d'information sera affichée.
  * la machine cible
  * Si la connexion est établie
  * la verification de l'espace disque
  * la verification des chemins serveur et clients
  * si le transfert est effectué
  * si l'installation est effectuée
  * la fin du script
